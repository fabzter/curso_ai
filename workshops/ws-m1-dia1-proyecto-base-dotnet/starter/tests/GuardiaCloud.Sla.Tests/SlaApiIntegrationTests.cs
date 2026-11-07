using System.Net;
using System.Net.Http.Json;
using GuardiaCloud.Sla.Api.Domain;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Xunit;

namespace GuardiaCloud.Sla.Tests;

public sealed class FakeTimeProvider(DateTimeOffset initialUtc) : TimeProvider
{
    private DateTimeOffset _nowUtc = initialUtc.ToUniversalTime();

    public override DateTimeOffset GetUtcNow() => _nowUtc;

    public void Advance(TimeSpan delta) => _nowUtc = _nowUtc.Add(delta);
}

public sealed class SlaApiIntegrationTests
{
    private static WebApplicationFactory<Program> CreateFactory(FakeTimeProvider clock) =>
        new WebApplicationFactory<Program>().WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                services.AddSingleton<TimeProvider>(clock);
            });
        });

    [Fact]
    public async Task CreateIncident_And_QuerySla_ReturnsActiveRemainingMinutes()
    {
        var t0 = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(t0);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var createResponse = await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "banco-rio",
            Title: "Timeout en gateway de pagos",
            Priority: IncidentPriority.CriticalP1,
            OpenedAtUtc: t0));

        Assert.Equal(HttpStatusCode.Created, createResponse.StatusCode);
        var created = await createResponse.Content.ReadFromJsonAsync<Incident>();
        Assert.NotNull(created);

        // Avanzamos el reloj 25 minutos (objetivo P1 = 60 min)
        clock.Advance(TimeSpan.FromMinutes(25));

        var sla = await client.GetFromJsonAsync<SlaStatusResponse>($"/api/incidents/{created.Id}/sla");
        Assert.NotNull(sla);
        Assert.Equal(60, sla.TargetResolutionMinutes);
        Assert.Equal(25, sla.ElapsedActiveMinutes);
        Assert.Equal(35, sla.RemainingMinutes);
        Assert.False(sla.IsBreached);
    }

    [Fact]
    public async Task CreateIncident_WithEmptyTenant_ReturnsProblemDetails400()
    {
        var clock = new FakeTimeProvider(DateTimeOffset.UtcNow);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var response = await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "",
            Title: "Incidente sin tenant",
            Priority: IncidentPriority.HighP2));

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
