using GuardiaCloud.CommandCenter.Api.Domain;
using GuardiaCloud.CommandCenter.Api.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton(TimeProvider.System);
builder.Services.AddSingleton<InMemoryCommandCenterStore>();
builder.Services.AddSingleton<CommandCenterEvaluator>();
builder.Services.AddProblemDetails();

var app = builder.Build();

app.MapGet("/api/command-center/incidents/{incidentId}", (
    string incidentId,
    InMemoryCommandCenterStore store,
    CommandCenterEvaluator evaluator) =>
{
    var incident = store.GetById(incidentId);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe el incidente '{incidentId}'.",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://errors.guardiacloud.internal/command-center/incident-not-found",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "CC-404-INCIDENT-NOT-FOUND" });
    }

    return Results.Ok(new
    {
        incident.IncidentId,
        incident.ClientTier,
        incident.Severity,
        ConsumedPercentage = evaluator.CalculateConsumedPercentage(incident)
    });
});

app.MapPost("/api/command-center/webhooks/incident-event", (
    IncidentWebhookEventRequest request,
    InMemoryCommandCenterStore store,
    CommandCenterEvaluator evaluator) =>
{
    var incident = store.GetById(request.IncidentId);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe el incidente '{request.IncidentId}'.",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://errors.guardiacloud.internal/command-center/incident-not-found",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "CC-404-INCIDENT-NOT-FOUND" });
    }

    return Results.Ok(evaluator.ApplyWebhookEvent(incident, request));
});

// TODO (Módulo 3 - FEAT-301): Exponer POST /api/command-center/escalations/evaluate/{incidentId}
// TODO (Módulo 3 - FEAT-302): Exponer POST /api/command-center/exemptions (con validaciones RFC 9457: CC-400-SAME-APPROVER y CC-422-INVALID-DUAL-TOKEN)
// TODO (Módulo 3 - FEAT-303): Exponer GET /api/command-center/dashboard/{clientTier} (con validación RFC 9457: CC-400-INVALID-CLIENT-TIER)

app.Run();

public partial class Program;
