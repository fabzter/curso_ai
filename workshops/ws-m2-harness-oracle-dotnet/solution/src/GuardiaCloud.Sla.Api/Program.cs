using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton(TimeProvider.System);
builder.Services.AddSingleton<InMemoryIncidentStore>();
builder.Services.AddSingleton<SlaRuleEngine>();
builder.Services.AddProblemDetails();

var app = builder.Build();

app.MapGet("/api/sla/incidents/{incidentId}", (
    string incidentId,
    InMemoryIncidentStore store,
    SlaRuleEngine engine) =>
{
    var incident = store.GetById(incidentId);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe el incidente '{incidentId}'.",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://errors.guardiacloud.internal/sla/incident-not-found",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
    }

    return Results.Ok(new
    {
        incident.IncidentId,
        incident.ClientTier,
        incident.Severity,
        IsBreached = engine.IsIncidentBreached(incident)
    });
});

app.MapPost("/api/sla/credits/calculate", (
    SlaCreditCalculationRequest request,
    InMemoryIncidentStore store,
    SlaRuleEngine engine) =>
{
    if (request.MonthlyInvoiceUsd <= 0)
    {
        return Results.Problem(
            title: "Monto de factura mensual inválido",
            detail: "El monto MonthlyInvoiceUsd debe ser mayor que cero.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://errors.guardiacloud.internal/sla/invalid-invoice-amount",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-400-INVALID-INVOICE-AMOUNT" });
    }

    if (string.IsNullOrWhiteSpace(request.ClientTier) ||
        !SlaRuleEngine.AllowedClientTiers.Contains(request.ClientTier.Trim()))
    {
        return Results.Problem(
            title: "Tier de cliente inválido",
            detail: $"El tier '{request.ClientTier}' no pertenece al catálogo contractual.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://errors.guardiacloud.internal/sla/invalid-client-tier",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-400-INVALID-CLIENT-TIER" });
    }

    var matchedIncidents = new List<IncidentEntry>();
    foreach (var id in request.IncidentIds ?? [])
    {
        var found = store.GetById(id);
        if (found is null)
        {
            return Results.Problem(
                title: "Incidente no encontrado",
                detail: $"No existe el incidente '{id}' incluido en la liquidación.",
                statusCode: StatusCodes.Status404NotFound,
                type: "https://errors.guardiacloud.internal/sla/incident-not-found",
                extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
        }

        matchedIncidents.Add(found);
    }

    var result = engine.CalculateMonthlyCredit(request.ClientTier, request.MonthlyInvoiceUsd, matchedIncidents);
    return Results.Ok(result);
});

app.MapGet("/api/sla/incidents/export-summary", (
    InMemoryIncidentStore store,
    SlaRuleEngine engine) =>
{
    var summary = engine.BuildShiftExportSummary(store.GetAll());
    return Results.Ok(summary);
});

app.Run();

public partial class Program;
