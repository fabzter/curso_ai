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

group.MapPost("/{id:guid}/sla/pause", (
    Guid id,
    PauseSlaRequest request,
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

    if (string.IsNullOrWhiteSpace(request.RequestedBy) || string.IsNullOrWhiteSpace(request.EvidenceNote))
    {
        return Results.Problem(
            title: "Datos de auditoría incompletos",
            detail: "RequestedBy y EvidenceNote son obligatorios para pausar el SLA.",
            statusCode: StatusCodes.Status400BadRequest);
    }

    if (incident.Status == IncidentStatus.Resolved)
    {
        return Results.Problem(
            title: "Transición de estado inválida",
            detail: "No se puede pausar el SLA de un incidente que ya está Resolved.",
            statusCode: StatusCodes.Status409Conflict);
    }

    if (incident.PauseWindows.Any(w => w.IsActive))
    {
        return Results.Problem(
            title: "SLA ya se encuentra pausado",
            detail: "Existe una ventana de pausa activa para este incidente.",
            statusCode: StatusCodes.Status409Conflict);
    }

    var pausedAt = (request.PausedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime();
    if (pausedAt < incident.OpenedAtUtc)
    {
        return Results.Problem(
            title: "Fecha de pausa inválida",
            detail: "PausedAtUtc no puede ser anterior a OpenedAtUtc.",
            statusCode: StatusCodes.Status422UnprocessableEntity);
    }

    // Regla OpenSpec cap-p1-pause-budget:
    // Para incidentes CriticalP1, si ya se agotaron los 30 minutos acumulados de pausa,
    // no se permite abrir una nueva pausa sin SupervisorOverrideCode.
    var maxBudget = SlaPolicyCatalog.GetMaxPauseBudgetMinutes(incident.Priority);
    var alreadyPausedMinutes = incident.PauseWindows.Sum(w => w.GetDurationMinutes(pausedAt));
    var hasOverride = !string.IsNullOrWhiteSpace(request.SupervisorOverrideCode)
        || incident.PauseWindows.Any(w => !string.IsNullOrWhiteSpace(w.SupervisorOverrideCode));

    if (maxBudget.HasValue && alreadyPausedMinutes >= maxBudget.Value && !hasOverride)
    {
        return Results.Problem(
            title: "Presupuesto de pausa P1 agotado",
            detail: $"Los incidentes CriticalP1 tienen un tope acumulado de {maxBudget.Value} minutos de pausa. Se requiere SupervisorOverrideCode.",
            statusCode: StatusCodes.Status422UnprocessableEntity);
    }

    var window = new SlaPauseWindow
    {
        Reason = request.Reason,
        RequestedBy = request.RequestedBy.Trim(),
        EvidenceNote = request.EvidenceNote.Trim(),
        SupervisorOverrideCode = string.IsNullOrWhiteSpace(request.SupervisorOverrideCode)
            ? null
            : request.SupervisorOverrideCode.Trim(),
        PausedAtUtc = pausedAt
    };

    incident.PauseWindows.Add(window);
    incident.Status = IncidentStatus.WaitingForCustomer;

    return Results.Ok(incident);
});

group.MapPost("/{id:guid}/sla/resume", (
    Guid id,
    ResumeSlaRequest request,
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

    if (string.IsNullOrWhiteSpace(request.ResumedBy))
    {
        return Results.Problem(
            title: "Datos de auditoría incompletos",
            detail: "ResumedBy es obligatorio para reanudar el SLA.",
            statusCode: StatusCodes.Status400BadRequest);
    }

    var activeWindow = incident.PauseWindows.SingleOrDefault(w => w.IsActive);
    if (activeWindow is null)
    {
        return Results.Problem(
            title: "El SLA no está en pausa",
            detail: "No existe una ventana de pausa activa para reanudar.",
            statusCode: StatusCodes.Status409Conflict);
    }

    var resumedAt = (request.ResumedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime();
    if (resumedAt < activeWindow.PausedAtUtc)
    {
        return Results.Problem(
            title: "Fecha de reanudación inválida",
            detail: "ResumedAtUtc no puede ser anterior a PausedAtUtc.",
            statusCode: StatusCodes.Status422UnprocessableEntity);
    }

    activeWindow.ResumedAtUtc = resumedAt;
    activeWindow.ResumedBy = request.ResumedBy.Trim();
    incident.Status = IncidentStatus.InProgress;

    return Results.Ok(incident);
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

    // Si se resuelve estando en pausa, cerramos automáticamente la ventana activa en resolvedAt
    var activeWindow = incident.PauseWindows.SingleOrDefault(w => w.IsActive);
    if (activeWindow is not null)
    {
        activeWindow.ResumedAtUtc = resolvedAt;
        activeWindow.ResumedBy = "system:auto-resume-on-resolve";
    }

    incident.Status = IncidentStatus.Resolved;
    incident.ResolvedAtUtc = resolvedAt;
    return Results.Ok(incident);
});

app.Run();

public partial class Program;
