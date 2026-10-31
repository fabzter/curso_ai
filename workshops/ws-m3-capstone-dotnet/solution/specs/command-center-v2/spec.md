# Especificación Funcional: GuardiaCloud Command Center v2.0 (Entregable #3 — Unidad 3.2)

- **Estado:** Aprobada tras entrevista con el cliente (Unidad 3.1) y revisión adversarial cruzada (Unidad 3.2).
- **Alcance comprometido:** `BUG-301`, `FEAT-301`, `FEAT-302` y `FEAT-303`.

---

## 1. Requerimientos en Notación EARS

### R1 — Idempotencia de Webhooks de Incidentes (`BUG-301`)
- **WHEN** `POST /api/command-center/webhooks/incident-event` recibe un `IncidentWebhookEventRequest` cuyo `EventId` ya fue procesado previamente para ese `IncidentId`, **THE SYSTEM SHALL** ignorar el incremento de minutos pausados y de penalidades, devolviendo `HTTP 200 OK` con `WasDuplicateIgnored = true`.

### R2 — Escalamiento Proactivo al 80% con Cooldown de 15 Minutos (`FEAT-301`)
- **WHEN** `POST /api/command-center/escalations/evaluate/{incidentId}` es invocado sobre un incidente abierto cuyo consumo de SLA es `>= 80.0%`, **WHILE** no exista una alerta previa enviada en los últimos **15 minutos** (`LastEscalationSentAtUtc`), **THE SYSTEM SHALL** registrar `LastEscalationSentAtUtc = TimeProvider.GetUtcNow()` y devolver `ShouldDispatchAlert = true` con `ReasonCode = "ALERT_DISPATCHED"`.
- **IF** se vuelve a evaluar el mismo incidente dentro de la ventana de 15 minutos, **THEN THE SYSTEM SHALL** devolver `ShouldDispatchAlert = false` con `ReasonCode = "COOLDOWN_ACTIVE_15M"`.

### R3 — Aprobación Dual de Exenciones por Fuerza Mayor (`FEAT-302`)
- **WHEN** `POST /api/command-center/exemptions` recibe una solicitud válida con dos aprobadores distintos (`PrimaryApproverEmail != SecondaryApproverEmail`, case-insensitive) y un `DualApprovalToken` con prefijo `"FM-DUAL-"`, **THE SYSTEM SHALL** asociar la exención al incidente y excluirlo del cálculo de exposición financiera.
- **IF** `PrimaryApproverEmail` y `SecondaryApproverEmail` son iguales, **THEN THE SYSTEM SHALL** rechazar la solicitud con `HTTP 400 Bad Request` (`ProblemDetails` RFC 9457, `errorCode = "CC-400-SAME-APPROVER"`).
- **IF** `DualApprovalToken` no comienza con `"FM-DUAL-"`, **THEN THE SYSTEM SHALL** rechazar la solicitud con `HTTP 422 Unprocessable Entity` (`ProblemDetails` RFC 9457, `errorCode = "CC-422-INVALID-DUAL-TOKEN"`).

### R4 — Tablero Ejecutivo Consolidado por Tier (`FEAT-303`)
- **WHEN** `GET /api/command-center/dashboard/{clientTier}` es consultado para un tier válido (`Bancario-Tier1`, `Aseguradora-Gold`, `Retail-Standard`), **THE SYSTEM SHALL** devolver `TierExecutiveDashboardDto` calculando:
  - `BreachedIncidents`: cantidad de incidentes con `ConsumedPercentage > 100.0`.
  - `AtRiskIncidents`: cantidad de incidentes con `80.0 <= ConsumedPercentage <= 100.0`.
  - `ExemptedIncidents`: cantidad de incidentes con `Exemption != null`.
  - `TotalFinancialExposureUsd`: suma de `PenaltyPerBreachUsd` únicamente de los incidentes vencidos (`> 100.0%`) que **no** posean exención activa.

---

## 2. Escenarios de Aceptación (Given / When / Then)

1. **Escenario GWT-301 (Webhook duplicado):**
   - *Given* el incidente `INC-2026-3001` con `PausedMinutes = 0` y `AppliedPenaltyEventsCount = 0`
   - *When* se envía dos veces el webhook con `EventId = "EVT-9001"`, `AdditionalPausedMinutes = 5` y `TriggerPenaltyIncrement = true`
   - *Then* la primera llamada devuelve `WasDuplicateIgnored = false` (`PausedMinutes = 5`, `AppliedPenaltyEventsCount = 1`) y la segunda devuelve `WasDuplicateIgnored = true` manteniendo `PausedMinutes = 5` y `AppliedPenaltyEventsCount = 1`.
2. **Escenario GWT-302 (Alerta al 80% y Cooldown):**
   - *Given* `INC-2026-3001` con `86.67%` de consumo de SLA y sin alertas previas
   - *When* se evalúa el escalamiento dos veces seguidas en el mismo minuto
   - *Then* la primera llamada devuelve `ShouldDispatchAlert = true` (`ALERT_DISPATCHED`) y la segunda devuelve `ShouldDispatchAlert = false` (`COOLDOWN_ACTIVE_15M`).
3. **Escenario GWT-303 (Exención reduce exposición financiera en el Dashboard):**
   - *Given* `Bancario-Tier1` con dos incidentes vencidos (`INC-2026-3002` con USD 2500 y `INC-2026-3003` con USD 800 $\rightarrow$ USD 3300 de exposición total)
   - *When* se registra una exención válida (`FM-DUAL-BCRA-99`) sobre `INC-2026-3002` y se consulta `GET /api/command-center/dashboard/Bancario-Tier1`
   - *Then* `ExemptedIncidents` pasa a `1` y `TotalFinancialExposureUsd` baja de `3300.00` a `800.00`.
