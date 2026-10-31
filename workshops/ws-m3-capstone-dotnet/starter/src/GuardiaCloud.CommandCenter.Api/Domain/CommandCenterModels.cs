namespace GuardiaCloud.CommandCenter.Api.Domain;

public sealed class CommandCenterIncident
{
    public required string IncidentId { get; init; }
    public required string ClientTier { get; init; }
    public required string Severity { get; init; }
    public required DateTimeOffset OpenedAtUtc { get; init; }
    public DateTimeOffset? ResolvedAtUtc { get; set; }
    public int PausedMinutes { get; set; }
    public int TargetResolutionMinutes { get; init; }
    public decimal PenaltyPerBreachUsd { get; init; }
    public int AppliedPenaltyEventsCount { get; set; }
    public DateTimeOffset? LastEscalationSentAtUtc { get; set; }
    public ForceMajeureExemption? Exemption { get; set; }
    public HashSet<string> ProcessedWebhookEventIds { get; } = new(StringComparer.Ordinal);
}

public sealed record IncidentWebhookEventRequest(
    string EventId,
    string IncidentId,
    int AdditionalPausedMinutes,
    bool TriggerPenaltyIncrement);

public sealed record WebhookProcessingResult(
    string EventId,
    string IncidentId,
    bool WasDuplicateIgnored,
    int TotalPausedMinutes,
    int AppliedPenaltyEventsCount);

public sealed record ProactiveEscalationResult(
    string IncidentId,
    double ConsumedPercentage,
    bool ShouldDispatchAlert,
    string ReasonCode,
    DateTimeOffset EvaluatedAtUtc);

public sealed record ForceMajeureExemptionRequest(
    string IncidentId,
    string ExternalProviderCode,
    string PrimaryApproverEmail,
    string SecondaryApproverEmail,
    string DualApprovalToken);

public sealed record ForceMajeureExemption(
    string IncidentId,
    string ExternalProviderCode,
    string PrimaryApproverEmail,
    string SecondaryApproverEmail,
    DateTimeOffset ApprovedAtUtc);

public sealed record TierExecutiveDashboardDto(
    string ClientTier,
    int TotalIncidents,
    int BreachedIncidents,
    int AtRiskIncidents,
    int ExemptedIncidents,
    decimal TotalFinancialExposureUsd,
    DateTimeOffset GeneratedAtUtc);
