using System.Net;
using GuardiaCloud.CommandCenter.Api.Domain;
using Microsoft.AspNetCore.Mvc.Testing;
using NetArchTest.Rules;
using Xunit;

namespace GuardiaCloud.CommandCenter.Tests;

public sealed class CommandCenterTests(WebApplicationFactory<Program> factory)
    : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory = factory;

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
        using var client = _factory.CreateClient();

        var response = await client.GetAsync("/api/command-center/incidents/INC-2026-3001");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
