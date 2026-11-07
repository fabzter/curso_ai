using GuardiaCloud.Sla.Api.Domain;
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
