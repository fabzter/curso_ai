namespace GuardiaCloud.Sla.Api.Domain;

public sealed class SlaRuleEngine(TimeProvider timeProvider)
{
    public static readonly IReadOnlySet<string> AllowedClientTiers = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
    {
        "Bancario-Tier1",
        "Aseguradora-Gold",
        "Retail-Standard"
    };

    private readonly TimeProvider _timeProvider = timeProvider;

    public bool IsIncidentBreached(IncidentEntry incident)
    {
        var endUtc = incident.ResolvedAtUtc ?? _timeProvider.GetUtcNow();
        var effectiveMinutes = Math.Max(0, (endUtc - incident.OpenedAtUtc).TotalMinutes - incident.PausedMinutes);
        return effectiveMinutes > incident.TargetResolutionMinutes;
    }

    public SlaCreditCalculationResult CalculateMonthlyCredit(
        string clientTier,
        decimal monthlyInvoiceUsd,
        IReadOnlyList<IncidentEntry> incidents)
    {
        var breachedIncidents = incidents.Where(IsIncidentBreached).ToList();

        var rawPercentage = 0m;
        foreach (var incident in breachedIncidents)
        {
            rawPercentage += incident.Severity.ToUpperInvariant() switch
            {
                "P1" => 0.10m,
                "P2" => 0.05m,
                "P3" => 0.02m,
                _ => 0m
            };
        }

        var capPercentage = string.Equals(clientTier?.Trim(), "Bancario-Tier1", StringComparison.OrdinalIgnoreCase)
            ? 0.30m
            : 0.20m;

        var rawCreditUsd = decimal.Round(monthlyInvoiceUsd * rawPercentage, 2, MidpointRounding.ToEven);
        var maxCreditUsd = decimal.Round(monthlyInvoiceUsd * capPercentage, 2, MidpointRounding.ToEven);
        var cappedCreditUsd = Math.Min(rawCreditUsd, maxCreditUsd);

        return new SlaCreditCalculationResult(
            clientTier?.Trim() ?? string.Empty,
            breachedIncidents.Count,
            rawCreditUsd,
            cappedCreditUsd,
            capPercentage * 100m,
            rawCreditUsd > maxCreditUsd);
    }

    public ShiftExportSummaryDto BuildShiftExportSummary(IReadOnlyList<IncidentEntry> incidents)
    {
        var countBySeverity = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
        {
            ["P1"] = 0,
            ["P2"] = 0,
            ["P3"] = 0
        };

        var openCount = 0;
        var breachedCount = 0;

        foreach (var incident in incidents)
        {
            if (!incident.ResolvedAtUtc.HasValue)
            {
                openCount++;
            }

            if (IsIncidentBreached(incident))
            {
                breachedCount++;
            }

            var sevKey = incident.Severity.ToUpperInvariant();
            countBySeverity[sevKey] = countBySeverity.GetValueOrDefault(sevKey) + 1;
        }

        return new ShiftExportSummaryDto(
            _timeProvider.GetUtcNow(),
            incidents.Count,
            openCount,
            breachedCount,
            countBySeverity);
    }
}
