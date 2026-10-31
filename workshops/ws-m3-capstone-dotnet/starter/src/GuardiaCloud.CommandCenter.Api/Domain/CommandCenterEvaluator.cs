namespace GuardiaCloud.CommandCenter.Api.Domain;

public sealed class CommandCenterEvaluator(TimeProvider timeProvider)
{
    public static readonly IReadOnlySet<string> AllowedClientTiers = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
    {
        "Bancario-Tier1",
        "Aseguradora-Gold",
        "Retail-Standard"
    };

    private readonly TimeProvider _timeProvider = timeProvider;

    public double CalculateConsumedPercentage(CommandCenterIncident incident)
    {
        var endUtc = incident.ResolvedAtUtc ?? _timeProvider.GetUtcNow();
        var effectiveMinutes = Math.Max(0, (endUtc - incident.OpenedAtUtc).TotalMinutes - incident.PausedMinutes);
        return Math.Round((effectiveMinutes / incident.TargetResolutionMinutes) * 100.0, 2);
    }

    public WebhookProcessingResult ApplyWebhookEvent(
        CommandCenterIncident incident,
        IncidentWebhookEventRequest request)
    {
        // ❌ BUG-301 (Defecto sembrado para el Proyecto Integrador):
        // No verifica si request.EventId ya está en incident.ProcessedWebhookEventIds,
        // por lo que los reintentos de red duplican PausedMinutes y AppliedPenaltyEventsCount.
        incident.PausedMinutes += Math.Max(0, request.AdditionalPausedMinutes);
        if (request.TriggerPenaltyIncrement)
        {
            incident.AppliedPenaltyEventsCount += 1;
        }

        return new WebhookProcessingResult(
            request.EventId,
            incident.IncidentId,
            WasDuplicateIgnored: false,
            incident.PausedMinutes,
            incident.AppliedPenaltyEventsCount);
    }

    // TODO (Módulo 3 - FEAT-301): Implementar EvaluateProactiveEscalation
    // Reglas reveladas en Unidad 3.1:
    // - Si el incidente ya está resuelto (ResolvedAtUtc != null), devolver ShouldDispatchAlert = false ("ALREADY_RESOLVED").
    // - Si ConsumedPercentage < 80.0, devolver ShouldDispatchAlert = false ("BELOW_80_PERCENT_THRESHOLD").
    // - Si LastEscalationSentAtUtc tiene menos de 15 minutos respecto a _timeProvider.GetUtcNow(), devolver ShouldDispatchAlert = false ("COOLDOWN_ACTIVE_15M").
    // - En caso contrario, actualizar incident.LastEscalationSentAtUtc = now y devolver ShouldDispatchAlert = true ("ALERT_DISPATCHED").
    public ProactiveEscalationResult EvaluateProactiveEscalation(CommandCenterIncident incident)
    {
        _ = _timeProvider;
        _ = incident;
        throw new NotImplementedException("TODO (Módulo 3 - FEAT-301): Implementar motor de escalamiento proactivo al 80% con cooldown de 15 min.");
    }

    // TODO (Módulo 3 - FEAT-302): Implementar ApplyForceMajeureExemption
    // Reglas reveladas en Unidad 3.1:
    // - PrimaryApproverEmail y SecondaryApproverEmail deben ser distintos (case-insensitive).
    // - DualApprovalToken debe comenzar con el prefijo "FM-DUAL-".
    // - Registrar ForceMajeureExemption con ApprovedAtUtc = _timeProvider.GetUtcNow().
    public ForceMajeureExemption ApplyForceMajeureExemption(
        CommandCenterIncident incident,
        ForceMajeureExemptionRequest request)
    {
        _ = incident;
        _ = request;
        throw new NotImplementedException("TODO (Módulo 3 - FEAT-302): Implementar aprobación dual de exención por fuerza mayor.");
    }

    // TODO (Módulo 3 - FEAT-303): Implementar BuildTierDashboard
    // Reglas reveladas en Unidad 3.1:
    // - BreachedIncidents: incidentes con ConsumedPercentage > 100.0.
    // - AtRiskIncidents: incidentes con ConsumedPercentage >= 80.0 y <= 100.0.
    // - ExemptedIncidents: incidentes con Exemption != null.
    // - TotalFinancialExposureUsd: suma de PenaltyPerBreachUsd de los incidentes vencidos (ConsumedPercentage > 100.0) que NO tengan Exemption.
    public TierExecutiveDashboardDto BuildTierDashboard(
        string clientTier,
        IReadOnlyList<CommandCenterIncident> tierIncidents)
    {
        _ = clientTier;
        _ = tierIncidents;
        throw new NotImplementedException("TODO (Módulo 3 - FEAT-303): Implementar tablero ejecutivo consolidado por tier.");
    }
}
