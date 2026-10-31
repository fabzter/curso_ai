using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Infrastructure;

public sealed class InMemoryIncidentStore
{
    private static readonly DateTimeOffset AnchorUtc = new(2026, 10, 30, 14, 0, 0, TimeSpan.Zero);

    private readonly Dictionary<string, IncidentEntry> _incidents = new(StringComparer.OrdinalIgnoreCase)
    {
        ["INC-2026-1001"] = new("INC-2026-1001", "Bancario-Tier1", "P1", AnchorUtc.AddMinutes(-90), AnchorUtc.AddMinutes(-10), 10, 60), // 70m > 60m => Breached (10%)
        ["INC-2026-1002"] = new("INC-2026-1002", "Bancario-Tier1", "P1", AnchorUtc.AddMinutes(-120), AnchorUtc.AddMinutes(-20), 5, 60), // 95m > 60m => Breached (10%)
        ["INC-2026-1003"] = new("INC-2026-1003", "Bancario-Tier1", "P2", AnchorUtc.AddMinutes(-300), null, 20, 240),                    // 280m > 240m => Breached (5%)
        ["INC-2026-1004"] = new("INC-2026-1004", "Bancario-Tier1", "P1", AnchorUtc.AddMinutes(-40), null, 5, 60),                       // 35m <= 60m => Healthy (0%)
        ["INC-2026-1005"] = new("INC-2026-1005", "Bancario-Tier1", "P1", AnchorUtc.AddMinutes(-150), AnchorUtc.AddMinutes(-30), 0, 60)  // 120m > 60m => Breached (10%)
    };

    public IncidentEntry? GetById(string incidentId) =>
        _incidents.TryGetValue(incidentId.Trim(), out var entry) ? entry : null;

    public IReadOnlyList<IncidentEntry> GetAll() => [.. _incidents.Values];
}
