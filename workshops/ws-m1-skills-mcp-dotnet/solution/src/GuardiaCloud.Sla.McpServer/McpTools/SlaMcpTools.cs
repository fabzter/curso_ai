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

    [McpServerTool(
        Name = "inspect_incident_sla_status",
        Title = "Auditar Estado de SLA de un Incidente",
        ReadOnly = true,
        Idempotent = true,
        Destructive = false,
        OpenWorld = false)]
    [Description("Audita en tiempo real el consumo de SLA de un incidente (ej. INC-2026-1001), descontando minutos pausados válidos, sanitizando notas no confiables y determinando si está en riesgo (>=80%) o vencido (>100%).")]
    public IncidentSlaAuditDto InspectIncidentSlaStatus(
        [Description("Identificador único del incidente (ej. INC-2026-1001, INC-2026-1002, INC-2026-1003).")] string incidentId)
    {
        if (string.IsNullOrWhiteSpace(incidentId))
        {
            throw new ArgumentException("SLA-404-INCIDENT-NOT-FOUND: El identificador de incidente no puede ser vacío.", nameof(incidentId));
        }

        var incident = _catalogStore.FindIncident(incidentId)
            ?? throw new KeyNotFoundException($"SLA-404-INCIDENT-NOT-FOUND: No existe el incidente '{incidentId}'.");

        var policy = GetClientSlaPolicy(incident.ClientTier, incident.Severity);
        var effectiveEndUtc = incident.ResolvedAtUtc ?? _timeProvider.GetUtcNow();
        var rawElapsedMinutes = Math.Max(0, (effectiveEndUtc - incident.OpenedAtUtc).TotalMinutes);
        var cappedPauseMinutes = Math.Min(incident.AccumulatedPauseMinutes, policy.MaxAllowedPauseMinutes);
        var effectiveElapsedMinutes = Math.Round(Math.Max(0, rawElapsedMinutes - cappedPauseMinutes), 2);
        var consumedPercentage = Math.Round((effectiveElapsedMinutes / policy.TargetResolutionMinutes) * 100.0, 2);

        var isBreached = effectiveElapsedMinutes > policy.TargetResolutionMinutes;
        var isAtRisk = !isBreached && consumedPercentage >= 80.0;
        var status = isBreached
            ? "BREACHED"
            : isAtRisk
                ? "AT_RISK"
                : incident.ResolvedAtUtc.HasValue
                    ? "RESOLVED_WITHIN_SLA"
                    : "HEALTHY";

        var sanitizedSummary = InMemorySlaCatalogStore.SanitizeUntrustedNotes(incident.Summary);
        var recommendedAction = isBreached
            ? $"Escalar de inmediato a {policy.EscalationChannel} (penalidad activa: USD {policy.PenaltyPerHourUsd}/h)."
            : isAtRisk
                ? $"Alerta preventiva (>=80% del SLA): notificar en {policy.EscalationChannel}."
                : "Mantener monitoreo estándar dentro de ventana contractual.";

        return new IncidentSlaAuditDto(
            incident.IncidentId,
            incident.ClientTier,
            incident.Severity,
            effectiveElapsedMinutes,
            policy.TargetResolutionMinutes,
            consumedPercentage,
            status,
            isBreached,
            isAtRisk,
            sanitizedSummary,
            recommendedAction);
    }

    [McpServerTool(
        Name = "validate_rfc9457_contract",
        Title = "Validar Contrato de Error RFC 9457 (ProblemDetails)",
        ReadOnly = true,
        Idempotent = true,
        Destructive = false,
        OpenWorld = false)]
    [Description("Verifica determinísticamente si un código de error (errorCode), statusCode HTTP y URI type cumplen el catálogo oficial RFC 9457 de GuardiaCloud.Sla.")]
    public Rfc9457ValidationResult ValidateRfc9457Contract(
        [Description("Código canónico en extensions['errorCode'], ej. SLA-400-INVALID-SEVERITY.")] string errorCode,
        [Description("Código de estado HTTP numérico devuelto por el endpoint (400, 404, 409, 422).")] int httpStatus,
        [Description("URI type declarada en el ProblemDetails.")] string typeUri)
    {
        var violations = new List<string>();
        var normalizedCode = errorCode?.Trim() ?? string.Empty;

        if (!InMemorySlaCatalogStore.CanonicalErrorCatalog.TryGetValue(normalizedCode, out var expected))
        {
            violations.Add($"El código '{normalizedCode}' no existe en el catálogo oficial RFC 9457 de GuardiaCloud.");
            return new Rfc9457ValidationResult(false, normalizedCode, 0, string.Empty, violations);
        }

        if (httpStatus != expected.HttpStatus)
        {
            violations.Add($"HTTP status inválido para '{normalizedCode}': se recibió {httpStatus}, pero el catálogo exige {expected.HttpStatus}.");
        }

        if (!string.Equals(typeUri?.Trim(), expected.TypeUri, StringComparison.Ordinal))
        {
            violations.Add($"URI 'type' inválida para '{normalizedCode}': se recibió '{typeUri}', pero el catálogo exige '{expected.TypeUri}'.");
        }

        return new Rfc9457ValidationResult(
            violations.Count == 0,
            normalizedCode,
            expected.HttpStatus,
            expected.TypeUri,
            violations);
    }
}
