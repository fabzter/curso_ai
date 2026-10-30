using GuardiaCloud.Sla.McpServer.Infrastructure;
using GuardiaCloud.Sla.McpServer.McpTools;
using Microsoft.Extensions.DependencyInjection;
using ModelContextProtocol.Server;
using Xunit;

namespace GuardiaCloud.Sla.McpTests;

public sealed class SlaMcpWorkshopTests
{
    [Fact]
    public void GetClientSlaPolicy_ReturnsExpectedBancarioTier1P1Targets()
    {
        var store = new InMemorySlaCatalogStore();
        var tools = new SlaMcpTools(store, TimeProvider.System);

        var policy = tools.GetClientSlaPolicy("Bancario-Tier1", "P1");

        Assert.Equal("Bancario-Tier1", policy.ClientTier);
        Assert.Equal("P1", policy.Severity);
        Assert.Equal(60, policy.TargetResolutionMinutes);
        Assert.Equal(30, policy.MaxAllowedPauseMinutes);
        Assert.Equal(2500m, policy.PenaltyPerHourUsd);
    }

    [Fact]
    public void McpServer_RegistersBaselinePolicyToolWithReadOnlyAnnotations()
    {
        var builder = GuardiaCloud.Sla.McpServer.Program.CreateHostBuilder([]);
        using var host = builder.Build();

        var registeredTools = host.Services.GetServices<McpServerTool>().ToList();

        var policyTool = Assert.Single(registeredTools, t => t.ProtocolTool.Name == "get_client_sla_policy");
        Assert.NotNull(policyTool.ProtocolTool.Description);
        Assert.Contains("Bancario-Tier1", policyTool.ProtocolTool.Description, StringComparison.Ordinal);
        Assert.Equal(true, policyTool.ProtocolTool.Annotations?.ReadOnlyHint);
        Assert.Equal(false, policyTool.ProtocolTool.Annotations?.DestructiveHint);
    }
}
