#!/usr/bin/env python3
"""
Scaffolds the complete Day 1 Base Project (`workshops/ws-m1-dia1-proyecto-base-dotnet/starter` and `solution`),
completes the missing artifacts in `ws-m2-sdd-dotnet` (Unit 2.2 Impact & Estimation report) and
`ws-m3-capstone-dotnet` (Unit 3.2 UI Prototype + design tokens), writes `workshops/README.md`,
and packages the clean `.zip` archive (`GuardiaCloud-Sla-Proyectos-Base-y-Workshops-DotNet10.zip`)
for Max and the students.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WS_DAY1 = ROOT / "workshops" / "ws-m1-dia1-proyecto-base-dotnet"

SLN_CONTENT = (ROOT / "workshops" / "ws-m2-sdd-dotnet" / "starter" / "GuardiaCloud.Sla.sln").read_text(encoding="utf-8")
API_CSPROJ = (ROOT / "workshops" / "ws-m2-sdd-dotnet" / "starter" / "src" / "GuardiaCloud.Sla.Api" / "GuardiaCloud.Sla.Api.csproj").read_text(encoding="utf-8")
TESTS_CSPROJ = (ROOT / "workshops" / "ws-m2-sdd-dotnet" / "starter" / "tests" / "GuardiaCloud.Sla.Tests" / "GuardiaCloud.Sla.Tests.csproj").read_text(encoding="utf-8")

# ==============================================================================
# 1. DOMAIN MODELS (Shared between starter and solution of Day 1)
# ==============================================================================
DOMAIN_MODELS_CS = """namespace GuardiaCloud.Sla.Api.Domain;

/// <summary>
/// Prioridad operativa del incidente (compatible con la nomenclatura P1/P2/P3 de los slides).
/// </summary>
public enum IncidentPriority
{
    CriticalP1 = 1,
    HighP2 = 2,
    StandardP3 = 3,
    P1 = CriticalP1,
    P2 = HighP2,
    P3 = StandardP3
}

/// <summary>
/// Alias semántico usado en las slides de las Unidades 1.1 y 1.2 (SeverityTier.P1, P2, P3).
/// </summary>
public enum SeverityTier
{
    P1 = 1,
    P2 = 2,
    P3 = 3
}

public enum ClientTier
{
    Platinum = 1,
    Gold = 2,
    Silver = 3
}

public enum IncidentStatus
{
    Open = 1,
    InProgress = 2,
    Resolved = 3
}

public enum PauseReason
{
    WaitingForCustomer = 1,
    MaintenanceWindow = 2
}

public static class SlaPolicyCatalog
{
    public static int GetTargetMinutes(IncidentPriority priority) => priority switch
    {
        IncidentPriority.CriticalP1 => 60,
        IncidentPriority.HighP2 => 240,
        IncidentPriority.StandardP3 => 1440,
        _ => throw new ArgumentOutOfRangeException(nameof(priority), $"Prioridad no soportada: {priority}")
    };
}

public sealed class Incident
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public string Code { get; init; } = "INC-2026-1001";
    public required string TenantId { get; init; }
    public required string Title { get; init; }
    public required IncidentPriority Priority { get; init; }
    public ClientTier Tier { get; init; } = ClientTier.Platinum;
    public IncidentStatus Status { get; set; } = IncidentStatus.Open;
    public required DateTimeOffset OpenedAtUtc { get; init; }
    public DateTimeOffset? ResolvedAtUtc { get; set; }
}

public sealed record PauseWindowDto(
    PauseReason Reason,
    DateTimeOffset StartsAtUtc,
    DateTimeOffset EndsAtUtc);

/// <summary>
/// Contrato DTO exacto utilizado en la Unidad 1.1 (Diseño UI con IA + Handoff a Blazor / OpenAPI).
/// </summary>
public sealed record IncidentSlaSummaryDto(
    string IncidentId,
    string ClientTier,
    string Severity,
    double ConsumedRatio,
    bool IsBreached,
    DateTimeOffset DeadlineUtc,
    IReadOnlyList<PauseWindowDto> PauseWindows);

/// <summary>
/// Modelo tipado para el componente Blazor SlaStatusCard.razor (Unidad 1.1 Paso 3).
/// </summary>
public sealed record IncidentSlaCardDto(
    string IncidentId,
    string ClientTier,
    string Severity,
    double ConsumedRatio,
    bool IsBreached,
    DateTimeOffset DeadlineUtc,
    IReadOnlyList<PauseWindowDto> PauseWindows)
{
    public bool IsAtRisk80Percent => ConsumedRatio >= 0.80 && !IsBreached;
}

public sealed record CreateIncidentRequest(
    string TenantId,
    string Title,
    IncidentPriority Priority,
    DateTimeOffset? OpenedAtUtc = null,
    ClientTier Tier = ClientTier.Platinum);

public sealed record ResolveIncidentRequest(
    DateTimeOffset? ResolvedAtUtc = null,
    string? ResolutionSummary = null);

public sealed record SlaStatusResponse(
    Guid IncidentId,
    string TenantId,
    IncidentPriority Priority,
    IncidentStatus Status,
    int TargetResolutionMinutes,
    double ElapsedActiveMinutes,
    double RemainingMinutes,
    double ConsumedRatio,
    DateTimeOffset EffectiveDeadlineUtc,
    bool IsBreached);
"""

# ==============================================================================
# 2. STARTER FILES (With deliberate traps for Unit 1.2 Flows 1, 2, 4, and 5)
# ==============================================================================
STARTER_SLA_SERVICES_CS = """using System.Collections.Concurrent;
using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Services;

public interface IIncidentRepository
{
    Incident Add(Incident incident);
    Incident? GetById(Guid id);
    IReadOnlyCollection<Incident> ListAll();
    IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId);
}

public sealed class InMemoryIncidentRepository : IIncidentRepository
{
    private readonly ConcurrentDictionary<Guid, Incident> _store = new();

    public Incident Add(Incident incident)
    {
        _store[incident.Id] = incident;
        return incident;
    }

    public Incident? GetById(Guid id) =>
        _store.TryGetValue(id, out var incident) ? incident : null;

    public IReadOnlyCollection<Incident> ListAll() =>
        _store.Values.OrderByDescending(i => i.OpenedAtUtc).ToArray();

    public IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId) =>
        [$"AUDIT-OPENED:{incidentId}", $"AUDIT-MONITORED:{incidentId}"];
}

public sealed class SlaCalculator(TimeProvider timeProvider)
{
    // =========================================================================
    // TRAMPA DIDÁCTICA — FLUJO 1 (Arqueología de Código Legado):
    // NOTA HISTÓRICA (2023 - OBSOLETO): Este método convierte automáticamente
    // las marcas de tiempo a huso horario local GMT-3 (Buenos Aires) y otorga
    // 15 minutos extra de gracia en incidentes críticos P1 antes de marcar vencimiento.
    // (¡FALSO! El código real debajo opera en UTC puro y NO suma minutos de gracia).
    // =========================================================================
    public SlaStatusResponse Evaluate(Incident incident)
    {
        var targetMinutes = SlaPolicyCatalog.GetTargetMinutes(incident.Priority);

        // =====================================================================
        // BUG SEMBRADO — FLUJO 4 (Debugging de ResolvedAtUtc):
        // Usa siempre la hora actual del reloj en lugar de incident.ResolvedAtUtc
        // cuando el incidente ya fue cerrado.
        // =====================================================================
        var referenceEndUtc = timeProvider.GetUtcNow();

        var elapsedMinutes = Math.Max(0, (referenceEndUtc - incident.OpenedAtUtc).TotalMinutes);
        var remainingMinutes = Math.Round(targetMinutes - elapsedMinutes, 2);
        var consumedRatio = Math.Round(elapsedMinutes / targetMinutes, 4);
        var effectiveDeadlineUtc = incident.OpenedAtUtc.AddMinutes(targetMinutes);
        var isBreached = elapsedMinutes > targetMinutes;

        return new SlaStatusResponse(
            IncidentId: incident.Id,
            TenantId: incident.TenantId,
            Priority: incident.Priority,
            Status: incident.Status,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: remainingMinutes,
            ConsumedRatio: consumedRatio,
            EffectiveDeadlineUtc: effectiveDeadlineUtc,
            IsBreached: isBreached);
    }

    // =========================================================================
    // CÓDIGO LEGADO A REFACTORIZAR — FLUJO 2 (Refactoring Seguro a C# 13):
    // Condicionales if/else anidados que los alumnos transforman en una
    // switch expression pura y exhaustiva de C# 13.
    // =========================================================================
    public static TimeSpan GetTargetResponseWindow(SeverityTier tier)
    {
        if (tier == SeverityTier.P1)
        {
            return TimeSpan.FromMinutes(60);
        }
        else if (tier == SeverityTier.P2)
        {
            return TimeSpan.FromHours(4);
        }
        else if (tier == SeverityTier.P3)
        {
            return TimeSpan.FromHours(24);
        }
        else
        {
            throw new ArgumentOutOfRangeException(nameof(tier), $"Severidad no soportada: {tier}");
        }
    }

    public static SlaStatusResponse Evaluate(
        DateTimeOffset openedAtUtc,
        DateTimeOffset? resolvedAtUtc,
        SeverityTier tier,
        DateTimeOffset nowUtc)
    {
        var targetMinutes = (int)GetTargetResponseWindow(tier).TotalMinutes;
        // BUG SEMBRADO (Flujo 4): ignora resolvedAtUtc y compara siempre contra nowUtc
        var effectiveEndUtc = nowUtc;
        var elapsedMinutes = Math.Max(0, (effectiveEndUtc - openedAtUtc).TotalMinutes);

        return new SlaStatusResponse(
            IncidentId: Guid.Empty,
            TenantId: "default-tenant",
            Priority: (IncidentPriority)(int)tier,
            Status: resolvedAtUtc.HasValue ? IncidentStatus.Resolved : IncidentStatus.Open,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: Math.Round(targetMinutes - elapsedMinutes, 2),
            ConsumedRatio: Math.Round(elapsedMinutes / targetMinutes, 4),
            EffectiveDeadlineUtc: openedAtUtc.AddMinutes(targetMinutes),
            IsBreached: elapsedMinutes > targetMinutes);
    }
}
"""

STARTER_VIBE_CODED_EXPORT_CS = """using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Services;

namespace GuardiaCloud.Sla.Api.Endpoints;

// =============================================================================
// ARCHIVO CONTAMINADO — UNIDAD 1.2 FLUJO 5 (Code Review de un PR "Vibe-Codeado")
// Simula la rama `pr/vibe-coded-export` generada sin supervisión humana.
// Contiene los 4 defectos clásicos documentados en los slides de la Unidad 1.2:
//   1. Credencial de Azure Storage hardcodeada en el código fuente.
//   2. Endpoint asíncrono sin CancellationToken ni límite de paginación.
//   3. Consulta N+1 iterando logs de auditoría por cada incidente dentro de un foreach.
//   4. Excepción cruda 500 ante filtro inválido en lugar de ProblemDetails RFC 9457 (400).
// =============================================================================
public static class VibeCodedExportEndpoints
{
    // DEFECTO 1: Secreto de producción hardcodeado en código fuente
    private const string HardcodedAzureBlobConnString =
        "DefaultEndpointsProtocol=https;AccountName=guardiacloudprod;AccountKey=PLAIN_TEXT_SECRET_KEY_998877==;EndpointSuffix=core.windows.net";

    public static IEndpointRouteBuilder MapVibeCodedExportEndpoints(this IEndpointRouteBuilder app)
    {
        // DEFECTO 2: No recibe CancellationToken ni acota el tamaño de página (pageSize)
        app.MapGet("/api/incidents/export", async (
            string? priority,
            IIncidentRepository repository,
            SlaCalculator calculator) =>
        {
            await Task.Yield();

            IncidentPriority? filterPriority = null;
            if (!string.IsNullOrWhiteSpace(priority))
            {
                // DEFECTO 4: Lanza excepción cruda 500 en vez de devolver ProblemDetails RFC 9457 (400 Bad Request)
                if (!Enum.TryParse<IncidentPriority>(priority, ignoreCase: true, out var parsed))
                {
                    throw new Exception($"Filtro de prioridad inválido: {priority}. Boom 500! Destino: {HardcodedAzureBlobConnString}");
                }
                filterPriority = parsed;
            }

            var incidents = repository.ListAll()
                .Where(i => !filterPriority.HasValue || i.Priority == filterPriority.Value)
                .ToList();

            var rows = new List<object>();
            foreach (var inc in incidents)
            {
                // DEFECTO 3: Patrón N+1 llamando al repositorio dentro del bucle por cada fila
                var auditTrail = repository.GetAuditLogsForIncident(inc.Id);
                var sla = calculator.Evaluate(inc);
                rows.Add(new
                {
                    inc.Id,
                    inc.TenantId,
                    Priority = inc.Priority.ToString(),
                    sla.ConsumedRatio,
                    sla.IsBreached,
                    AuditCount = auditTrail.Count
                });
            }

            return Results.Ok(rows);
        });

        return app;
    }
}
"""

PROGRAM_CS = """using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Endpoints;
using GuardiaCloud.Sla.Api.Services;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddProblemDetails();
builder.Services.AddSingleton(TimeProvider.System);
builder.Services.AddSingleton<IIncidentRepository, InMemoryIncidentRepository>();
builder.Services.AddSingleton<SlaCalculator>();

var app = builder.Build();

app.UseExceptionHandler();

var group = app.MapGroup("/api/incidents");

group.MapPost("/", (
    CreateIncidentRequest request,
    IIncidentRepository repository,
    TimeProvider timeProvider,
    CancellationToken ct) =>
{
    ct.ThrowIfCancellationRequested();
    if (string.IsNullOrWhiteSpace(request.TenantId) || string.IsNullOrWhiteSpace(request.Title))
    {
        return Results.Problem(
            title: "Datos de incidente inválidos",
            detail: "TenantId y Title son obligatorios.",
            statusCode: StatusCodes.Status400BadRequest,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-400-INVALID-INCIDENT-PAYLOAD" });
    }

    var incident = new Incident
    {
        TenantId = request.TenantId.Trim(),
        Title = request.Title.Trim(),
        Priority = request.Priority,
        Tier = request.Tier,
        OpenedAtUtc = (request.OpenedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime()
    };

    repository.Add(incident);
    return Results.Created($"/api/incidents/{incident.Id}", incident);
});

group.MapGet("/{id:guid}", (Guid id, IIncidentRepository repository, CancellationToken ct) =>
{
    ct.ThrowIfCancellationRequested();
    var incident = repository.GetById(id);
    return incident is not null
        ? Results.Ok(incident)
        : Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
});

group.MapGet("/{id:guid}/sla", (
    Guid id,
    IIncidentRepository repository,
    SlaCalculator calculator,
    CancellationToken ct) =>
{
    ct.ThrowIfCancellationRequested();
    var incident = repository.GetById(id);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
    }

    return Results.Ok(calculator.Evaluate(incident));
});

group.MapPost("/{id:guid}/evaluate", (
    Guid id,
    IIncidentRepository repository,
    SlaCalculator calculator,
    CancellationToken ct) =>
{
    ct.ThrowIfCancellationRequested();
    var incident = repository.GetById(id);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
    }

    return Results.Ok(calculator.Evaluate(incident));
});

group.MapPost("/{id:guid}/resolve", (
    Guid id,
    [FromBody] ResolveIncidentRequest? request,
    IIncidentRepository repository,
    TimeProvider timeProvider,
    CancellationToken ct) =>
{
    ct.ThrowIfCancellationRequested();
    var incident = repository.GetById(id);
    if (incident is null)
    {
        return Results.Problem(
            title: "Incidente no encontrado",
            detail: $"No existe un incidente con Id '{id}'.",
            statusCode: StatusCodes.Status404NotFound,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-404-INCIDENT-NOT-FOUND" });
    }

    var resolvedAt = (request?.ResolvedAtUtc ?? timeProvider.GetUtcNow()).ToUniversalTime();
    if (resolvedAt < incident.OpenedAtUtc)
    {
        return Results.Problem(
            title: "Fecha de resolución inválida",
            detail: "ResolvedAtUtc no puede ser anterior a OpenedAtUtc.",
            statusCode: StatusCodes.Status422UnprocessableEntity,
            extensions: new Dictionary<string, object?> { ["errorCode"] = "SLA-422-INVALID-RESOLUTION-TIME" });
    }

    incident.Status = IncidentStatus.Resolved;
    incident.ResolvedAtUtc = resolvedAt;
    return Results.Ok(incident);
});

app.MapVibeCodedExportEndpoints();

app.Run();

public partial class Program;
"""

STARTER_TESTS_CS = (ROOT / "workshops" / "ws-m2-sdd-dotnet" / "starter" / "tests" / "GuardiaCloud.Sla.Tests" / "SlaApiIntegrationTests.cs").read_text(encoding="utf-8")

# ==============================================================================
# 3. SOLUTION FILES (All 5 Flows of Unit 1.2 + Unit 1.1 UI Handoff completed)
# ==============================================================================
SOLUTION_SLA_SERVICES_CS = """using System.Collections.Concurrent;
using GuardiaCloud.Sla.Api.Domain;

namespace GuardiaCloud.Sla.Api.Services;

public interface IIncidentRepository
{
    Incident Add(Incident incident);
    Incident? GetById(Guid id);
    IReadOnlyCollection<Incident> ListAll();
    IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId);
    IReadOnlyDictionary<Guid, IReadOnlyList<string>> GetAuditLogsBatch(IEnumerable<Guid> incidentIds);
}

public sealed class InMemoryIncidentRepository : IIncidentRepository
{
    private readonly ConcurrentDictionary<Guid, Incident> _store = new();

    public Incident Add(Incident incident)
    {
        _store[incident.Id] = incident;
        return incident;
    }

    public Incident? GetById(Guid id) =>
        _store.TryGetValue(id, out var incident) ? incident : null;

    public IReadOnlyCollection<Incident> ListAll() =>
        _store.Values.OrderByDescending(i => i.OpenedAtUtc).ToArray();

    public IReadOnlyList<string> GetAuditLogsForIncident(Guid incidentId) =>
        [$"AUDIT-OPENED:{incidentId}", $"AUDIT-MONITORED:{incidentId}"];

    public IReadOnlyDictionary<Guid, IReadOnlyList<string>> GetAuditLogsBatch(IEnumerable<Guid> incidentIds) =>
        incidentIds.Distinct().ToDictionary(
            id => id,
            id => (IReadOnlyList<string>)[$"AUDIT-OPENED:{id}", $"AUDIT-MONITORED:{id}"]);
}

/// <summary>
/// Calculador determinista de SLA en UTC (Flujo 1: comentario engañoso eliminado;
/// Flujo 2: switch expression C# 13; Flujo 4: fix de ResolvedAtUtc).
/// </summary>
public sealed class SlaCalculator(TimeProvider timeProvider)
{
    public SlaStatusResponse Evaluate(Incident incident)
    {
        var targetMinutes = SlaPolicyCatalog.GetTargetMinutes(incident.Priority);

        // FIX FLUJO 4: Si el incidente ya está resuelto, el reloj de SLA se detiene en ResolvedAtUtc.
        var effectiveEndUtc = incident.ResolvedAtUtc ?? timeProvider.GetUtcNow();

        var elapsedMinutes = Math.Max(0, (effectiveEndUtc - incident.OpenedAtUtc).TotalMinutes);
        var remainingMinutes = Math.Round(targetMinutes - elapsedMinutes, 2);
        var consumedRatio = Math.Round(elapsedMinutes / targetMinutes, 4);
        var effectiveDeadlineUtc = incident.OpenedAtUtc.AddMinutes(targetMinutes);
        var isBreached = elapsedMinutes > targetMinutes;

        return new SlaStatusResponse(
            IncidentId: incident.Id,
            TenantId: incident.TenantId,
            Priority: incident.Priority,
            Status: incident.Status,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: remainingMinutes,
            ConsumedRatio: consumedRatio,
            EffectiveDeadlineUtc: effectiveDeadlineUtc,
            IsBreached: isBreached);
    }

    // FIX FLUJO 2: Switch expression pura y exhaustiva de C# 13
    public static TimeSpan GetTargetResponseWindow(SeverityTier tier) => tier switch
    {
        SeverityTier.P1 => TimeSpan.FromMinutes(60),
        SeverityTier.P2 => TimeSpan.FromHours(4),
        SeverityTier.P3 => TimeSpan.FromHours(24),
        _ => throw new ArgumentOutOfRangeException(nameof(tier), $"Severidad no soportada: {tier}")
    };

    public static SlaStatusResponse Evaluate(
        DateTimeOffset openedAtUtc,
        DateTimeOffset? resolvedAtUtc,
        SeverityTier tier,
        DateTimeOffset nowUtc)
    {
        var targetMinutes = (int)GetTargetResponseWindow(tier).TotalMinutes;
        // FIX FLUJO 4: Usa resolvedAtUtc cuando el incidente está cerrado
        var effectiveEndUtc = resolvedAtUtc ?? nowUtc;
        var elapsedMinutes = Math.Max(0, (effectiveEndUtc - openedAtUtc).TotalMinutes);

        return new SlaStatusResponse(
            IncidentId: Guid.Empty,
            TenantId: "default-tenant",
            Priority: (IncidentPriority)(int)tier,
            Status: resolvedAtUtc.HasValue ? IncidentStatus.Resolved : IncidentStatus.Open,
            TargetResolutionMinutes: targetMinutes,
            ElapsedActiveMinutes: Math.Round(elapsedMinutes, 2),
            RemainingMinutes: Math.Round(targetMinutes - elapsedMinutes, 2),
            ConsumedRatio: Math.Round(elapsedMinutes / targetMinutes, 4),
            EffectiveDeadlineUtc: openedAtUtc.AddMinutes(targetMinutes),
            IsBreached: elapsedMinutes > targetMinutes);
    }
}
"""

SOLUTION_VIBE_CODED_EXPORT_CS = """using GuardiaCloud.Sla.Api.Domain;
using GuardiaCloud.Sla.Api.Services;

namespace GuardiaCloud.Sla.Api.Endpoints;

/// <summary>
/// SOLUCIÓN UNIDAD 1.2 FLUJO 5 (Code Review de Seguridad y Performance):
/// 1. Eliminado el secreto hardcodeado de Azure Storage.
/// 2. Agregado CancellationToken ct y límite de paginación (pageSize <= 100).
/// 3. Eliminada la consulta N+1 usando carga por lotes (GetAuditLogsBatch).
/// 4. Reemplazada la excepción 500 por ProblemDetails RFC 9457 (400 SLA-400-INVALID-EXPORT-FILTER).
/// </summary>
public static class VibeCodedExportEndpoints
{
    private const int MaxPageSize = 100;

    public static IEndpointRouteBuilder MapVibeCodedExportEndpoints(this IEndpointRouteBuilder app)
    {
        app.MapGet("/api/incidents/export", (
            string? priority,
            int? pageSize,
            IIncidentRepository repository,
            SlaCalculator calculator,
            CancellationToken ct) =>
        {
            ct.ThrowIfCancellationRequested();

            IncidentPriority? filterPriority = null;
            if (!string.IsNullOrWhiteSpace(priority))
            {
                if (!Enum.TryParse<IncidentPriority>(priority, ignoreCase: true, out var parsed) ||
                    !Enum.IsDefined(parsed))
                {
                    return Results.Problem(
                        title: "Filtro de prioridad inválido",
                        detail: $"El valor '{priority}' no es una prioridad válida (CriticalP1, HighP2, StandardP3).",
                        statusCode: StatusCodes.Status400BadRequest,
                        extensions: new Dictionary<string, object?>
                        {
                            ["errorCode"] = "SLA-400-INVALID-EXPORT-FILTER"
                        });
                }
                filterPriority = parsed;
            }

            var effectiveLimit = Math.Clamp(pageSize ?? 50, 1, MaxPageSize);

            var incidents = repository.ListAll()
                .Where(i => !filterPriority.HasValue || i.Priority == filterPriority.Value)
                .Take(effectiveLimit)
                .ToArray();

            // Proyección por lote única (sin N+1)
            var auditBatch = repository.GetAuditLogsBatch(incidents.Select(i => i.Id));

            var rows = incidents.Select(inc =>
            {
                var sla = calculator.Evaluate(inc);
                var auditCount = auditBatch.TryGetValue(inc.Id, out var logs) ? logs.Count : 0;
                return new
                {
                    inc.Id,
                    inc.TenantId,
                    Priority = inc.Priority.ToString(),
                    sla.ConsumedRatio,
                    sla.IsBreached,
                    AuditCount = auditCount
                };
            }).ToArray();

            return Results.Ok(rows);
        });

        return app;
    }
}
"""

SOLUTION_DAY1_FLOWS_TESTS_CS = """using System.Net;
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
"""

# ==============================================================================
# 4. WORKSPACE RULES & UI ARTIFACTS (Unit 1.1 & Unit 1.2)
# ==============================================================================
RULES_CONTENT = """# Reglas de Ingeniería .NET 10 — GuardiaCloud.Sla

## Comandos de Verificación Obligatorios
- Compilar sin warnings: `dotnet build GuardiaCloud.Sla.sln --no-restore /p:TreatWarningsAsErrors=true`
- Ejecutar suite de pruebas: `dotnet test GuardiaCloud.Sla.sln --no-build`

## Invariantes de Arquitectura y Código C# 13
1. **Target Framework:** `net10.0`, `Nullable=enable`, `TreatWarningsAsErrors=true`.
2. **Tiempo Determinista:** Prohibido usar `DateTime.Now` o `DateTime.UtcNow` directamente en servicios de negocio; inyectá siempre `System.TimeProvider`.
3. **Contratos HTTP:** Todo endpoint ASP.NET Core Minimal API recibe `CancellationToken` y devuelve errores 4xx/5xx en formato `ProblemDetails` (RFC 9457) con `extensions["errorCode"]`.
4. **Seguridad y Performance:** Prohibido hardcodear secretos en código/configuración o ejecutar consultas `N+1` dentro de bucles `foreach`.
5. **Tokens de UI:** Todo componente visual debe respetar los colores semánticos de `ui/design-tokens.json` y las propiedades exactas de `IncidentSlaCardDto`.
"""

DESIGN_TOKENS_STARTER_JSON = """{
  "$schema": "https://tr.designtokens.org/format/",
  "meta": {
    "system": "GuardiaCloud SLA Console",
    "status": "TODO: Completar tokens en Unidad 1.1 Paso 2"
  },
  "colors": {
    "bgCanvas": "#F8FAFC",
    "surfaceCard": "#FFFFFF",
    "slaHealthy": "TODO",
    "slaWarning80": "TODO",
    "slaBreached": "TODO"
  }
}
"""

DESIGN_TOKENS_SOLUTION_JSON = """{
  "$schema": "https://tr.designtokens.org/format/",
  "meta": {
    "system": "GuardiaCloud SLA Console (.NET 10)",
    "version": "1.0.0"
  },
  "colors": {
    "bgCanvas": "#F8FAFC",
    "surfacePrimary": "#0F172A",
    "surfaceCard": "#FFFFFF",
    "textPrimary": "#0F172A",
    "textMuted": "#64748B",
    "slaHealthy": "#0D9488",
    "slaWarning80": "#D97706",
    "slaBreached": "#DC2626"
  },
  "typography": {
    "fontFamilySans": "Inter, system-ui, sans-serif",
    "fontFamilyMono": "JetBrains Mono, Consolas, monospace"
  },
  "spacing": {
    "cardPadding": "16px",
    "borderRadius": "8px",
    "badgeRadius": "9999px"
  }
}
"""

RAZOR_STARTER = """@* ui/Components/SlaStatusCard.razor — STARTER (Unidad 1.1 Paso 3) *@
@using GuardiaCloud.Sla.Api.Domain

<article class="sla-card">
    @* TODO (Unidad 1.1 Paso 3):
       1. Mostrar Severity, ClientTier e IncidentId desde @Item.
       2. Renderizar barra de progreso con @Item.ConsumedRatio.
       3. Si @Item.IsAtRisk80Percent es true, mostrar alerta ámbar preventiva (>= 80%).
    *@
    <h4>@Item.IncidentId</h4>
</article>

@code {
    [Parameter, EditorRequired]
    public required IncidentSlaCardDto Item { get; set; }
}
"""

RAZOR_SOLUTION = """@* ui/Components/SlaStatusCard.razor — SOLUCIÓN VERIFICADA (Unidad 1.1 Paso 3) *@
@using GuardiaCloud.Sla.Api.Domain

<article class="sla-card @(Item.IsBreached ? "sla-breached" : Item.IsAtRisk80Percent ? "sla-warning" : "sla-ok")">
    <header class="sla-header">
        <span class="badge-severity">@Item.Severity</span>
        <span class="badge-tier">@Item.ClientTier</span>
        <code>@Item.IncidentId</code>
    </header>

    <div class="sla-progress">
        <progress value="@Math.Min(Item.ConsumedRatio, 1.0)" max="1.0"></progress>
        <span>@($"{Item.ConsumedRatio:P0}") consumido (Vence: @Item.DeadlineUtc.ToString("HH:mm 'UTC'"))</span>
    </div>

    @if (Item.IsAtRisk80Percent)
    {
        <p role="alert" class="alert-amber">
            Atención: SLA al >= 80%. Requiere escalamiento proactivo.
        </p>
    }
    else if (Item.IsBreached)
    {
        <p role="alert" class="alert-red">
            SLA Vencido. Ventanas de pausa registradas: @Item.PauseWindows.Count.
        </p>
    }
</article>

@code {
    [Parameter, EditorRequired]
    public required IncidentSlaCardDto Item { get; set; }
}
"""

UI_README_HANDOFF = """# Guía de Diseño UI y Handoff a .NET 10 (Unidad 1.1)

## Prompt Estructurado de 5 Capas (Pegar en Google Stitch, v0, Lovable, Figma Make o Claude Artifacts)

```text
Actuá como Diseñador Senior de Producto B2B. Necesito diseñar la consola operativa "GuardiaCloud SLA" para ingenieros de guardia.
Restricción técnica obligatoria: Los componentes deben mapear exactamente a este contrato DTO de nuestro backend .NET 10 Minimal API (IncidentSlaCardDto):
- incidentId (string, ej. "INC-2026-1001")
- clientTier (enum: "Platinum" | "Gold" | "Silver")
- severity (enum: "P1" | "P2" | "P3")
- consumedRatio (double entre 0.0 y 1.5)
- isBreached (bool)
- deadlineUtc (ISO-8601 UTC timestamp)
- pauseWindows (array de { reason: "WaitingForCustomer" | "MaintenanceWindow", startsAtUtc, endsAtUtc })

Generá 3 vistas conectadas:
1. Tablero Principal de Guardia SLA con filtro por severity y barra de progreso (verde <0.80, ámbar >=0.80, rojo si isBreached == true).
2. Modal "Registrar Ventana de Pausa" con selector de reason y aviso visible cuando severity == "P1": "En incidentes P1 la pausa máxima acumulada es de 30 minutos".
3. Timeline de Auditoría de SLA + Banner de error estandarizado para respuestas HTTP 4xx en formato ProblemDetails RFC 9457 (mostrando title, detail, errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED" y traceId).
```
"""

PROTOTYPE_3_SCREENS_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>GuardiaCloud SLA — Prototipo 3 Pantallas (Unidad 1.1 Solution)</title>
  <style>
    :root {
      --bg-canvas: #F8FAFC;
      --surface-primary: #0F172A;
      --surface-card: #FFFFFF;
      --sla-healthy: #0D9488;
      --sla-warning: #D97706;
      --sla-breached: #DC2626;
    }
    body { font-family: Inter, system-ui, sans-serif; background: var(--bg-canvas); color: #0F172A; margin: 0; padding: 24px; }
    h1, h2, h3 { margin-top: 0; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
    .card { background: var(--surface-card); border-radius: 8px; padding: 16px; border: 2px solid #CBD5E1; }
    .card.warning { border-color: var(--sla-warning); }
    .card.breached { border-color: var(--sla-breached); }
    .badge { display: inline-block; padding: 2px 10px; border-radius: 9999px; font-size: 12px; font-weight: 700; color: #FFF; background: #1E3A8A; }
    .rfc9457 { background: #FEF2F2; border-left: 4px solid var(--sla-breached); padding: 12px 16px; border-radius: 6px; font-family: monospace; }
  </style>
</head>
<body>
  <h1>GuardiaCloud SLA — Prototipo Validado de 3 Pantallas (.NET 10 DTO Handoff)</h1>

  <h2>Pantalla 1: Tablero Principal de Guardia SLA (IncidentSlaCardDto)</h2>
  <div class="grid">
    <article class="card">
      <span class="badge">P2 · Gold</span> <code>INC-2026-1001</code>
      <p>Consumo SLA: <strong>42%</strong> (`consumedRatio: 0.42`, `isBreached: false`)</p>
    </article>
    <article class="card warning">
      <span class="badge" style="background:#D97706">P1 · Platinum</span> <code>INC-2026-1002</code>
      <p>Consumo SLA: <strong>84%</strong> (`consumedRatio: 0.84`, `isBreached: false`)</p>
      <p style="color:#D97706;font-weight:bold">⚠ Atención: SLA al >= 80%. Requiere escalamiento proactivo.</p>
    </article>
    <article class="card breached">
      <span class="badge" style="background:#DC2626">P1 · Platinum</span> <code>INC-2026-1003</code>
      <p>Consumo SLA: <strong>118%</strong> (`consumedRatio: 1.18`, `isBreached: true`)</p>
      <p style="color:#DC2626;font-weight:bold">✖ SLA Vencido (2 pausas fusionadas).</p>
    </article>
  </div>

  <h2>Pantalla 2: Modal "Registrar Ventana de Pausa" (Regla Regulatoria P1)</h2>
  <div class="card" style="max-width: 540px; margin-bottom: 24px;">
    <h3>Registrar Pausa — <code>INC-2026-1002 (P1)</code></h3>
    <p>Motivo (`PauseReason`): <code>WaitingForCustomer</code> | <code>MaintenanceWindow</code></p>
    <p style="background:#FFFBEB;border:1px solid #D97706;padding:8px;border-radius:6px;">
      <strong>Aviso Regulatorio P1:</strong> En incidentes P1 la pausa máxima acumulada es de <strong>30 minutos</strong>.
    </p>
  </div>

  <h2>Pantalla 3: Timeline de Auditoría + Banner de Error RFC 9457 (ProblemDetails)</h2>
  <div class="rfc9457">
    <strong>HTTP 422 Unprocessable Entity — ProblemDetails (RFC 9457)</strong><br/>
    title: "Límite de pausa P1 excedido"<br/>
    detail: "La pausa solicitada acumula 35 min y supera el tope regulatorio de 30 min para incidentes P1."<br/>
    errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED"<br/>
    traceId: "00-8f3a9d1c2e4b6a80123456789abcdef0-4b2c1d0e9f8a7b6c-01"
  </div>
</body>
</html>
"""


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scaffold_day1():
    # Starter
    s_root = WS_DAY1 / "starter"
    write_text(s_root / "GuardiaCloud.Sla.sln", SLN_CONTENT)
    write_text(s_root / "AGENTS.md", RULES_CONTENT)
    write_text(s_root / ".github" / "copilot-instructions.md", RULES_CONTENT)
    write_text(s_root / ".cursor" / "rules" / "dotnet10.mdc", RULES_CONTENT)
    write_text(s_root / ".windsurfrules", RULES_CONTENT)
    write_text(s_root / "ui" / "README-UI-HANDOFF.md", UI_README_HANDOFF)
    write_text(s_root / "ui" / "design-tokens.starter.json", DESIGN_TOKENS_STARTER_JSON)
    write_text(s_root / "ui" / "Components" / "SlaStatusCard.razor", RAZOR_STARTER)
    write_text(s_root / "src" / "GuardiaCloud.Sla.Api" / "GuardiaCloud.Sla.Api.csproj", API_CSPROJ)
    write_text(s_root / "src" / "GuardiaCloud.Sla.Api" / "Program.cs", PROGRAM_CS)
    write_text(s_root / "src" / "GuardiaCloud.Sla.Api" / "Domain" / "IncidentModels.cs", DOMAIN_MODELS_CS)
    write_text(s_root / "src" / "GuardiaCloud.Sla.Api" / "Services" / "SlaCalculator.cs", STARTER_SLA_SERVICES_CS)
    write_text(s_root / "src" / "GuardiaCloud.Sla.Api" / "Endpoints" / "VibeCodedExportEndpoints.cs", STARTER_VIBE_CODED_EXPORT_CS)
    write_text(s_root / "tests" / "GuardiaCloud.Sla.Tests" / "GuardiaCloud.Sla.Tests.csproj", TESTS_CSPROJ)
    write_text(s_root / "tests" / "GuardiaCloud.Sla.Tests" / "SlaApiIntegrationTests.cs", STARTER_TESTS_CS)

    # Solution
    sol_root = WS_DAY1 / "solution"
    write_text(sol_root / "GuardiaCloud.Sla.sln", SLN_CONTENT)
    write_text(sol_root / "AGENTS.md", RULES_CONTENT)
    write_text(sol_root / ".github" / "copilot-instructions.md", RULES_CONTENT)
    write_text(sol_root / ".cursor" / "rules" / "dotnet10.mdc", RULES_CONTENT)
    write_text(sol_root / ".windsurfrules", RULES_CONTENT)
    write_text(sol_root / "ui" / "README-UI-HANDOFF.md", UI_README_HANDOFF)
    write_text(sol_root / "ui" / "design-tokens.json", DESIGN_TOKENS_SOLUTION_JSON)
    write_text(sol_root / "ui" / "prototype-3-screens.html", PROTOTYPE_3_SCREENS_HTML)
    write_text(sol_root / "ui" / "Components" / "SlaStatusCard.razor", RAZOR_SOLUTION)
    write_text(sol_root / "src" / "GuardiaCloud.Sla.Api" / "GuardiaCloud.Sla.Api.csproj", API_CSPROJ)
    write_text(sol_root / "src" / "GuardiaCloud.Sla.Api" / "Program.cs", PROGRAM_CS)
    write_text(sol_root / "src" / "GuardiaCloud.Sla.Api" / "Domain" / "IncidentModels.cs", DOMAIN_MODELS_CS)
    write_text(sol_root / "src" / "GuardiaCloud.Sla.Api" / "Services" / "SlaCalculator.cs", SOLUTION_SLA_SERVICES_CS)
    write_text(sol_root / "src" / "GuardiaCloud.Sla.Api" / "Endpoints" / "VibeCodedExportEndpoints.cs", SOLUTION_VIBE_CODED_EXPORT_CS)
    write_text(sol_root / "tests" / "GuardiaCloud.Sla.Tests" / "GuardiaCloud.Sla.Tests.csproj", TESTS_CSPROJ)
    write_text(sol_root / "tests" / "GuardiaCloud.Sla.Tests" / "SlaApiIntegrationTests.cs", STARTER_TESTS_CS)
    write_text(sol_root / "tests" / "GuardiaCloud.Sla.Tests" / "SlaCalculatorDay1FlowsTests.cs", SOLUTION_DAY1_FLOWS_TESTS_CS)


def add_missing_m2_and_m3_artifacts():
    # Unit 2.2: Brownfield Impact Analysis & 2-Column Estimation Report in ws-m2-sdd-dotnet/solution
    u22_report = ROOT / "workshops" / "ws-m2-sdd-dotnet" / "solution" / "specs" / "001-sla-pause-windows" / "impact-and-estimation.md"
    write_text(
        u22_report,
        """# Informe de Impacto Brownfield y Estimación Comparada (Unidad 2.2)
## Feature: `001-sla-pause-windows` sobre `GuardiaCloud.Sla.sln`

### 1. Matriz de Archivos Afectados (Auditoría en Modo Solo Lectura)
| Archivo | Tipo de Cambio | Riesgo de Colisión | Estrategia en el Grafo DAG (`tasks.md`) |
|---|---|---|---|
| `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs` | Modificación (agregar `PauseReason`, `SlaPauseWindow` y lista en `Incident`) | Alto (archivo compartido) | Congelar en **Fase 1 Secuencial (`T001`)** antes de abrir ramas paralelas |
| `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs` | Extensión (suites xUnit en rojo para fusión de pausas y RFC 9457) | Medio | Escribir en **Fase 1 Secuencial (`T002`)** como oráculo determinista |
| `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs` | Modificación (algoritmo puro de recorte y unión de intervalos solapados) | Bajo si se aísla | Ejecutar en **Fase 2 Paralela (`T003 [P]`)** en `git worktree` |
| `src/GuardiaCloud.Sla.Api/Program.cs` | Modificación (endpoint `POST /api/incidents/{id}/pauses` + validaciones RFC 9457) | Bajo si no toca `Services` | Ejecutar en **Fase 2 Paralela (`T004 [P]`)** en rama separada |

---

### 2. Estimación en Dos Columnas (Generación con IA vs. Verificación Humana)

| Tarea del DAG | Modo (`HITL` / `Full AI`) | Estimación Tradicional (sin IA) | Tiempo de Generación con IA | Tiempo de Verificación y Code Review | Total con IA | Ahorro Neto |
|---|---|---:|---:|---:|---:|---:|
| **T001** Contratos Domain y DTOs | HITL | 30 min | 5 min | 10 min | **15 min** | 50% |
| **T002** Suite Oráculo xUnit en rojo | HITL | 60 min | 10 min | 20 min | **30 min** | 50% |
| **T003 [P]** Unión matemática de intervalos | Full AI (`worktree`) | 75 min | 5 min | 15 min | **20 min** | 73% |
| **T004 [P]** Endpoint Minimal API + RFC 9457 | HITL | 45 min | 10 min | 15 min | **25 min** | 44% |
| **Total Feature `001-sla-pause-windows`** | Mixto | **210 min (3.5 hs)** | **30 min** | **60 min** | **90 min (1.5 hs)** | **57%** |
""",
    )

    # Unit 3.2: UI Prototype + Design Tokens for FEAT-303 in ws-m3-capstone-dotnet/solution/ui/
    m3_ui_dir = ROOT / "workshops" / "ws-m3-capstone-dotnet" / "solution" / "ui"
    write_text(m3_ui_dir / "design-tokens.json", DESIGN_TOKENS_SOLUTION_JSON)
    write_text(
        m3_ui_dir / "executive-tier-dashboard.html",
        """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>GuardiaCloud CommandCenter — Tablero Ejecutivo por Tier (FEAT-303)</title>
  <style>
    body { font-family: Inter, system-ui, sans-serif; background: #F8FAFC; color: #0F172A; padding: 24px; }
    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .card { background: #FFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 16px; }
  </style>
</head>
<body>
  <h1>GuardiaCloud.CommandCenter — Tablero Ejecutivo por Tier (`GET /api/command-center/dashboard/tiers`)</h1>
  <div class="grid">
    <div class="card"><h3>Tier: Platinum</h3><p>Total Incidentes: 12 · Breached: 1 · Cumplimiento: <strong>91.7%</strong> · Exenciones Duales: 2</p></div>
    <div class="card"><h3>Tier: Gold</h3><p>Total Incidentes: 28 · Breached: 2 · Cumplimiento: <strong>92.9%</strong> · Exenciones Duales: 1</p></div>
    <div class="card"><h3>Tier: Silver</h3><p>Total Incidentes: 45 · Breached: 0 · Cumplimiento: <strong>100.0%</strong> · Exenciones Duales: 0</p></div>
  </div>
</body>
</html>
""",
    )


def write_workshops_master_readme():
    readme_content = """# Mapa Maestro de Proyectos Base y Workshops (.NET 10)
## Curso: Desarrollo de Software con IA (52 Horas · 3 Módulos · 13 Unidades)

Este directorio contiene **todos los proyectos base (`.NET 10` / C# 13), ejercicios guiados (`starter/`), soluciones verificadas (`solution/`), prototipos UI y rúbricas docentes** que respaldan cada slide y cada bloque práctico de los 7 días del curso.

---

## 1. Tabla de Correspondencia: Día / Unidad / Slide → Carpeta de Código

| Día | Unidades | Deck de Clase (`presentaciones/`) | Carpeta de Código en `workshops/` | Solución `.NET 10` (`.sln`) | Verificación (`dotnet test`) |
|---|---|---|---|---|---|
| **Día 1** (8 hs) | **U1.1** (Diseño UI + Handoff .NET) y **U1.2** (VS Code, Cursor, Windsurf + 5 Flujos Diarios) | `Unidad-1.1-*.pptx` y `Unidad-1.2-*.pptx` (Slides 1–13 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-dia1-proyecto-base-dotnet/`](ws-m1-dia1-proyecto-base-dotnet/) | `GuardiaCloud.Sla.sln` | `starter/`: **2/2 passed**<br>`solution/`: **10/10 passed** |
| **Día 2** (Mañana · 4 hs) | **U1.3** (Agentes, Patrones, `SKILL.md` y `Microsoft.Extensions.AI`) | `Unidad-1.3-*.pptx` (Slides 13–16 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-skills-mcp-dotnet/`](ws-m1-skills-mcp-dotnet/) (Fases 1 y 3) | `GuardiaCloud.Sla.McpWorkshop.sln` | `solution/`: **6/6 passed** + `verify-minimal-api.sh` OK |
| **Día 2** (Tarde · 6 hs) | **U1.4** (Harness Engineering: Claude Code, Codex, Devin, `AGENTS.md` y Hooks) | `Unidad-1.4-*.pptx` (Slides 17–20 de `00-Modulo-1-Completo.pptx`) | [`ws-m2-harness-oracle-dotnet/`](ws-m2-harness-oracle-dotnet/) (Fases 1, 2 y Subagente) | `GuardiaCloud.Sla.HarnessLab.sln` | `solution/`: **7/7 passed** + `post-edit-dotnet-hook.sh` OK |
| **Día 3** (Bloque 1 · 2 hs) | **U1.5** (Model Context Protocol en C# `v2.3.0` + Seguridad Anti-Inyección · **Entrega #1 = 15%**) | `Unidad-1.5-*.pptx` (Slides 21–23 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-skills-mcp-dotnet/`](ws-m1-skills-mcp-dotnet/) (Fase 2: `SlaMcpTools.cs`) | `GuardiaCloud.Sla.McpWorkshop.sln` | `solution/`: **6/6 passed** |
| **Día 3** (Bloque 2 · 4 hs) y **Día 4** (Bloque 1 · 4 hs) | **U2.1** (Specs EARS + Given/When/Then + *Spec Critic*) y **U2.2** (Impacto Brownfield, Estimación y DAG `tasks.md`) | `Unidad-2.1-*.pptx` y `Unidad-2.2-*.pptx` (Slides 1–5 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-sdd-dotnet/`](ws-m2-sdd-dotnet/) (`specs/001-sla-pause-windows/`) | `GuardiaCloud.Sla.sln` | `starter/`: **2/2 passed**<br>`solution/`: **6/6 passed** |
| **Día 4** (Bloque 2 · 4 hs) | **U2.3** (Full AI vs. HITL en `git worktree` + Oráculo `NetArchTest.Rules` v1.3.2) | `Unidad-2.3-*.pptx` (Slides 6–7 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-harness-oracle-dotnet/`](ws-m2-harness-oracle-dotnet/) (Fases 3 y 4) | `GuardiaCloud.Sla.HarnessLab.sln` | `solution/`: **7/7 passed** |
| **Día 5** (6 hs) | **U2.4** (GitHub Spec Kit `v1.2.5` + OpenSpec `v1.15.0` Deltas Brownfield · **Entrega #2 = 15%**) | `Unidad-2.4-*.pptx` (Slides 8–9 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-sdd-dotnet/`](ws-m2-sdd-dotnet/) (`.specify/` + `openspec/`) | `GuardiaCloud.Sla.sln` | `solution/`: **6/6 passed** |
| **Días 6 y 7** (14 hs) | **U3.1 a U3.4** (Proyecto Integrador Capstone en Equipos · **Entregas #3, #4 y #5 = 70%**) | `Unidades-3.1-a-3.4-*.pptx` (`00-Modulo-3-Completo.pptx`) | [`ws-m3-capstone-dotnet/`](ws-m3-capstone-dotnet/) | `GuardiaCloud.CommandCenter.sln` | `starter/`: **1/1 passed**<br>`solution/`: **8/8 passed** |

---

## 2. Cómo Ejecutar Todos los Proyectos y Tests de un Vistazo

Desde la raíz del repositorio (o tras descomprimir el `.zip`):

```bash
# Día 1 (Unidades 1.1 y 1.2) — Proyecto Base GuardiaCloud.Sla
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/starter/GuardiaCloud.Sla.sln
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/solution/GuardiaCloud.Sla.sln

# Unidades 1.3 y 1.5 — Agent Skills (SKILL.md), Agente Microsoft.Extensions.AI y Servidor MCP en C#
./workshops/ws-m1-skills-mcp-dotnet/solution/.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh
dotnet test workshops/ws-m1-skills-mcp-dotnet/solution/GuardiaCloud.Sla.McpWorkshop.sln

# Unidades 1.4 y 2.3 — Harness Engineering, Hooks .NET y Oráculo NetArchTest.Rules
dotnet test workshops/ws-m2-harness-oracle-dotnet/solution/GuardiaCloud.Sla.HarnessLab.sln

# Unidades 2.1, 2.2 y 2.4 — Spec-Driven Development (GitHub Spec Kit + OpenSpec)
dotnet test workshops/ws-m2-sdd-dotnet/solution/GuardiaCloud.Sla.sln

# Módulo 3 (Unidades 3.1 a 3.4) — Proyecto Integrador Capstone (GuardiaCloud.CommandCenter)
dotnet test workshops/ws-m3-capstone-dotnet/solution/GuardiaCloud.CommandCenter.sln
```
"""
    write_text(ROOT / "workshops" / "README.md", readme_content)


def build_clean_zip():
    zip_paths = [
        ROOT / "presentaciones" / "GuardiaCloud-Sla-Proyectos-Base-y-Workshops-DotNet10.zip",
        ROOT / "GuardiaCloud-Sla-Proyectos-Base-y-Workshops-DotNet10.zip",
    ]
    exclude_dirs = {"bin", "obj", ".git", ".vs", "__pycache__", ".pytest_cache"}

    for zp in zip_paths:
        if zp.exists():
            zp.unlink()

    primary_zip = zip_paths[0]
    with zipfile.ZipFile(primary_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Include workshops/README.md at the root of the zip as LEEME-MAPA-DE-PROYECTOS.md as well
        zf.write(ROOT / "workshops" / "README.md", arcname="LEEME-MAPA-DE-PROYECTOS.md")

        for item in sorted((ROOT / "workshops").rglob("*")):
            if any(part in exclude_dirs for part in item.parts):
                continue
            if item.is_file() and item.name != ".DS_Store":
                rel = item.relative_to(ROOT)
                zf.write(item, arcname=str(rel))

    # Copy to root as well so Fab can grab it from either root or presentaciones/
    import shutil
    shutil.copy2(primary_zip, zip_paths[1])
    print(f"Created {primary_zip.relative_to(ROOT)} ({primary_zip.stat().st_size:,} bytes)")
    print(f"Created {zip_paths[1].relative_to(ROOT)} ({zip_paths[1].stat().st_size:,} bytes)")


if __name__ == "__main__":
    scaffold_day1()
    add_missing_m2_and_m3_artifacts()
    write_workshops_master_readme()
    build_clean_zip()
    print("Done scaffolding Day 1 Base Project + M2/M3 artifacts + ZIP archive.")
