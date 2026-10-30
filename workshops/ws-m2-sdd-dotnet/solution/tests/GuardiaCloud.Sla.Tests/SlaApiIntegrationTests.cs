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
    public async Task ResolvedIncident_FreezesSlaClock_AtResolvedAtUtc_RegressionTest()
    {
        // Escenario del bug reportado por Operaciones (/speckit-bug-test):
        // Se abre P1 a las 12:00, se resuelve a los 40 min (adentro del SLA de 60 min),
        // y se consulta el tablero 10 horas después. Debe seguir con IsBreached = false y 40 min activos.
        var t0 = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(t0);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var createResponse = await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "banco-rio",
            Title: "Caída de nodo primario",
            Priority: IncidentPriority.CriticalP1,
            OpenedAtUtc: t0));
        var created = await createResponse.Content.ReadFromJsonAsync<Incident>();
        Assert.NotNull(created);

        clock.Advance(TimeSpan.FromMinutes(40));
        var resolveResponse = await client.PostAsJsonAsync(
            $"/api/incidents/{created.Id}/resolve",
            new ResolveIncidentRequest(ResolutionSummary: "Failover completado"));
        Assert.Equal(HttpStatusCode.OK, resolveResponse.StatusCode);

        // Pasan 10 horas más hasta que el dashboard consulta el SLA
        clock.Advance(TimeSpan.FromHours(10));

        var sla = await client.GetFromJsonAsync<SlaStatusResponse>($"/api/incidents/{created.Id}/sla");
        Assert.NotNull(sla);
        Assert.Equal(IncidentStatus.Resolved, sla.Status);
        Assert.Equal(40, sla.ElapsedActiveMinutes);
        Assert.Equal(20, sla.RemainingMinutes);
        Assert.False(sla.IsBreached);
    }

    [Fact]
    public async Task PauseAndResumeSla_OnHighP2_ExcludesPausedWindowAndShiftsDeadline()
    {
        // Spec 001 (US1): Pausar y reanudar el reloj de SLA excluyendo el tiempo de espera del cliente
        var t0 = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(t0);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var created = await (await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "seguros-austral",
            Title: "Error 502 en webhook de pólizas",
            Priority: IncidentPriority.HighP2,
            OpenedAtUtc: t0))).Content.ReadFromJsonAsync<Incident>();
        Assert.NotNull(created);

        // 1) Corren 30 min activos
        clock.Advance(TimeSpan.FromMinutes(30));

        // 2) Se pausa esperando logs del cliente
        var pauseResponse = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerLogs,
            RequestedBy: "fdeboli@consultora.ar",
            EvidenceNote: "Solicitado dump de request ID 9941 por ticket #402"));
        Assert.Equal(HttpStatusCode.OK, pauseResponse.StatusCode);

        // 3) El cliente tarda 90 minutos en responder (en pausa)
        clock.Advance(TimeSpan.FromMinutes(90));

        // 4) Reanudamos cuando el cliente envía los logs
        var resumeResponse = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/resume", new ResumeSlaRequest(
            ResumedBy: "fdeboli@consultora.ar"));
        Assert.Equal(HttpStatusCode.OK, resumeResponse.StatusCode);

        // 5) Trabajamos 20 minutos activos más
        clock.Advance(TimeSpan.FromMinutes(20));

        var sla = await client.GetFromJsonAsync<SlaStatusResponse>($"/api/incidents/{created.Id}/sla");
        Assert.NotNull(sla);
        Assert.Equal(IncidentStatus.InProgress, sla.Status);
        Assert.Equal(50, sla.ElapsedActiveMinutes); // 30 + 20 activos
        Assert.Equal(90, sla.TotalPausedMinutes);   // 90 pausados
        Assert.Equal(190, sla.RemainingMinutes);    // 240 - 50
        Assert.Equal(t0.AddMinutes(240 + 90), sla.EffectiveDeadlineUtc);
        Assert.False(sla.IsBreached);
        Assert.Equal(1, sla.PauseCount);
    }

    [Fact]
    public async Task DoublePause_ReturnsProblemDetails409Conflict()
    {
        var t0 = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(t0);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var created = await (await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "banco-rio",
            Title: "Latencia alta en sucursales",
            Priority: IncidentPriority.HighP2,
            OpenedAtUtc: t0))).Content.ReadFromJsonAsync<Incident>();
        Assert.NotNull(created);

        var firstPause = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerVpnAccess,
            RequestedBy: "oncall@consultora.ar",
            EvidenceNote: "Esperando habilitación de túnel IPSec"));
        Assert.Equal(HttpStatusCode.OK, firstPause.StatusCode);

        var secondPause = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerVpnAccess,
            RequestedBy: "oncall@consultora.ar",
            EvidenceNote: "Intento duplicado"));
        Assert.Equal(HttpStatusCode.Conflict, secondPause.StatusCode);
    }

    [Fact]
    public async Task CriticalP1_PauseBudget_CapsAt30Minutes_UnlessSupervisorOverrideProvided()
    {
        // Regla Delta OpenSpec (cap-p1-pause-budget):
        // En P1 el tope de pausa acreditable sin supervisor es 30 minutos.
        var t0 = new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero);
        var clock = new FakeTimeProvider(t0);
        await using var factory = CreateFactory(clock);
        using var client = factory.CreateClient();

        var created = await (await client.PostAsJsonAsync("/api/incidents", new CreateIncidentRequest(
            TenantId: "banco-rio",
            Title: "Corte en motor de transferencias",
            Priority: IncidentPriority.CriticalP1,
            OpenedAtUtc: t0))).Content.ReadFromJsonAsync<Incident>();
        Assert.NotNull(created);

        // Corren 10 min activos y se pausa sin código de supervisor
        clock.Advance(TimeSpan.FromMinutes(10));
        await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerLogs,
            RequestedBy: "oncall@consultora.ar",
            EvidenceNote: "Esperando logs de HSM"));

        // Pasan 45 minutos en pausa (supera el tope estándar de 30 min en 15 min)
        clock.Advance(TimeSpan.FromMinutes(45));
        await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/resume", new ResumeSlaRequest(
            ResumedBy: "oncall@consultora.ar"));

        var slaAfterResume = await client.GetFromJsonAsync<SlaStatusResponse>($"/api/incidents/{created.Id}/sla");
        Assert.NotNull(slaAfterResume);
        Assert.Equal(30, slaAfterResume.TotalPausedMinutes);        // Acreditados solo 30 min de los 45 min
        Assert.Equal(0, slaAfterResume.RemainingPauseBudgetMinutes); // Presupuesto agotado
        Assert.Equal(25, slaAfterResume.ElapsedActiveMinutes);       // 10 min iniciales + 15 min excedentes de pausa

        // Si intentamos abrir una segunda pausa sin SupervisorOverrideCode -> 422 UnprocessableEntity
        var rejectedPause = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerValidation,
            RequestedBy: "oncall@consultora.ar",
            EvidenceNote: "Nueva espera sin override"));
        Assert.Equal(HttpStatusCode.UnprocessableEntity, rejectedPause.StatusCode);

        // Si enviamos SupervisorOverrideCode válido -> 200 OK y destraba el presupuesto
        var approvedPause = await client.PostAsJsonAsync($"/api/incidents/{created.Id}/sla/pause", new PauseSlaRequest(
            Reason: SlaPauseReason.WaitingForCustomerValidation,
            RequestedBy: "oncall@consultora.ar",
            EvidenceNote: "Aprobado por guardia gerencial",
            SupervisorOverrideCode: "SUP-2026-OK"));
        Assert.Equal(HttpStatusCode.OK, approvedPause.StatusCode);
    }
}
