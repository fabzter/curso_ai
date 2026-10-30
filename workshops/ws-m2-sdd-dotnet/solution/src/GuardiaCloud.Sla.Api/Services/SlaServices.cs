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

        // FIX (/speckit-bug-fix): Cuando el incidente está resuelto, el reloj se congela en ResolvedAtUtc.
        var referenceEndUtc = incident.Status == IncidentStatus.Resolved && incident.ResolvedAtUtc.HasValue
            ? incident.ResolvedAtUtc.Value
            : timeProvider.GetUtcNow();

        var totalWallClockMinutes = Math.Max(0, (referenceEndUtc - incident.OpenedAtUtc).TotalMinutes);

        // Spec 001 + OpenSpec cap-p1-pause-budget:
        // Calculamos el tiempo total en pausa y aplicamos el tope de 30 min en P1 salvo SupervisorOverrideCode válido.
        var rawPausedMinutes = incident.PauseWindows.Sum(w => w.GetDurationMinutes(referenceEndUtc));
        var hasSupervisorOverride = incident.PauseWindows.Any(w => !string.IsNullOrWhiteSpace(w.SupervisorOverrideCode));
        var maxBudget = SlaPolicyCatalog.GetMaxPauseBudgetMinutes(incident.Priority);

        var creditedPausedMinutes = maxBudget.HasValue && !hasSupervisorOverride
            ? Math.Min(rawPausedMinutes, maxBudget.Value)
            : rawPausedMinutes;

        double? remainingPauseBudgetMinutes = maxBudget.HasValue && !hasSupervisorOverride
            ? Math.Round(Math.Max(0, maxBudget.Value - creditedPausedMinutes), 2)
            : null;

        var elapsedActiveMinutes = Math.Max(0, totalWallClockMinutes - creditedPausedMinutes);
        var remainingMinutes = Math.Round(targetMinutes - elapsedActiveMinutes, 2);
        var effectiveDeadlineUtc = incident.OpenedAtUtc.AddMinutes(targetMinutes + creditedPausedMinutes);
        var isBreached = elapsedActiveMinutes > targetMinutes;

        return new SlaStatusResponse(
            IncidentId: incident.Id,
            TenantId: incident.TenantId,
            Priority: incident.Priority,
            Status: incident.Status,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedActiveMinutes, 2),
            TotalPausedMinutes: Math.Round(creditedPausedMinutes, 2),
            RemainingPauseBudgetMinutes: remainingPauseBudgetMinutes,
            RemainingMinutes: remainingMinutes,
            EffectiveDeadlineUtc: effectiveDeadlineUtc,
            IsBreached: isBreached,
            PauseCount: incident.PauseWindows.Count);
    }
}
