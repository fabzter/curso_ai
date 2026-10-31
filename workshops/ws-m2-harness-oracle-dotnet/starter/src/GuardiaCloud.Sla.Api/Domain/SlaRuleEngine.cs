namespace GuardiaCloud.Sla.Api.Domain;

public sealed class SlaRuleEngine(TimeProvider timeProvider)
{
    private readonly TimeProvider _timeProvider = timeProvider;

    public bool IsIncidentBreached(IncidentEntry incident)
    {
        var endUtc = incident.ResolvedAtUtc ?? _timeProvider.GetUtcNow();
        var effectiveMinutes = Math.Max(0, (endUtc - incident.OpenedAtUtc).TotalMinutes - incident.PausedMinutes);
        return effectiveMinutes > incident.TargetResolutionMinutes;
    }

    // TODO (Fase 3A - Modo Human-in-the-Loop):
    // Calcular la bonificación mensual por incidentes vencidos:
    // - Cada incidente vencido bonifica: P1 = 10% de MonthlyInvoiceUsd, P2 = 5%, P3 = 2%.
    // - La bonificación total mensual NO puede superar el tope contractual (30% para Bancario-Tier1, 20% para otros tiers).
    // - Redondear a 2 decimales con MidpointRounding.ToEven.
    public SlaCreditCalculationResult CalculateMonthlyCredit(
        string clientTier,
        decimal monthlyInvoiceUsd,
        IReadOnlyList<IncidentEntry> incidents)
    {
        _ = clientTier;
        _ = monthlyInvoiceUsd;
        _ = incidents;
        throw new NotImplementedException("TODO (Fase 3A - Modo HITL): Implementar cálculo financiero de créditos SLA.");
    }

    // TODO (Fase 3B - Modo Full AI Autónomo en git worktree):
    // Construir el resumen operativo de guardia (ShiftExportSummaryDto) usando _timeProvider.GetUtcNow().
    public ShiftExportSummaryDto BuildShiftExportSummary(IReadOnlyList<IncidentEntry> incidents)
    {
        _ = incidents;
        throw new NotImplementedException("TODO (Fase 3B - Modo Full AI): Implementar exportación de resumen de guardia.");
    }
}
