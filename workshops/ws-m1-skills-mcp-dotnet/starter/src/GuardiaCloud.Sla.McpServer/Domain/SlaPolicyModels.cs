namespace GuardiaCloud.Sla.McpServer.Domain;

public sealed record ClientSlaPolicy(
    string ClientTier,
    string Severity,
    int TargetResolutionMinutes,
    int MaxAllowedPauseMinutes,
    decimal PenaltyPerHourUsd,
    string EscalationChannel);

public sealed record IncidentRecord(
    string IncidentId,
    string ClientTier,
    string Severity,
    DateTimeOffset OpenedAtUtc,
    DateTimeOffset? ResolvedAtUtc,
    int AccumulatedPauseMinutes,
    string Summary);

public sealed record IncidentSlaAuditDto(
    string IncidentId,
    string ClientTier,
    string Severity,
    double EffectiveElapsedMinutes,
    int TargetResolutionMinutes,
    double ConsumedPercentage,
    string Status,
    bool IsBreached,
    bool IsAtRisk,
    string SanitizedSummary,
    string RecommendedAction);

public sealed record Rfc9457ValidationResult(
    bool IsValid,
    string ErrorCode,
    int ExpectedHttpStatus,
    string ExpectedTypeUri,
    IReadOnlyList<string> Violations);
