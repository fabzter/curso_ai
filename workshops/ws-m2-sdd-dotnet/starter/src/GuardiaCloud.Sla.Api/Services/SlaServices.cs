using System.Collections.Concurrent;
using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Services;

public interface IIncidentRepository
{
    Incident Add(Incident incident);
    Incident? GetById(Guid id);
    IReadOnlyCollection<Incident> ListAll();
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
}

public sealed class SlaCalculator(TimeProvider timeProvider)
{
    public SlaStatusResponse Evaluate(Incident incident)
    {
        var targetMinutes = SlaPolicyCatalog.GetTargetMinutes(incident.Priority);

        // NOTA DEL TALLER (para ejercicio /speckit-bug-assess):
        // Este cálculo usa siempre la hora actual en lugar de ResolvedAtUtc cuando el incidente ya fue resuelto.
        var referenceEndUtc = timeProvider.GetUtcNow();

        var elapsedMinutes = Math.Max(0, (referenceEndUtc - incident.OpenedAtUtc).TotalMinutes);
        var remainingMinutes = Math.Round(targetMinutes - elapsedMinutes, 2);
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
            EffectiveDeadlineUtc: effectiveDeadlineUtc,
            IsBreached: isBreached);
    }
}
