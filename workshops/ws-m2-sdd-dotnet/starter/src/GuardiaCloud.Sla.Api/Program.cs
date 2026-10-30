using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Services;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddProblemDetails();
builder.Services.AddSingleton(TimeProvider.System);
builder.Services.AddSingleton<IIncidentRepository, InMemoryIncidentRepository>();
builder.Services.AddSingleton<SlaCalculator>();

var app = builder.Build();

app.UseExceptionHandler();

var group = app.MapGroup("/api/incidents");

group.MapPost("/", (
    CreateIncidentRequest request,
    IIncidentRepository repository,
    TimeProvider timeProvider) =>
{
    if (string.IsNullOrWhiteSpace(request.TenantId) || string.IsNullOrWhiteSpace(request.Title))
    {
        return Results.Problem(
            title: "Datos de incidente inválidos",
            detail: "TenantId y Title son obligatorios.",
            statusCode: StatusCodes.Status400BadRequest);
    }

    var incident = new Incident
    {
        TenantId = request.TenantId.Trim(),
        Title = request.Title.Trim(),
        Priority = request.Priority,
        OpenedAtUtc = (request.OpenedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime()
    };

    repository.Add(incident);
    return Results.Created($"/api/incidents/{incident.Id}", incident);
});

group.MapGet("/{id:guid}", (Guid id, IIncidentRepository repository) =>
{
    var incident = repository.GetById(id);
    return incident is not null
        ? Results.Ok(incident)
        : Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound);
});

group.MapGet("/{id:guid}/sla", (
    Guid id,
    IIncidentRepository repository,
    SlaCalculator calculator) =>
{
    var incident = repository.GetById(id);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound);
    }

    return Results.Ok(calculator.Evaluate(incident));
});

group.MapPost("/{id:guid}/resolve", (
    Guid id,
    [FromBody] ResolveIncidentRequest? request,
    IIncidentRepository repository,
    TimeProvider timeProvider) =>
{
    var incident = repository.GetById(id);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound);
    }

    var resolvedAt = (request?.ResolvedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime();
    if (resolvedAt < incident.OpenedAtUtc)
    {
        return Results.Problem(
            title: "Fecha de resolución inválida",
            detail: "ResolvedAtUtc no puede ser anterior a OpenedAtUtc.",
            statusCode: StatusCodes.Status422UnprocessableEntity);
    }

    incident.Status = IncidentStatus.Resolved;
    incident.ResolvedAtUtc = resolvedAt;
    return Results.Ok(incident);
});

app.Run();

public partial class Program;
