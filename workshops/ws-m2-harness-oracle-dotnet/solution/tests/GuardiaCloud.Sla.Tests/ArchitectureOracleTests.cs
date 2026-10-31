using GuardiaCloud.Sla.Api.Domain;
using NetArchTest.Rules;
using Xunit;

namespace GuardiaCloud.Sla.Tests;

public sealed class ArchitectureOracleTests
{
    [Fact]
    public void Domain_Assembly_Contains_SlaRuleEngine()
    {
        var result = Types.InAssembly(typeof(SlaRuleEngine).Assembly)
            .That()
            .ResideInNamespace("GuardiaCloud.Sla.Api.Domain")
            .GetTypes();

        Assert.NotEmpty(result);
    }

    [Fact]
    public void Domain_Should_Not_Depend_On_Infrastructure_Or_AspNetCoreHttp()
    {
        var result = Types.InAssembly(typeof(SlaRuleEngine).Assembly)
            .That()
            .ResideInNamespace("GuardiaCloud.Sla.Api.Domain")
            .ShouldNot()
            .HaveDependencyOnAny(
                "GuardiaCloud.Sla.Api.Infrastructure",
                "Microsoft.AspNetCore.Http")
            .GetResult();

        Assert.True(
            result.IsSuccessful,
            $"Violación de arquitectura limpia en Domain: {string.Join(", ", result.FailingTypeNames ?? [])}");
    }

    [Fact]
    public void Domain_Classes_Should_Be_Sealed()
    {
        var result = Types.InAssembly(typeof(SlaRuleEngine).Assembly)
            .That()
            .ResideInNamespace("GuardiaCloud.Sla.Api.Domain")
            .And()
            .AreClasses()
            .Should()
            .BeSealed()
            .GetResult();

        Assert.True(
            result.IsSuccessful,
            $"Las siguientes clases de Domain no son sealed: {string.Join(", ", result.FailingTypeNames ?? [])}");
    }
}
