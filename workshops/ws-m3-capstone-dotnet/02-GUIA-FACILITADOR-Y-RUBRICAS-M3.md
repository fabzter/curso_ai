# Guía del Facilitador y Rúbricas Oficiales del Módulo 3 (`ws-m3-capstone-dotnet`)

- **Unidades cubiertas:** **Unidades 3.1, 3.2, 3.3 y 3.4** (14 horas totales)
- **Peso en la nota final del curso:** **70% del total del curso**, dividido en:
  - **Entregable #3 (25%):** Constitución (`AGENTS.md`), Especificaciones (`spec.md` + `plan.md`), Prototipo UI y Plan de Tareas (`tasks.md`).
  - **Entregable #4 (35%):** Proyecto .NET funcionando en vivo, suite de pruebas oráculo (`NetArchTest` + `WebApplicationFactory`) y Demo.
  - **Entregable #5 (10%):** Retrospectiva de ingeniería basada en métricas (`retrospectiva-metricas.md`).

---

## 1. Hoja de Respuestas del "Cliente" para la Entrevista de la Unidad 3.1

Durante la Unidad 3.1, actuás como **Director de Operaciones Regionales de GuardiaCloud**. No regales estas 8 definiciones de entrada: esperá a que los equipos te hagan preguntas específicas después de auditar `pliego-licitacion-cliente.md` y el código de `starter/` con sus agentes.

| # | Tema consultado por el equipo | Respuesta oficial del "Cliente" (Instructor) |
|---|---|---|
| **1** | **Criterio de deduplicación en `BUG-301` (`webhooks/incident-event`)** | *"Cada evento tiene un `EventId` único por incidente. Si llega un `EventId` que ya procesamos en `ProcessedWebhookEventIds`, devolvé `200 OK` con `WasDuplicateIgnored = true` y no toques ni `PausedMinutes` ni `AppliedPenaltyEventsCount`."* |
| **2** | **Umbral exacto de alerta temprana en `FEAT-301`** | *"La alerta proactiva se dispara cuando `ConsumedPercentage >= 80.0%` (inclusive). Si está en `79.99%`, todavía no dispara (`ReasonCode = "BELOW_80_PERCENT_THRESHOLD"`)."* |
| **3** | **Ventana de enfriamiento (*cooldown*) e incidentes cerrados en `FEAT-301`** | *"Si el incidente ya tiene `ResolvedAtUtc != null`, devolvé `ShouldDispatchAlert = false` con `ReasonCode = "ALREADY_RESOLVED"`. Si sigue abierto y ya enviamos una alerta hace **menos de 15 minutos** (`< 15.0` min según `TimeProvider`), devolvé `ShouldDispatchAlert = false` con `ReasonCode = "COOLDOWN_ACTIVE_15M"`."* |
| **4** | **Regla de control dual de aprobadores en `FEAT-302`** | *"Los emails `PrimaryApproverEmail` y `SecondaryApproverEmail` deben ser de dos personas distintas comparando **case-insensitive** (`StringComparison.OrdinalIgnoreCase`). Si alguien manda el mismo email en mayúsculas y minúsculas, rechazalo."* |
| **5** | **Formato válido del `DualApprovalToken` en `FEAT-302`** | *"Todo token emitido por nuestro HSM corporativo arranca con el prefijo exacto `'FM-DUAL-'` (case-sensitive). Si no tiene ese prefijo, es inválido."* |
| **6** | **Catálogo de errores RFC 9457 (`ProblemDetails`) para Command Center** | *"Usen el prefijo `CC-`:<br>- Incidente inexistente: `404` (`CC-404-INCIDENT-NOT-FOUND`)<br>- Mismo aprobador primario y secundario: `400` (`CC-400-SAME-APPROVER`)<br>- Token sin prefijo `FM-DUAL-`: `422` (`CC-422-INVALID-DUAL-TOKEN`)<br>- Tier inválido en Dashboard: `400` (`CC-400-INVALID-CLIENT-TIER`)."* |
| **7** | **Impacto financiero de la exención en el Dashboard (`FEAT-303`)** | *"Un incidente vencido (`ConsumedPercentage > 100.0%`) sigue contando en `BreachedIncidents`, pero si tiene `Exemption != null`, **no suma su `PenaltyPerBreachUsd` en `TotalFinancialExposureUsd`** y además incrementa `ExemptedIncidents`."* |
| **8** | **Definición de `AtRiskIncidents` vs. `BreachedIncidents` en `FEAT-303`** | *"`BreachedIncidents` son los que tienen `ConsumedPercentage > 100.0%`. `AtRiskIncidents` son los que están entre `80.0%` y `100.0%` inclusive (`80.0 <= ConsumedPercentage <= 100.0`)."* |

---

## 2. Intervenciones Clave del Facilitador en las Unidades 3.2, 3.3 y 3.4

1. **En la Unidad 3.2 (Revisión Cruzada de Specs):** Asegurate de que ningún equipo pase a la Unidad 3.3 con frases ambiguas como *"cuando consuma casi todo el SLA"* o *"validar token"*. En `specs/command-center-v2/spec.md` deben figurar literalmente `>= 80.0%`, `15 minutos`, `FM-DUAL-` y los códigos `CC-4xx`.
2. **En la Unidad 3.3 (`tasks.md` y prevención de conflictos de merge):** Verificá que el equipo haya asignado `FEAT-302` a modo **Human-in-the-Loop (HITL)** (por tratarse de control regulatorio dual y exención financiera) y que el *QA & Oracle Lead* escriba primero los tests en `CommandCenterTests.cs` al iniciar el Sprint 1.
3. **En el Checkpoint de la Unidad 3.4 (Minuto 120 de implementación):** Hacé que todos los equipos integren sus ramas del Sprint 1 (`BUG-301` y `FEAT-301`) a `main` y corran `dotnet test`. Esto evita que acumulen ramas divergentes durante 4 horas.

---

## 3. Las 3 Rúbricas Oficiales de Calificación del Módulo 3 (70% de la Nota del Curso)

### Rúbrica A — Entregable #3: Constitución, Specs y Plan del Proyecto Integrador (25% Nota Final)

| Criterio | Peso | Excelente (100%) | Aceptable (70%) | Insuficiente (0–40%) |
|---|---:|---|---|---|
| **1. Constitución del Repo (`AGENTS.md` + `CLAUDE.md` + Skill)** | **25 pts** | `AGENTS.md` conciso (<80 líneas) con invariantes de `NetArchTest`, comandos exactos y puente `@AGENTS.md`. | `AGENTS.md` presente pero omite comandos de filtro o puente `CLAUDE.md`. | Sin `AGENTS.md` curado. |
| **2. Spec Funcional EARS + Escenarios GWT (`spec.md`)** | **30 pts** | Cubre `BUG-301` y `FEAT-301..303` en sintaxis EARS con las 8 reglas destrabadas en la entrevista y escenarios GWT verificables. | Cubre las 4 entregas pero deja alguna regla de borde sin cuantificar. | Spec ambigua o incompleta. |
| **3. Spec Técnica .NET + Prototipo UI (`plan.md`)** | **25 pts** | Contratos HTTP, tabla RFC 9457 (`CC-4xx`), ADRs y prototipo UI del Dashboard alineado a `TierExecutiveDashboardDto`. | Contratos correctos pero falta algún código RFC 9457 o detalle del prototipo. | Sin especificación de errores RFC 9457. |
| **4. Grafo de Tareas Paralelizable (`tasks.md`)** | **20 pts** | Tareas asignadas por rol y `git worktree`, con modo `HITL`/`Full AI` justificado, tiempos estimados y comando `dotnet test --filter` por tarea. | Plan de tareas completo pero sin aislamiento claro de archivos/worktrees. | Lista plana de tareas sin criterios de verificación. |

---

### Rúbrica B — Entregable #4: Proyecto .NET Funcionando, Oráculo de Pruebas y Demo (35% Nota Final)

| Criterio | Peso | Excelente (100%) | Aceptable (70%) | Insuficiente (0–40%) |
|---|---:|---|---|---|
| **1. Reparación de `BUG-301` (Idempotencia de Webhooks)** | **20 pts** | Deduplicación exacta por `EventId` en `ProcessedWebhookEventIds`; reintentos devuelven `WasDuplicateIgnored = true` sin duplicar penalidades. | Resuelve la duplicación pero no informa `WasDuplicateIgnored = true`. | El bug persiste ante reintentos. |
| **2. Implementación de `FEAT-301` y `FEAT-302` (Negocio + RFC 9457)** | **35 pts** | Escalamiento al `>= 80%` con cooldown de 15m vía `TimeProvider`, y exención dual validando emails distintos (case-insensitive, `400 CC-400-SAME-APPROVER`) y prefijo `FM-DUAL-` (`422 CC-422-INVALID-DUAL-TOKEN`). | Lógica principal funciona pero falla alguna validación de borde RFC 9457. | Endpoints incompletos o uso de `DateTimeOffset.UtcNow`. |
| **3. Implementación de `FEAT-303` (Dashboard Ejecutivo)** | **20 pts** | Calcula `BreachedIncidents`, `AtRiskIncidents`, `ExemptedIncidents` y descuenta incidentes exentos de `TotalFinancialExposureUsd`. | Calcula conteos pero olvida descontar exenciones de la exposición en USD. | Endpoint no funciona o devuelve datos estáticos. |
| **4. Oráculo `NetArchTest` + Integración y Demo en Vivo** | **25 pts** | Compila con `0 warnings` (`TreatWarningsAsErrors=true`), pasan las **8 suites xUnit** (`NetArchTest` + `WebApplicationFactory`) y la demo en vivo es fluida. | Pasan los tests funcionales pero falta algún test de borde o de arquitectura. | El proyecto no compila o fallan tests en la demo. |

---

### Rúbrica C — Entregable #5: Retrospectiva de Ingeniería Basada en Métricas (10% Nota Final)

| Criterio | Peso | Excelente (100%) | Aceptable (70%) | Insuficiente (0–40%) |
|---|---:|---|---|---|
| **1. Registro Cuantitativo Estimado vs. Real (`retrospectiva-metricas.md`)** | **50 pts** | Tabla completa para las 4 entregas con tiempo estimado, tiempo de generación, tiempo de revisión/QA, iteraciones y defectos contenidos por el oráculo. | Tabla completa pero sin separar tiempo de generación vs. tiempo de revisión. | Datos incompletos o sin mediciones reales. |
| **2. Plan de Transferencia a la Consultora** | **50 pts** | Define 3 decisiones accionables y específicas (qué adoptar en repos `.NET`, qué prohibir y cómo ajustar estimaciones el lunes siguiente). | Conclusiones genéricas sin aterrizar al flujo `.NET` de la consultora. | No presenta plan de transferencia. |

### Comando de Corrección Rápida para el Docente
```bash
dotnet test GuardiaCloud.CommandCenter.sln --nologo
```
