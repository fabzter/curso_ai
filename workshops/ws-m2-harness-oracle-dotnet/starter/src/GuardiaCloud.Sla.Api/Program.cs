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

// TODO (Fase 3A - Modo HITL): Exponer POST /api/sla/credits/calculate validando MonthlyInvoiceUsd > 0 con ProblemDetails RFC 9457 (SLA-400-INVALID-INVOICE-AMOUNT)
// TODO (Fase 3B - Modo Full AI): Exponer GET /api/sla/incidents/export-summary devolviendo ShiftExportSummaryDto

app.Run();

public partial class Program;
