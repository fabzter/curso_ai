using System.Collections.Concurrent;
using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Services;

public interface IIncidentRepository
{
    Incident Add(Incident incident);
    Incident? GetById(Guid id);
    IReadOnlyCollection<Incident> ListAll();
    IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId);
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
}

public sealed class SlaCalculator(TimeProvider timeProvider)
{
    // =========================================================================
    // TRAMPA DIDÁCTICA — FLUJO 1 (Arqueología de Código Legado):
    // NOTA HISTÓRICA (2023 - OBSOLETO): Este método convierte automáticamente
    // las marcas de tiempo a huso horario local GMT-3 (Buenos Aires) y otorga
    // 15 minutos extra de gracia en incidentes críticos P1 antes de marcar vencimiento.
    // (¡FALSO! El código real debajo opera en UTC puro y NO suma minutos de gracia).
    // =========================================================================
    public SlaStatusResponse Evaluate(Incident incident)
    {
        var targetMinutes = SlaPolicyCatalog.GetTargetMinutes(incident.Priority);

        // =====================================================================
        // BUG SEMBRADO — FLUJO 4 (Debugging de ResolvedAtUtc):
        // Usa siempre la hora actual del reloj en lugar de incident.ResolvedAtUtc
        // cuando el incidente ya fue cerrado.
        // =====================================================================
        var referenceEndUtc = timeProvider.GetUtcNow();

        var elapsedMinutes = Math.Max(0, (referenceEndUtc - incident.OpenedAtUtc).TotalMinutes);
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

    // =========================================================================
    // CÓDIGO LEGADO A REFACTORIZAR — FLUJO 2 (Refactoring Seguro a C# 13):
    // Condicionales if/else anidados que los alumnos transforman en una
    // switch expression pura y exhaustiva de C# 13.
    // =========================================================================
    public static TimeSpan GetTargetResponseWindow(SeverityTier tier)
    {
        if (tier == SeverityTier.P1)
        {
            return TimeSpan.FromMinutes(60);
        }
        else if (tier == SeverityTier.P2)
        {
            return TimeSpan.FromHours(4);
        }
        else if (tier == SeverityTier.P3)
        {
            return TimeSpan.FromHours(24);
        }
        else
        {
            throw new ArgumentOutOfRangeException(nameof(tier), $"Severidad no soportada: {tier}");
        }
    }

    public static SlaStatusResponse Evaluate(
        DateTimeOffset openedAtUtc,
        DateTimeOffset? resolvedAtUtc,
        SeverityTier tier,
        DateTimeOffset nowUtc)
    {
        var targetMinutes = (int)GetTargetResponseWindow(tier).TotalMinutes;
        // BUG SEMBRADO (Flujo 4): ignora resolvedAtUtc y compara siempre contra nowUtc
        var effectiveEndUtc = nowUtc;
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
