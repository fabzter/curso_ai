namespace GuardiaCloud.Sla.Api.Domain;

public enum IncidentPriority
{
    CriticalP1 = 1,
    HighP2 = 2,
    StandardP3 = 3
}

public enum IncidentStatus
{
    Open = 1,
    InProgress = 2,
    Resolved = 3,
    WaitingForCustomer = 4
}

public enum SlaPauseReason
{
    WaitingForCustomerLogs = 1,
    WaitingForCustomerVpnAccess = 2,
    WaitingForCustomerValidation = 3
}

public static class SlaPolicyCatalog
{
    public const int CriticalP1StandardPauseBudgetMinutes = 30;

    public static int GetTargetMinutes(IncidentPriority priority) => priority switch
    {
        IncidentPriority.CriticalP1 => 60,
        IncidentPriority.HighP2 => 240,
        IncidentPriority.StandardP3 => 1440,
        _ => throw new ArgumentOutOfRangeException(nameof(priority), $"Prioridad no soportada: {priority}")
    };

    public static int? GetMaxPauseBudgetMinutes(IncidentPriority priority) => priority switch
    {
        IncidentPriority.CriticalP1 => CriticalP1StandardPauseBudgetMinutes,
        _ => null
    };
}

public sealed class SlaPauseWindow
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public required SlaPauseReason Reason { get; init; }
    public required string RequestedBy { get; init; }
    public required string EvidenceNote { get; init; }
    public string? SupervisorOverrideCode { get; init; }
    public required DateTimeOffset PausedAtUtc { get; init; }
    public DateTimeOffset? ResumedAtUtc { get; set; }
    public string? ResumedBy { get; set; }

    public bool IsActive => ResumedAtUtc is null;

    public double GetDurationMinutes(DateTimeOffset evaluationPointUtc)
    {
        var end = ResumedAtUtc ?? evaluationPointUtc;
        if (end <= PausedAtUtc)
        {
            return 0;
        }

        return (end - PausedAtUtc).TotalMinutes;
    }
}

public sealed class Incident
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public required string TenantId { get; init; }
    public required string Title { get; init; }
    public required IncidentPriority Priority { get; init; }
    public IncidentStatus Status { get; set; } = IncidentStatus.Open;
    public required DateTimeOffset OpenedAtUtc { get; init; }
    public DateTimeOffset? ResolvedAtUtc { get; set; }
    public List<SlaPauseWindow> PauseWindows { get; } = [];
}

public sealed record CreateIncidentRequest(
    string TenantId,
    string Title,
    IncidentPriority Priority,
    DateTimeOffset? OpenedAtUtc = null);

public sealed record ResolveIncidentRequest(
    DateTimeOffset? ResolvedAtUtc = null,
    string? ResolutionSummary = null);

public sealed record PauseSlaRequest(
    SlaPauseReason Reason,
    string RequestedBy,
    string EvidenceNote,
    string? SupervisorOverrideCode = null,
    DateTimeOffset? PausedAtUtc = null);

public sealed record ResumeSlaRequest(
    string ResumedBy,
    DateTimeOffset? ResumedAtUtc = null);

public sealed record SlaStatusResponse(
    Guid IncidentId,
    string TenantId,
    IncidentPriority Priority,
    IncidentStatus Status,
    int TargetResolutionMinutes,
    double ElapsedActiveMinutes,
    double TotalPausedMinutes,
    double? RemainingPauseBudgetMinutes,
    double RemainingMinutes,
    DateTimeOffset EffectiveDeadlineUtc,
    bool IsBreached,
    int PauseCount);
