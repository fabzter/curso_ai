using GuardiaCloud.CommandCenter.Api.Domain;

namespace GuardiaCloud.CommandCenter.Api.Infrastructure;

public sealed class InMemoryCommandCenterStore
{
    private static readonly DateTimeOffset AnchorUtc = new(2026, 10, 30, 14, 0, 0, TimeSpan.Zero);

    private readonly Dictionary<string, CommandCenterIncident> _incidents = new(StringComparer.OrdinalIgnoreCase)
    {
        ["INC-2026-3001"] = new CommandCenterIncident
        {
            IncidentId = "INC-2026-3001",
            ClientTier = "Bancario-Tier1",
            Severity = "P1",
            OpenedAtUtc = AnchorUtc.AddMinutes(-52), // 52m / 60m = 86.67% (>= 80%, At Risk)
            PausedMinutes = 0,
            TargetResolutionMinutes = 60,
            PenaltyPerBreachUsd = 2500m
        },
        ["INC-2026-3002"] = new CommandCenterIncident
        {
            IncidentId = "INC-2026-3002",
            ClientTier = "Bancario-Tier1",
            Severity = "P1",
            OpenedAtUtc = AnchorUtc.AddMinutes(-90), // 80m / 60m = 133.33% (> 100%, Breached, USD 2500)
            PausedMinutes = 10,
            TargetResolutionMinutes = 60,
            PenaltyPerBreachUsd = 2500m
        },
        ["INC-2026-3003"] = new CommandCenterIncident
        {
            IncidentId = "INC-2026-3003",
            ClientTier = "Bancario-Tier1",
            Severity = "P2",
            OpenedAtUtc = AnchorUtc.AddMinutes(-300), // 280m / 240m = 116.67% (> 100%, Breached, USD 800)
            PausedMinutes = 20,
            TargetResolutionMinutes = 240,
            PenaltyPerBreachUsd = 800m
        }
    };

    public CommandCenterIncident? GetById(string incidentId) =>
        _incidents.TryGetValue(incidentId.Trim(), out var incident) ? incident : null;

    public IReadOnlyList<CommandCenterIncident> GetByTier(string clientTier) =>
        [.. _incidents.Values.Where(i => string.Equals(i.ClientTier, clientTier.Trim(), StringComparison.OrdinalIgnoreCase))];
}
