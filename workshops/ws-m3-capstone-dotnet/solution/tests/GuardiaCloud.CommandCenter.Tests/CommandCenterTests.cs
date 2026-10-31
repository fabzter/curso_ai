using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using GuardiaCloud.CommandCenter.Api.Domain;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using NetArchTest.Rules;
using Xunit;

namespace GuardiaCloud.CommandCenter.Tests;

public sealed class CommandCenterTests(WebApplicationFactory<Program> factory)
    : IClassFixture<WebApplicationFactory<Program>>
{
    private static readonly DateTimeOffset FixedNowUtc = new(2026, 10, 30, 14, 0, 0, TimeSpan.Zero);

    private WebApplicationFactory<Program> CreateIsolatedFactory() =>
        factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                services.RemoveAll<TimeProvider>();
                services.AddSingleton<TimeProvider>(new FixedTimeProvider(FixedNowUtc));
            });
        });

    [Fact]
    public void ArchitectureOracle_Domain_Should_Not_Depend_On_Infrastructure_Or_Http()
    {
        var result = Types.InAssembly(typeof(CommandCenterEvaluator).Assembly)
            .That()
            .ResideInNamespace("GuardiaCloud.CommandCenter.Api.Domain")
            .ShouldNot()
            .HaveDependencyOnAny(
                "GuardiaCloud.CommandCenter.Api.Infrastructure",
                "Microsoft.AspNetCore.Http")
            .GetResult();

        Assert.True(result.IsSuccessful);
    }

    [Fact]
    public void ArchitectureOracle_Domain_Classes_Should_Be_Sealed()
    {
        var result = Types.InAssembly(typeof(CommandCenterEvaluator).Assembly)
            .That()
            .ResideInNamespace("GuardiaCloud.CommandCenter.Api.Domain")
            .And()
            .AreClasses()
            .Should()
            .BeSealed()
            .GetResult();

        Assert.True(result.IsSuccessful);
    }

    [Fact]
    public async Task GetIncident_ReturnsOkForSeededCommandCenterIncident()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        var response = await client.GetAsync("/api/command-center/incidents/INC-2026-3001");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task WebhookEvent_IsIdempotentOnDuplicateEventId_Bug301()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        var webhook = new IncidentWebhookEventRequest("EVT-9001", "INC-2026-3001", 5, TriggerPenaltyIncrement: true);

        var firstResponse = await client.PostAsJsonAsync("/api/command-center/webhooks/incident-event", webhook);
        var firstResult = await firstResponse.Content.ReadFromJsonAsync<WebhookProcessingResult>();
        Assert.NotNull(firstResult);
        Assert.False(firstResult.WasDuplicateIgnored);
        Assert.Equal(5, firstResult.TotalPausedMinutes);
        Assert.Equal(1, firstResult.AppliedPenaltyEventsCount);

        var duplicateResponse = await client.PostAsJsonAsync("/api/command-center/webhooks/incident-event", webhook);
        var duplicateResult = await duplicateResponse.Content.ReadFromJsonAsync<WebhookProcessingResult>();
        Assert.NotNull(duplicateResult);
        Assert.True(duplicateResult.WasDuplicateIgnored);
        Assert.Equal(5, duplicateResult.TotalPausedMinutes);
        Assert.Equal(1, duplicateResult.AppliedPenaltyEventsCount);
    }

    [Fact]
    public async Task ProactiveEscalation_DispatchesAt80PercentAndRespects15MinuteCooldown_Feat301()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        var first = await client.PostAsync("/api/command-center/escalations/evaluate/INC-2026-3001", null);
        var firstDto = await first.Content.ReadFromJsonAsync<ProactiveEscalationResult>();
        Assert.NotNull(firstDto);
        Assert.True(firstDto.ShouldDispatchAlert);
        Assert.Equal("ALERT_DISPATCHED", firstDto.ReasonCode);

        var second = await client.PostAsync("/api/command-center/escalations/evaluate/INC-2026-3001", null);
        var secondDto = await second.Content.ReadFromJsonAsync<ProactiveEscalationResult>();
        Assert.NotNull(secondDto);
        Assert.False(secondDto.ShouldDispatchAlert);
        Assert.Equal("COOLDOWN_ACTIVE_15M", secondDto.ReasonCode);
    }

    [Fact]
    public async Task ForceMajeureExemption_RejectsSameApproverWithRfc9457ErrorCode_Feat302()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        var invalidRequest = new ForceMajeureExemptionRequest(
            "INC-2026-3002",
            "COELSA-OUTAGE",
            "ana.lopez@guardiacloud.com",
            "ANA.LOPEZ@guardiacloud.com",
            "FM-DUAL-2026-99");

        var response = await client.PostAsJsonAsync("/api/command-center/exemptions", invalidRequest);
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);

        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal("CC-400-SAME-APPROVER", doc.RootElement.GetProperty("errorCode").GetString());
    }

    [Fact]
    public async Task ForceMajeureExemption_RejectsInvalidDualTokenWith422_Feat302()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        var invalidTokenRequest = new ForceMajeureExemptionRequest(
            "INC-2026-3002",
            "COELSA-OUTAGE",
            "ana.lopez@guardiacloud.com",
            "carlos.ruiz@guardiacloud.com",
            "TOKEN-SIN-PREFIJO");

        var response = await client.PostAsJsonAsync("/api/command-center/exemptions", invalidTokenRequest);
        Assert.Equal(HttpStatusCode.UnprocessableEntity, response.StatusCode);

        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal("CC-422-INVALID-DUAL-TOKEN", doc.RootElement.GetProperty("errorCode").GetString());
    }

    [Fact]
    public async Task TierDashboard_CalculatesExposureAndExcludesExemptedIncidents_Feat303()
    {
        using var isolatedFactory = CreateIsolatedFactory();
        using var client = isolatedFactory.CreateClient();

        // Antes de la exención: INC-2026-3002 (USD 2500) + INC-2026-3003 (USD 800) = USD 3300 de exposición
        var beforeResponse = await client.GetAsync("/api/command-center/dashboard/Bancario-Tier1");
        var beforeDto = await beforeResponse.Content.ReadFromJsonAsync<TierExecutiveDashboardDto>();
        Assert.NotNull(beforeDto);
        Assert.Equal(3, beforeDto.TotalIncidents);
        Assert.Equal(2, beforeDto.BreachedIncidents);
        Assert.Equal(1, beforeDto.AtRiskIncidents);
        Assert.Equal(0, beforeDto.ExemptedIncidents);
        Assert.Equal(3300.00m, beforeDto.TotalFinancialExposureUsd);

        // Aplicamos exención válida por fuerza mayor sobre INC-2026-3002 (USD 2500)
        var exemptionReq = new ForceMajeureExemptionRequest(
            "INC-2026-3002",
            "COELSA-OUTAGE",
            "ana.lopez@guardiacloud.com",
            "carlos.ruiz@guardiacloud.com",
            "FM-DUAL-BCRA-99");
        var exResponse = await client.PostAsJsonAsync("/api/command-center/exemptions", exemptionReq);
        Assert.Equal(HttpStatusCode.OK, exResponse.StatusCode);

        // Después de la exención: la exposición financiera baja a USD 800.00
        var afterResponse = await client.GetAsync("/api/command-center/dashboard/Bancario-Tier1");
        var afterDto = await afterResponse.Content.ReadFromJsonAsync<TierExecutiveDashboardDto>();
        Assert.NotNull(afterDto);
        Assert.Equal(1, afterDto.ExemptedIncidents);
        Assert.Equal(800.00m, afterDto.TotalFinancialExposureUsd);
    }

    private sealed class FixedTimeProvider(DateTimeOffset utcNow) : TimeProvider
    {
        public override DateTimeOffset GetUtcNow() => utcNow;
    }
}
