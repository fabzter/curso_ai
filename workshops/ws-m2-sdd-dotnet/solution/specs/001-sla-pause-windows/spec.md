# Feature Specification: Ventanas de Pausa y Reanudación Auditable de SLA (`001-sla-pause-windows`)

**Feature Branch**: `001-sla-pause-windows`  
**Created**: 2026-10-30  
**Status**: Converged  
**Input**: Pedido de Operaciones (`brief-cliente-ambiguo.md`) refinado mediante Auditoría Adversarial + `/speckit-specify` + `/speckit-clarify`.

---

## Decisiones de Clarificación (Ambigüedades resueltas antes de diseñar)

| # | Ambigüedad detectada en el pedido original | Decisión de negocio acordada con Operaciones |
|---|---|---|
| 1 | ¿Qué motivos habilitan pausar el reloj de SLA? | Solo tres causales imputables al cliente (`SlaPauseReason`): `WaitingForCustomerLogs`, `WaitingForCustomerVpnAccess`, `WaitingForCustomerValidation`. |
| 2 | ¿Qué datos obligatorios exige la auditoría bancaria al pausar/reanudar? | Al pausar: `Reason`, `RequestedBy` (no vacío) y `EvidenceNote` (no vacío). Al reanudar: `ResumedBy` (no vacío). Sin estos campos se rechaza con `400 Bad Request`. |
| 3 | ¿Qué ocurre si se envía un `pause` cuando ya está en pausa o ya está `Resolved`? | Se rechaza con `409 Conflict` (`ProblemDetails` RFC 9457). Solo puede existir a lo sumo una ventana activa (`ResumedAtUtc == null`) por incidente. |
| 4 | ¿Qué ocurre si se envía un `resume` cuando el incidente NO está en pausa? | Se rechaza con `409 Conflict` (`ProblemDetails`). |
| 5 | ¿Qué ocurre si las marcas de tiempo enviadas violan la cronología (`PausedAtUtc < OpenedAtUtc` o `ResumedAtUtc < PausedAtUtc`)? | Se rechaza con `422 Unprocessable Entity` (`ProblemDetails`). |
| 6 | ¿Qué pasa si un incidente se resuelve (`POST /resolve`) mientras tenía una pausa activa? | El sistema cierra automáticamente la ventana de pausa activa con `ResumedAtUtc = ResolvedAtUtc` y `ResumedBy = "system:auto-resume-on-resolve"`, y pasa el incidente a `Resolved`. |
| 7 | ¿En qué huso horario se procesan y almacenan las pausas? | Todas las marcas de tiempo se normalizan y calculan en UTC (`.ToUniversalTime()`). |

---

## Especificación Funcional (Notación EARS)

- **REQ-001 (Ubiquitous):** El sistema SHALL almacenar en cada incidente una colección ordenada de ventanas de pausa (`PauseWindows`), registrando `Id`, `Reason`, `RequestedBy`, `EvidenceNote`, `PausedAtUtc`, `ResumedAtUtc` y `ResumedBy`.
- **REQ-002 (Event-Driven):** **WHEN** un operador envía `POST /api/incidents/{id}/sla/pause` con `Reason`, `RequestedBy` y `EvidenceNote` válidos **WHILE** el incidente está en estado `Open` o `InProgress` y sin pausa activa, **THE SYSTEM SHALL** abrir una nueva `SlaPauseWindow` y cambiar el estado del incidente a `WaitingForCustomer`.
- **REQ-003 (Unwanted Behavior):** **IF** un cliente intenta pausar un incidente que ya posee una pausa activa o cuyo estado es `Resolved`, **THEN THE SYSTEM SHALL** rechazar la solicitud con HTTP `409 Conflict` en formato `ProblemDetails`.
- **REQ-004 (Event-Driven):** **WHEN** un operador envía `POST /api/incidents/{id}/sla/resume` con `ResumedBy` válido **WHILE** el incidente posee una ventana de pausa activa, **THE SYSTEM SHALL** registrar `ResumedAtUtc`, cerrar la ventana activa y transicionar el incidente a `InProgress`.
- **REQ-005 (State-Driven):** **WHILE** o después de que un incidente acumule tiempo en ventanas de pausa acreditadas, **THE SYSTEM SHALL** descontar `TotalPausedMinutes` del tiempo activo (`ElapsedActiveMinutes`) y desplazar hacia adelante `EffectiveDeadlineUtc` en esa misma cantidad de minutos.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pausar y reanudar el reloj de SLA por espera del cliente (Priority: P1)

Como ingeniero de guardia 24x7, necesito pausar el reloj de SLA dejando evidencia auditable cuando dependo de insumos del cliente y reanudarlo cuando responde, para que el tiempo de demora del cliente no penalice nuestro SLA ni dispare multas improcedentes.

**Independent Test**: Crear un incidente `HighP2` (objetivo 240 min), avanzar 30 min, pausar por `WaitingForCustomerLogs`, avanzar 90 min en pausa, reanudar, avanzar 20 min activos y verificar en `GET /api/incidents/{id}/sla` que el tiempo activo sea `50` min, el tiempo pausado `90` min y el `EffectiveDeadlineUtc` se haya corrido `+90` min.

**Acceptance Scenarios**:

1. **Given** un incidente `HighP2` abierto a las `12:00 UTC` con 30 minutos activos transcurridos, **When** se invoca `POST /api/incidents/{id}/sla/pause` con `Reason = WaitingForCustomerLogs`, `RequestedBy = "fdeboli@consultora.ar"` y `EvidenceNote` válido, **Then** el sistema responde `200 OK`, cambia `Status` a `WaitingForCustomer` y congela `ElapsedActiveMinutes` en `30`.
2. **Given** un incidente en estado `WaitingForCustomer` durante 90 minutos, **When** se invoca `POST /api/incidents/{id}/sla/resume` con `ResumedBy = "fdeboli@consultora.ar"` y luego transcurren 20 minutos activos adicionales, **Then** `GET /api/incidents/{id}/sla` devuelve `ElapsedActiveMinutes = 50`, `TotalPausedMinutes = 90`, `RemainingMinutes = 190`, `EffectiveDeadlineUtc = OpenedAtUtc + 330 min` y `PauseCount = 1`.

---

### User Story 2 - Protección contra transiciones inválidas y datos sin evidencia (Priority: P1)

Como auditor de cumplimiento SLA, necesito que la API impida dobles pausas, reanudaciones sin pausa activa o pausas sin evidencia/autor, devolviendo errores estructurados RFC 9457.

**Independent Test**: Intentar pausar dos veces seguidas el mismo incidente y verificar HTTP `409 Conflict`; intentar pausar con `EvidenceNote` vacío y verificar HTTP `400 Bad Request`.

**Acceptance Scenarios**:

1. **Given** un incidente que ya tiene una ventana de pausa activa, **When** se envía otro `POST /api/incidents/{id}/sla/pause`, **Then** el sistema responde `409 Conflict` (`application/problem+json`) sin agregar una segunda ventana.
2. **Given** un incidente en estado `Open` sin pausa activa, **When** se envía `POST /api/incidents/{id}/sla/resume`, **Then** el sistema responde `409 Conflict`.
3. **Given** un incidente activo, **When** se envía `POST /api/incidents/{id}/sla/pause` con `RequestedBy` o `EvidenceNote` en blanco, **Then** el sistema responde `400 Bad Request`.
