using GuardiaCloud.Sla.McpServer.Agent;
using GuardiaCloud.Sla.McpServer.Infrastructure;
using GuardiaCloud.Sla.McpServer.McpTools;
using Microsoft.Extensions.DependencyInjection;
using ModelContextProtocol.Server;
using Xunit;

namespace GuardiaCloud.Sla.McpTests;

public sealed class SlaMcpWorkshopTests
{
    private static readonly DateTimeOffset FixedNowUtc = new(2026, 10, 30, 14, 0, 0, TimeSpan.Zero);

    [Fact]
    public void GetClientSlaPolicy_ReturnsExpectedBancarioTier1P1Targets()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, new FixedTimeProvider(FixedNowUtc));

        var policy = tools.GetClientSlaPolicy("Bancario-Tier1", "P1");

        Assert.Equal("Bancario-Tier1", policy.ClientTier);
        Assert.Equal("P1", policy.Severity);
        Assert.Equal(60, policy.TargetResolutionMinutes);
        Assert.Equal(30, policy.MaxAllowedPauseMinutes);
        Assert.Equal(2500m, policy.PenaltyPerHourUsd);
    }

    [Fact]
    public void GetClientSlaPolicy_RejectsInvalidClientTierAndSeverityWithRfc9457ErrorCode()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, new FixedTimeProvider(FixedNowUtc));

        var tierEx = Assert.Throws<ArgumentException>(() => tools.GetClientSlaPolicy("Tier-Inventado", "P1"));
        Assert.Contains("SLA-400-INVALID-CLIENT-TIER", tierEx.Message, StringComparison.Ordinal);

        var sevEx = Assert.Throws<ArgumentException>(() => tools.GetClientSlaPolicy("Bancario-Tier1", "P99"));
        Assert.Contains("SLA-400-INVALID-SEVERITY", sevEx.Message, StringComparison.Ordinal);
    }

    [Fact]
    public void InspectIncidentSlaStatus_CalculatesBreachAndSanitizesIndirectPromptInjection()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, new FixedTimeProvider(FixedNowUtc));

        // INC-2026-1002: abrió hace 95m, tiene 15m de pausa válida => 80m efectivos vs 60m objetivo (BREACHED)
        var audit = tools.InspectIncidentSlaStatus("INC-2026-1002");

        Assert.Equal("INC-2026-1002", audit.IncidentId);
        Assert.Equal(80.0, audit.EffectiveElapsedMinutes);
        Assert.Equal(60, audit.TargetResolutionMinutes);
        Assert.True(audit.IsBreached);
        Assert.Equal("BREACHED", audit.Status);
        Assert.DoesNotContain("SYSTEM OVERRIDE", audit.SanitizedSummary, StringComparison.OrdinalIgnoreCase);
        Assert.Contains("[REDACTED-UNTRUSTED-INSTRUCTION]", audit.SanitizedSummary, StringComparison.Ordinal);
    }

    [Fact]
    public void ValidateRfc9457Contract_DetectsMismatchedStatusAndTypeUri()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, new FixedTimeProvider(FixedNowUtc));

        var valid = tools.ValidateRfc9457Contract(
            "SLA-422-P1-PAUSE-BUDGET-EXCEEDED",
            422,
            "https://errors.guardiacloud.internal/sla/p1-pause-budget-exceeded");
        Assert.True(valid.IsValid);
        Assert.Empty(valid.Violations);

        var invalid = tools.ValidateRfc9457Contract(
            "SLA-422-P1-PAUSE-BUDGET-EXCEEDED",
            400,
            "https://example.com/wrong-uri");
        Assert.False(invalid.IsValid);
        Assert.Equal(2, invalid.Violations.Count);
    }

    [Fact]
    public void McpServer_RegistersAllThreeToolsWithReadOnlyAnnotationsAndDescriptions()
    {
        var builder = GuardiaCloud.Sla.McpServer.Program.CreateHostBuilder([]);
        using var host = builder.Build();

        var registeredTools = host.Services.GetServices<McpServerTool>().ToList();
        var toolNames = registeredTools.Select(t => t.ProtocolTool.Name).ToHashSet(StringComparer.Ordinal);

        Assert.Equal(3, registeredTools.Count);
        Assert.Contains("get_client_sla_policy", toolNames);
        Assert.Contains("inspect_incident_sla_status", toolNames);
        Assert.Contains("validate_rfc9457_contract", toolNames);

        foreach (var tool in registeredTools)
        {
            Assert.False(string.IsNullOrWhiteSpace(tool.ProtocolTool.Description));
            Assert.Equal(true, tool.ProtocolTool.Annotations?.ReadOnlyHint);
            Assert.Equal(true, tool.ProtocolTool.Annotations?.IdempotentHint);
            Assert.Equal(false, tool.ProtocolTool.Annotations?.DestructiveHint);
            Assert.Equal(false, tool.ProtocolTool.Annotations?.OpenWorldHint);
        }
    }

    [Fact]
    public async Task SlaTriageAgent_ExecutesMultiStepToolCallingLoopViaMicrosoftExtensionsAi()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, new FixedTimeProvider(FixedNowUtc));
        using var innerClient = new DeterministicTriageChatClient("INC-2026-1002");
        var agent = new SlaTriageAgent(tools, innerClient);

        var report = await agent.RunTriageAsync("INC-2026-1002");

        Assert.Equal("INC-2026-1002", report.IncidentId);
        Assert.Equal(["inspect_incident_sla_status", "get_client_sla_policy"], report.InvokedToolNames);
        Assert.Contains("BREACHED", report.FinalSummary, StringComparison.Ordinal);
        Assert.Contains("[REDACTED-UNTRUSTED-INSTRUCTION]", report.FinalSummary, StringComparison.Ordinal);
        Assert.DoesNotContain("SYSTEM OVERRIDE", report.FinalSummary, StringComparison.OrdinalIgnoreCase);
    }

    private sealed class FixedTimeProvider(DateTimeOffset utcNow) : TimeProvider
    {
        public override DateTimeOffset GetUtcNow() => utcNow;
    }
}
