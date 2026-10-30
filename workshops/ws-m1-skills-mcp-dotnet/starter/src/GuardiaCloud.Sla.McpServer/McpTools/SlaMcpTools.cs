using System.ComponentModel;
using GuardiaCloud.Sla.McpServer.Domain;
using GuardiaCloud.Sla.McpServer.Infrastructure;
using ModelContextProtocol.Server;

namespace GuardiaCloud.Sla.McpServer.McpTools;

[McpServerToolType]
public sealed class SlaMcpTools(InMemorySlaCatalogStore catalogStore, TimeProvider timeProvider)
{
    private readonly InMemorySlaCatalogStore _catalogStore = catalogStore;
    private readonly TimeProvider _timeProvider = timeProvider;

    [McpServerTool(
        Name = "get_client_sla_policy",
        Title = "Consultar Política Contractual de SLA",
        ReadOnly = true,
        Idempotent = true,
        Destructive = false,
        OpenWorld = false)]
    [Description("Devuelve el objetivo de resolución en minutos, el tope de pausa permitido y la penalidad por hora para un tier de cliente (Bancario-Tier1, Aseguradora-Gold, Retail-Standard) y una severidad (P1, P2, P3).")]
    public ClientSlaPolicy GetClientSlaPolicy(
        [Description("Tier contractual del cliente: Bancario-Tier1, Aseguradora-Gold o Retail-Standard.")] string clientTier,
        [Description("Severidad del incidente: P1, P2 o P3.")] string severity)
    {
        if (string.IsNullOrWhiteSpace(clientTier) || !InMemorySlaCatalogStore.AllowedClientTiers.Contains(clientTier.Trim()))
        {
            throw new ArgumentException(
                $"SLA-400-INVALID-CLIENT-TIER: El tier '{clientTier}' no es válido. Valores permitidos: Bancario-Tier1, Aseguradora-Gold, Retail-Standard.",
                nameof(clientTier));
        }

        if (string.IsNullOrWhiteSpace(severity) || !InMemorySlaCatalogStore.AllowedSeverities.Contains(severity.Trim()))
        {
            throw new ArgumentException(
                $"SLA-400-INVALID-SEVERITY: La severidad '{severity}' no es válida. Valores permitidos: P1, P2, P3.",
                nameof(severity));
        }

        return _catalogStore.FindPolicy(clientTier, severity)
            ?? throw new InvalidOperationException($"No se encontró política configurada para {clientTier}/{severity}.");
    }

    // TODO (Fase 2 - Unidad 1.5): Decorar con [McpServerTool(Name = "inspect_incident_sla_status", ReadOnly = true, Idempotent = true, Destructive = false, OpenWorld = false)]
    // y [Description(...)], calcular el tiempo efectivo usando _timeProvider.GetUtcNow() (o ResolvedAtUtc si ya cerró),
    // sanitizar IncidentRecord.Summary con InMemorySlaCatalogStore.SanitizeUntrustedNotes(...) y devolver IncidentSlaAuditDto.
    public IncidentSlaAuditDto InspectIncidentSlaStatus(string incidentId)
    {
        _ = _timeProvider;
        throw new NotImplementedException("TODO (Fase 2 - Unidad 1.5): Implementar inspect_incident_sla_status y exponerla como McpServerTool.");
    }

    // TODO (Fase 2 - Unidad 1.5): Decorar con [McpServerTool(Name = "validate_rfc9457_contract", ReadOnly = true, Idempotent = true, Destructive = false, OpenWorld = false)]
    // y [Description(...)], validando errorCode, statusCode y typeUri contra InMemorySlaCatalogStore.CanonicalErrorCatalog.
    public Rfc9457ValidationResult ValidateRfc9457Contract(string errorCode, int httpStatus, string typeUri)
    {
        throw new NotImplementedException("TODO (Fase 2 - Unidad 1.5): Implementar validate_rfc9457_contract y exponerla como McpServerTool.");
    }
}
