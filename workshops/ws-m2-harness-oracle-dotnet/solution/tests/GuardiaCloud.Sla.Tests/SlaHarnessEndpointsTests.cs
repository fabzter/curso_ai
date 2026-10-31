using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using GuardiaCloud.Sla.Api.Domain;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Xunit;

namespace GuardiaCloud.Sla.Tests;

public sealed class SlaHarnessEndpointsTests(WebApplicationFactory<Program> factory)
    : IClassFixture<WebApplicationFactory<Program>>
{
    private static readonly DateTimeOffset FixedNowUtc = new(2026, 10, 30, 14, 0, 0, TimeSpan.Zero);

    private readonly WebApplicationFactory<Program> _factory = factory.WithWebHostBuilder(builder =>
    {
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<TimeProvider>();
            services.AddSingleton<TimeProvider>(new FixedTimeProvider(FixedNowUtc));
        });
    });

    [Fact]
    public async Task GetIncident_ReturnsOkForSeededIncident()
    {
        using var client = _factory.CreateClient();

        var response = await client.GetAsync("/api/sla/incidents/INC-2026-1001");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task CalculateCredits_AppliesTier1CapAtThirtyPercent()
    {
        using var client = _factory.CreateClient();

        // INC-2026-1001 (P1=10%), INC-2026-1002 (P1=10%), INC-2026-1003 (P2=5%), INC-2026-1005 (P1=10%) => 35% bruto, topeado a 30% en Bancario-Tier1
        var request = new SlaCreditCalculationRequest(
            "Bancario-Tier1",
            10000m,
            ["INC-2026-1001", "INC-2026-1002", "INC-2026-1003", "INC-2026-1005"]);

        var response = await client.PostAsJsonAsync("/api/sla/credits/calculate", request);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var payload = await response.Content.ReadFromJsonAsync<SlaCreditCalculationResult>();
        Assert.NotNull(payload);
        Assert.Equal(4, payload.BreachedIncidentsCount);
        Assert.Equal(3500.00m, payload.RawCreditUsd);
        Assert.Equal(3000.00m, payload.CappedCreditUsd);
        Assert.Equal(30.0m, payload.AppliedCapPercentage);
        Assert.True(payload.WasCapped);
    }

    [Fact]
    public async Task CalculateCredits_ReturnsRfc9457ProblemDetailsOnNegativeInvoice()
    {
        using var client = _factory.CreateClient();

        var request = new SlaCreditCalculationRequest("Bancario-Tier1", -500m, ["INC-2026-1001"]);
        var response = await client.PostAsJsonAsync("/api/sla/credits/calculate", request);

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal("SLA-400-INVALID-INVOICE-AMOUNT", doc.RootElement.GetProperty("errorCode").GetString());
    }

    [Fact]
    public async Task ExportSummary_ReturnsDeterministicCountsBySeverity()
    {
        using var client = _factory.CreateClient();

        var response = await client.GetAsync("/api/sla/incidents/export-summary");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var summary = await response.Content.ReadFromJsonAsync<ShiftExportSummaryDto>();
        Assert.NotNull(summary);
        Assert.Equal(FixedNowUtc, summary.GeneratedAtUtc);
        Assert.Equal(5, summary.TotalIncidents);
        Assert.Equal(2, summary.OpenIncidents);
        Assert.Equal(4, summary.BreachedIncidents);
        Assert.Equal(4, summary.CountBySeverity["P1"]);
        Assert.Equal(1, summary.CountBySeverity["P2"]);
    }

    private sealed class FixedTimeProvider(DateTimeOffset utcNow) : TimeProvider
    {
        public override DateTimeOffset GetUtcNow() => utcNow;
    }
}
