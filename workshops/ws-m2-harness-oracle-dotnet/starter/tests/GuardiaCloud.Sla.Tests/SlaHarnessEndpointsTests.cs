using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace GuardiaCloud.Sla.Tests;

public sealed class SlaHarnessEndpointsTests(WebApplicationFactory<Program> factory)
    : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory = factory;

    [Fact]
    public async Task GetIncident_ReturnsOkForSeededIncident()
    {
        using var client = _factory.CreateClient();

        var response = await client.GetAsync("/api/sla/incidents/INC-2026-1001");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
