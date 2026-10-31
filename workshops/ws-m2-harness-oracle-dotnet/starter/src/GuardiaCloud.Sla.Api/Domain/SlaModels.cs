namespace GuardiaCloud.Sla.Api.Domain;

public sealed record IncidentEntry(
    string IncidentId,
    string ClientTier,
    string Severity,
    DateTimeOffset OpenedAtUtc,
    DateTimeOffset? ResolvedAtUtc,
    int PausedMinutes,
    int TargetResolutionMinutes);

public sealed record SlaCreditCalculationRequest(
    string ClientTier,
    decimal MonthlyInvoiceUsd,
    IReadOnlyList<string> IncidentIds);

public sealed record SlaCreditCalculationResult(
    string ClientTier,
    int BreachedIncidentsCount,
    decimal RawCreditUsd,
    decimal CappedCreditUsd,
    decimal AppliedCapPercentage,
    bool WasCapped);

public sealed record ShiftExportSummaryDto(
    DateTimeOffset GeneratedAtUtc,
    int TotalIncidents,
    int OpenIncidents,
    int BreachedIncidents,
    IReadOnlyDictionary<string, int> CountBySeverity);
