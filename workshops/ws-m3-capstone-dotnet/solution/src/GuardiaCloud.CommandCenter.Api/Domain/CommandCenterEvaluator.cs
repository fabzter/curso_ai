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
        var normalizedEventId = request.EventId?.Trim() ?? string.Empty;
        if (!incident.ProcessedWebhookEventIds.Add(normalizedEventId))
        {
            return new WebhookProcessingResult(
                normalizedEventId,
                incident.IncidentId,
                WasDuplicateIgnored: true,
                incident.PausedMinutes,
                incident.AppliedPenaltyEventsCount);
        }

        incident.PausedMinutes += Math.Max(0, request.AdditionalPausedMinutes);
        if (request.TriggerPenaltyIncrement)
        {
            incident.AppliedPenaltyEventsCount += 1;
        }

        return new WebhookProcessingResult(
            normalizedEventId,
            incident.IncidentId,
            WasDuplicateIgnored: false,
            incident.PausedMinutes,
            incident.AppliedPenaltyEventsCount);
    }

    public ProactiveEscalationResult EvaluateProactiveEscalation(CommandCenterIncident incident)
    {
        var nowUtc = _timeProvider.GetUtcNow();
        var consumedPercentage = CalculateConsumedPercentage(incident);

        if (incident.ResolvedAtUtc.HasValue)
        {
            return new ProactiveEscalationResult(
                incident.IncidentId,
                consumedPercentage,
                ShouldDispatchAlert: false,
                "ALREADY_RESOLVED",
                nowUtc);
        }

        if (consumedPercentage < 80.0)
        {
            return new ProactiveEscalationResult(
                incident.IncidentId,
                consumedPercentage,
                ShouldDispatchAlert: false,
                "BELOW_80_PERCENT_THRESHOLD",
                nowUtc);
        }

        if (incident.LastEscalationSentAtUtc.HasValue &&
            (nowUtc - incident.LastEscalationSentAtUtc.Value).TotalMinutes < 15.0)
        {
            return new ProactiveEscalationResult(
                incident.IncidentId,
                consumedPercentage,
                ShouldDispatchAlert: false,
                "COOLDOWN_ACTIVE_15M",
                nowUtc);
        }

        incident.LastEscalationSentAtUtc = nowUtc;
        return new ProactiveEscalationResult(
            incident.IncidentId,
            consumedPercentage,
            ShouldDispatchAlert: true,
            "ALERT_DISPATCHED",
            nowUtc);
    }

    public ForceMajeureExemption ApplyForceMajeureExemption(
        CommandCenterIncident incident,
        ForceMajeureExemptionRequest request)
    {
        var exemption = new ForceMajeureExemption(
            incident.IncidentId,
            request.ExternalProviderCode.Trim(),
            request.PrimaryApproverEmail.Trim(),
            request.SecondaryApproverEmail.Trim(),
            _timeProvider.GetUtcNow());

        incident.Exemption = exemption;
        return exemption;
    }

    public TierExecutiveDashboardDto BuildTierDashboard(
        string clientTier,
        IReadOnlyList<CommandCenterIncident> tierIncidents)
    {
        var breached = 0;
        var atRisk = 0;
        var exempted = 0;
        var exposureUsd = 0m;

        foreach (var incident in tierIncidents)
        {
            var consumed = CalculateConsumedPercentage(incident);
            var isBreached = consumed > 100.0;
            var isAtRisk = !isBreached && consumed >= 80.0;

            if (isBreached)
            {
                breached++;
                if (incident.Exemption is null)
                {
                    exposureUsd += incident.PenaltyPerBreachUsd;
                }
            }
            else if (isAtRisk)
            {
                atRisk++;
            }

            if (incident.Exemption is not null)
            {
                exempted++;
            }
        }

        return new TierExecutiveDashboardDto(
            clientTier.Trim(),
            tierIncidents.Count,
            breached,
            atRisk,
            exempted,
            decimal.Round(exposureUsd, 2, MidpointRounding.ToEven),
            _timeProvider.GetUtcNow());
    }
}
