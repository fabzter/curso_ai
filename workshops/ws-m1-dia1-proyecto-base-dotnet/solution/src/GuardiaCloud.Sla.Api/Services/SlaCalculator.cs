using System.Collections.Concurrent;
using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Services;

public interface IIncidentRepository
{
    Incident Add(Incident incident);
    Incident? GetById(Guid id);
    IReadOnlyCollection<Incident> ListAll();
    IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId);
    IReadOnlyDictionary<Guid, IReadOnlyList<string>> GetAuditLogsBatch(IEnumerable<Guid> incidentIds);
}

public sealed class InMemoryIncidentRepository : IIncidentRepository
{
    private readonly ConcurrentDictionary<Guid, Incident> _store = new();

    public Incident Add(Incident incident)
    {
        _store[incident.Id] = incident;
        return incident;
    }

    public Incident? GetById(Guid id) =>
        _store.TryGetValue(id, out var incident) ? incident : null;

    public IReadOnlyCollection<Incident> ListAll() =>
        _store.Values.OrderByDescending(i => i.OpenedAtUtc).ToArray();

    public IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId) =>
        [$"AUDIT-OPENED:{incidentId}", $"AUDIT-MONITORED:{incidentId}"];

    public IReadOnlyDictionary<Guid, IReadOnlyList<string>> GetAuditLogsBatch(IEnumerable<Guid> incidentIds) =>
        incidentIds.Distinct().ToDictionary(
            id => id,
            id => (IReadOnlyList<string>)[$"AUDIT-OPENED:{id}", $"AUDIT-MONITORED:{id}"]);
}

/// <summary>
/// Calculador determinista de SLA en UTC (Flujo 1: comentario engañoso eliminado;
/// Flujo 2: switch expression C# 13; Flujo 4: fix de ResolvedAtUtc).
/// </summary>
public sealed class SlaCalculator(TimeProvider timeProvider)
{
    public SlaStatusResponse Evaluate(Incident incident)
    {
        var targetMinutes = SlaPolicyCatalog.GetTargetMinutes(incident.Priority);

        // FIX FLUJO 4: Si el incidente ya está resuelto, el reloj de SLA se detiene en ResolvedAtUtc.
        var effectiveEndUtc = incident.ResolvedAtUtc ?? timeProvider.GetUtcNow();

        var elapsedMinutes = Math.Max(0, (effectiveEndUtc - incident.OpenedAtUtc).TotalMinutes);
        var remainingMinutes = Math.Round(targetMinutes - elapsedMinutes, 2);
        var consumedRatio = Math.Round(elapsedMinutes / targetMinutes, 4);
        var effectiveDeadlineUtc = incident.OpenedAtUtc.AddMinutes(targetMinutes);
        var isBreached = elapsedMinutes > targetMinutes;

        return new SlaStatusResponse(
            IncidentId: incident.Id,
            TenantId: incident.TenantId,
            Priority: incident.Priority,
            Status: incident.Status,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: remainingMinutes,
            ConsumedRatio: consumedRatio,
            EffectiveDeadlineUtc: effectiveDeadlineUtc,
            IsBreached: isBreached);
    }

    // FIX FLUJO 2: Switch expression pura y exhaustiva de C# 13
    public static TimeSpan GetTargetResponseWindow(SeverityTier tier) => tier switch
    {
        SeverityTier.P1 => TimeSpan.FromMinutes(60),
        SeverityTier.P2 => TimeSpan.FromHours(4),
        SeverityTier.P3 => TimeSpan.FromHours(24),
        _ => throw new ArgumentOutOfRangeException(nameof(tier), $"Severidad no soportada: {tier}")
    };

    public static SlaStatusResponse Evaluate(
        DateTimeOffset openedAtUtc,
        DateTimeOffset? resolvedAtUtc,
        SeverityTier tier,
        DateTimeOffset nowUtc)
    {
        var targetMinutes = (int)GetTargetResponseWindow(tier).TotalMinutes;
        // FIX FLUJO 4: Usa resolvedAtUtc cuando el incidente está cerrado
        var effectiveEndUtc = resolvedAtUtc ?? nowUtc;
        var elapsedMinutes = Math.Max(0, (effectiveEndUtc - openedAtUtc).TotalMinutes);

        return new SlaStatusResponse(
            IncidentId: Guid.Empty,
            TenantId: "default-tenant",
            Priority: (IncidentPriority)(int)tier,
            Status: resolvedAtUtc.HasValue ? IncidentStatus.Resolved : IncidentStatus.Open,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: Math.Round(targetMinutes - elapsedMinutes, 2),
            ConsumedRatio: Math.Round(elapsedMinutes / targetMinutes, 4),
            EffectiveDeadlineUtc: openedAtUtc.AddMinutes(targetMinutes),
            IsBreached: elapsedMinutes > targetMinutes);
    }
}
