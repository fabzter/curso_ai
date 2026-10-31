# Especificación Técnica (.NET 10): GuardiaCloud Command Center v2.0

## 1. Contratos HTTP y Catálogo RFC 9457 (`ProblemDetails`)

| Endpoint | Método | Respuesta Exitosa | Errores RFC 9457 (`extensions["errorCode"]`) |
|---|---|---|---|
| `/api/command-center/webhooks/incident-event` | `POST` | `200 OK` (`WebhookProcessingResult`) | `404` (`CC-404-INCIDENT-NOT-FOUND`) |
| `/api/command-center/escalations/evaluate/{incidentId}` | `POST` | `200 OK` (`ProactiveEscalationResult`) | `404` (`CC-404-INCIDENT-NOT-FOUND`) |
| `/api/command-center/exemptions` | `POST` | `200 OK` (`ForceMajeureExemption`) | `404` (`CC-404-INCIDENT-NOT-FOUND`), `400` (`CC-400-SAME-APPROVER`), `422` (`CC-422-INVALID-DUAL-TOKEN`) |
| `/api/command-center/dashboard/{clientTier}` | `GET` | `200 OK` (`TierExecutiveDashboardDto`) | `400` (`CC-400-INVALID-CLIENT-TIER`) |

## 2. Decisiones de Arquitectura (ADRs)
- **ADR-01 (Deduplicación de Webhooks):** Se utiliza el conjunto `ProcessedWebhookEventIds` (`HashSet<string>` con `StringComparer.Ordinal`) por entidad `CommandCenterIncident` para garantizar complejidad $O(1)$ e idempotencia determinista.
- **ADR-02 (Oráculo de Arquitectura `NetArchTest`):** Toda la lógica de negocio reside en `CommandCenterEvaluator` (`sealed`, sin referencias a `Infrastructure` ni `HttpContext`, dependiendo únicamente de `System.TimeProvider`).
