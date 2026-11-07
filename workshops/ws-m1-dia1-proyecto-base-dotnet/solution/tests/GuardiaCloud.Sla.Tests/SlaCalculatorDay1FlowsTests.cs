using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Services;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Xunit;

namespace GuardiaCloud.Sla.Tests;

/// <summary>
/// Suite de pruebas de la Unidad 1.2 (Flujos 2, 3, 4 y 5) verificada con FakeTimeProvider.
/// </summary>
public sealed class SlaCalculatorDay1FlowsTests
{
    [Theory]
    [InlineData(SeverityTier.P1, 60)]
    [InlineData(SeverityTier.P2, 240)]
    [InlineData(SeverityTier.P3, 1440)]
    public void Flow2_GetTargetResponseWindow_ReturnsExpectedMinutes(SeverityTier tier, int expectedMinutes)
    {
        var window = SlaCalculator.GetTargetResponseWindow(tier);
        Assert.Equal(expectedMinutes, window.TotalMinutes);
    }

    [Theory]
    [InlineData(60.0, false, 1.0)]   // Borde exacto minuto 60.0 -> En tiempo
    [InlineData(60.1, true, 1.0017)] // 60.1 min (6 seg después) -> Incumplido
    public void Flow3_Evaluate_AtExactBoundary_And_JustOver_P1(
        double elapsedMinutes,
        bool expectedBreach,
        double expectedRatio)
    {
        var openedAt = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(openedAt);
        clock.Advance(TimeSpan.FromMinutes(elapsedMinutes));

        var status = SlaCalculator.Evaluate(openedAt, resolvedAtUtc: null, SeverityTier.P1, clock.GetUtcNow());

        Assert.Equal(expectedBreach, status.IsBreached);
        Assert.Equal(expectedRatio, status.ConsumedRatio, precision: 3);
    }

    [Fact]
    public void Flow3_Evaluate_AcrossMidnightUtc_ComputesAccurateElapsedMinutes()
    {
        var openedAt = new DateTimeOffset(2026, 10, 30, 23, 30, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(new DateTimeOffset(2026, 10, 31, 0, 15, 0, TimeSpan.Zero));

        var status = SlaCalculator.Evaluate(openedAt, resolvedAtUtc: null, SeverityTier.P1, clock.GetUtcNow());

        Assert.Equal(45, status.ElapsedActiveMinutes);
        Assert.False(status.IsBreached);
    }

    [Fact]
    public void Flow4_Evaluate_Uses_ResolvedAtUtc_Instead_Of_CurrentTime_When_Incident_Is_Closed()
    {
        // Incidente P1 abierto a las 10:00Z y resuelto a las 10:45Z (45 min <= 60 min).
        // Se consulta el tablero a las 18:00Z (8 horas después).
        var openedAt = new DateTimeOffset(2026, 10, 30, 10, 0, 0, TimeSpan.Zero);
        var resolvedAt = new DateTimeOffset(2026, 10, 30, 10, 45, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(new DateTimeOffset(2026, 10, 30, 18, 0, 0, TimeSpan.Zero));

        var calculator = new SlaCalculator(clock);
        var incident = new Incident
        {
            TenantId = "banco-austral",
            Title = "Caída de switch core",
            Priority = IncidentPriority.CriticalP1,
            Status = IncidentStatus.Resolved,
            OpenedAtUtc = openedAt,
            ResolvedAtUtc = resolvedAt
        };

        var result = calculator.Evaluate(incident);

        Assert.Equal(45, result.ElapsedActiveMinutes);
        Assert.False(result.IsBreached);
    }

    [Fact]
    public async Task Flow5_ExportEndpoint_WithInvalidPriority_ReturnsProblemDetails400_Not500()
    {
        var clock = new FakeTimeProvider(new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero));
        await using var factory = new WebApplicationFactory<Program>().WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services => services.AddSingleton<TimeProvider>(clock));
        });
        using var client = factory.CreateClient();

        var response = await client.GetAsync("/api/incidents/export?priority=INVALID_PRIORITY");

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var payload = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("SLA-400-INVALID-EXPORT-FILTER", payload.GetProperty("errorCode").GetString());
    }
}
