namespace GuardiaCloud.Sla.Api.Domain;

/// <summary>
/// Prioridad operativa del incidente (compatible con la nomenclatura P1/P2/P3 de los slides).
/// </summary>
public enum IncidentPriority
{
    CriticalP1 = 1,
    HighP2 = 2,
    StandardP3 = 3,
    P1 = CriticalP1,
    P2 = HighP2,
    P3 = StandardP3
}

/// <summary>
/// Alias semántico usado en las slides de las Unidades 1.1 y 1.2 (SeverityTier.P1, P2, P3).
/// </summary>
public enum SeverityTier
{
    P1 = 1,
    P2 = 2,
    P3 = 3
}

public enum ClientTier
{
    Platinum = 1,
    Gold = 2,
    Silver = 3
}

public enum IncidentStatus
{
    Open = 1,
    InProgress = 2,
    Resolved = 3
}

public enum PauseReason
{
    WaitingForCustomer = 1,
    MaintenanceWindow = 2
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
    public string Code { get; init; } = "INC-2026-1001";
    public required string TenantId { get; init; }
    public required string Title { get; init; }
    public required IncidentPriority Priority { get; init; }
    public ClientTier Tier { get; init; } = ClientTier.Platinum;
    public IncidentStatus Status { get; set; } = IncidentStatus.Open;
    public required DateTimeOffset OpenedAtUtc { get; init; }
    public DateTimeOffset? ResolvedAtUtc { get; set; }
}

public sealed record PauseWindowDto(
    PauseReason Reason,
    DateTimeOffset StartsAtUtc,
    DateTimeOffset EndsAtUtc);

/// <summary>
/// Contrato DTO exacto utilizado en la Unidad 1.1 (Diseño UI con IA + Handoff a Blazor / OpenAPI).
/// </summary>
public sealed record IncidentSlaSummaryDto(
    string IncidentId,
    string ClientTier,
    string Severity,
    double ConsumedRatio,
    bool IsBreached,
    DateTimeOffset DeadlineUtc,
    IReadOnlyList<PauseWindowDto> PauseWindows);

/// <summary>
/// Modelo tipado para el componente Blazor SlaStatusCard.razor (Unidad 1.1 Paso 3).
/// </summary>
public sealed record IncidentSlaCardDto(
    string IncidentId,
    string ClientTier,
    string Severity,
    double ConsumedRatio,
    bool IsBreached,
    DateTimeOffset DeadlineUtc,
    IReadOnlyList<PauseWindowDto> PauseWindows)
{
    public bool IsAtRisk80Percent => ConsumedRatio >= 0.80 && !IsBreached;
}

public sealed record CreateIncidentRequest(
    string TenantId,
    string Title,
    IncidentPriority Priority,
    DateTimeOffset? OpenedAtUtc = null,
    ClientTier Tier = ClientTier.Platinum);

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
    double ConsumedRatio,
    DateTimeOffset EffectiveDeadlineUtc,
    bool IsBreached);
