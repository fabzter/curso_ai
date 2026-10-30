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
    Resolved = 3
}

public static class SlaPolicyCatalog
{
    public static int GetTargetMinutes(IncidentPriority priority) => priority switch
    {
        IncidentPriority.CriticalP1 => 60,
        IncidentPriority.HighP2 => 240,
        IncidentPriority.StandardP3 => 1440,
        _ => throw new ArgumentOutOfRangeException(nameof(priority), $"Prioridad no soportada: {priority}")
    };
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
}

public sealed record CreateIncidentRequest(
    string TenantId,
    string Title,
    IncidentPriority Priority,
    DateTimeOffset? OpenedAtUtc = null);

public sealed record ResolveIncidentRequest(
    DateTimeOffset? ResolvedAtUtc = null,
    string? ResolutionSummary = null);

public sealed record SlaStatusResponse(
    Guid IncidentId,
    string TenantId,
    IncidentPriority Priority,
    IncidentStatus Status,
    int TargetResolutionMinutes,
    double ElapsedActiveMinutes,
    double RemainingMinutes,
    DateTimeOffset EffectiveDeadlineUtc,
    bool IsBreached);
