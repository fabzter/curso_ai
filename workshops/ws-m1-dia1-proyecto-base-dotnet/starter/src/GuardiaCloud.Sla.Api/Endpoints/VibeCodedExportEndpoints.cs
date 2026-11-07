using GuardiaCloud.Sla.Api.Domain;
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
