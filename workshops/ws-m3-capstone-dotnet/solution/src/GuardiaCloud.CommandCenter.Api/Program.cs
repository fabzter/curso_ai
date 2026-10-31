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

app.MapPost("/api/command-center/escalations/evaluate/{incidentId}", (
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

    return Results.Ok(evaluator.EvaluateProactiveEscalation(incident));
});

app.MapPost("/api/command-center/exemptions", (
    ForceMajeureExemptionRequest request,
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

    if (string.IsNullOrWhiteSpace(request.PrimaryApproverEmail) ||
        string.IsNullOrWhiteSpace(request.SecondaryApproverEmail) ||
        string.Equals(request.PrimaryApproverEmail.Trim(), request.SecondaryApproverEmail.Trim(), StringComparison.OrdinalIgnoreCase))
    {
        return Results.Problem(
            title: "Violación de control dual de aprobadores",
            detail: "PrimaryApproverEmail y SecondaryApproverEmail deben corresponder a dos responsables distintos.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://errors.guardiacloud.internal/command-center/same-approver",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "CC-400-SAME-APPROVER" });
    }

    if (string.IsNullOrWhiteSpace(request.DualApprovalToken) ||
        !request.DualApprovalToken.Trim().StartsWith("FM-DUAL-", StringComparison.Ordinal))
    {
        return Results.Problem(
            title: "Token de aprobación dual inválido",
            detail: "El token DualApprovalToken debe poseer el prefijo criptográfico 'FM-DUAL-'.",
            statusCode: StatusCodes.Status422UnprocessableEntity,
            type: "https://errors.guardiacloud.internal/command-center/invalid-dual-token",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "CC-422-INVALID-DUAL-TOKEN" });
    }

    return Results.Ok(evaluator.ApplyForceMajeureExemption(incident, request));
});

app.MapGet("/api/command-center/dashboard/{clientTier}", (
    string clientTier,
    InMemoryCommandCenterStore store,
    CommandCenterEvaluator evaluator) =>
{
    if (string.IsNullOrWhiteSpace(clientTier) ||
        !CommandCenterEvaluator.AllowedClientTiers.Contains(clientTier.Trim()))
    {
        return Results.Problem(
            title: "Tier de cliente inválido",
            detail: $"El tier '{clientTier}' no pertenece al catálogo oficial.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://errors.guardiacloud.internal/command-center/invalid-client-tier",
            extensions: new Dictionary<string, object?> { ["errorCode"] = "CC-400-INVALID-CLIENT-TIER" });
    }

    var incidents = store.GetByTier(clientTier);
    return Results.Ok(evaluator.BuildTierDashboard(clientTier, incidents));
});

app.Run();

public partial class Program;
