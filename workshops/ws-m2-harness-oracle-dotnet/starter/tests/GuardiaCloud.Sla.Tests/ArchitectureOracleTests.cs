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

    // TODO (Fase 2 - Unidad 2.3): Agregar las 2 reglas de arquitectura verificables con NetArchTest.Rules:
    // 1. Domain_Should_Not_Depend_On_Infrastructure_Or_AspNetCoreHttp:
    //    Ningún tipo en "GuardiaCloud.Sla.Api.Domain" puede tener dependencia hacia "GuardiaCloud.Sla.Api.Infrastructure" ni "Microsoft.AspNetCore.Http".
    // 2. Domain_Classes_Should_Be_Sealed:
    //    Toda clase en "GuardiaCloud.Sla.Api.Domain" debe ser sealed (.Should().BeSealed()).
}
