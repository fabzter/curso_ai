# Guía Paso a Paso del Participante — Workshop M2: SDD sobre .NET con Spec Kit y OpenSpec

> **Objetivo:** Pasar de un pedido de negocio ambiguo a una API `.NET 10` verificada de punta a punta sin escribir código a ciegas ("vibe coding"), gobernando a tu agente mediante **Especificaciones EARS**, **GitHub Spec Kit (`v1.2.5`)** y **OpenSpec (`v1.15.0`)**.

---

## Fase 0 — Preparación y Reconocimiento del Terreno (15 min)

### Paso 0.1: Abrí y verificá el proyecto inicial (`starter/`)
1. En tu terminal, entrá a la carpeta `starter/` del workshop y ejecutá los tests base:
   ```bash
   cd workshops/ws-m2-sdd-dotnet/starter
   dotnet test --nologo
   ```
   Deberías ver **2 tests pasando en menos de 1 segundo** (`CreateIncident_And_QuerySla_ReturnsActiveRemainingMinutes` y `CreateIncident_WithEmptyTenant_ReturnsProblemDetails400`).
2. Leé dos archivos clave antes de tocar el agente:
   - `AGENTS.md`: las 4 invariantes de arquitectura del repositorio (`TimeProvider` inyectado, errores RFC 9457 `ProblemDetails`, fechas en UTC y tests con `WebApplicationFactory<Program>`).
   - `brief-cliente-ambiguo.md`: el mensaje de Slack urgente que mandó Martín (Gerente de Operaciones).

### Paso 0.2: Qué pide Martín (y por qué NO tenés que tirárselo directo al agente)
En `brief-cliente-ambiguo.md`, Martín pide dos cosas mezcladas:
1. **Un feature nuevo:** *"Poder pausar el SLA cuando estamos esperando al cliente (`WaitingForCustomer` o algo así) y volver a prenderlo cuando responde, corriendo hacia adelante el vencimiento y guardando auditoría para el banco."*
2. **Un bug en producción:** *"Ayer cerramos un incidente P1 a los 40 minutos (adentro de los 60 min del SLA), pero hoy a la mañana cuando el dashboard consultó `GET /api/incidents/{id}/sla` aparece como `isBreached: true` con más de 1000 minutos consumidos."*

Si le pegás ese texto crudo al agente y le decís *"implementalo"*, el agente va a inventar códigos de estado HTTP, reglas de transición y campos de auditoría que después no pasan la auditoría bancaria. Vamos a resolverlo con ingeniería.

---

## Fase 1 — Auditoría Adversarial y Especificación EARS (45 min · Unidad 2.1)

### Paso 1.1: Usá a tu agente como Analista Adversarial (sin escribir código)
Abrí tu agente (Claude Code en modo `/plan`, GitHub Copilot o Codex) en la carpeta `starter/` y ejecutá este prompt:

```text
Actuá como un Arquitecto .NET Principal y Analista de Especificaciones Adversarial.
Leé @AGENTS.md, @brief-cliente-ambiguo.md, @src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs y @src/GuardiaCloud.Sla.Api/Program.cs.
NO modifiques ningún archivo todavía.

Tu tarea:
1. Separar el bug reportado del feature nuevo.
2. Identificar al menos 6 ambigüedades, huecos de máquina de estados o casos borde no definidos en el pedido de pausa de SLA que un desarrollador o agente tendría que "adivinar".
3. Formular las preguntas concretas y cerradas para hacerle al Gerente de Operaciones (Product Owner) antes de escribir la especificación.
```

### Paso 1.2: Entrevistá al "Cliente" (el Instructor) y cerrá las 7 definiciones
Hacé tus preguntas al instructor (que actúa como Martín, Gerente de Operaciones). Tomá nota de las **7 definiciones de negocio** que destraban el diseño:
1. **Causales válidas de pausa (`SlaPauseReason`):** Solo tres motivos imputables al cliente: `WaitingForCustomerLogs = 1`, `WaitingForCustomerVpnAccess = 2`, `WaitingForCustomerValidation = 3`.
2. **Campos obligatorios de auditoría bancaria:**
   - Al pausar (`POST /api/incidents/{id}/sla/pause`): `Reason`, `RequestedBy` (string no vacío) y `EvidenceNote` (string no vacío).
   - Al reanudar (`POST /api/incidents/{id}/sla/resume`): `ResumedBy` (string no vacío).
   - Si falta alguno $\rightarrow$ `400 Bad Request` (`ProblemDetails`).
3. **Doble pausa o pausa sobre incidente resuelto:** Solo puede haber una ventana de pausa activa (`ResumedAtUtc == null`) a la vez, y no se puede pausar un incidente `Resolved`. Si se intenta $\rightarrow$ `409 Conflict` (`ProblemDetails`).
4. **Reanudar cuando no está en pausa:** Si se llama a `/resume` sin ventana de pausa activa $\rightarrow$ `409 Conflict`.
5. **Invariantes cronológicas:** `PausedAtUtc` no puede ser menor a `OpenedAtUtc`, y `ResumedAtUtc` no puede ser menor a `PausedAtUtc`. Si ocurre $\rightarrow$ `422 Unprocessable Entity`.
6. **Resolver estando en pausa:** Si un operador llama a `POST /api/incidents/{id}/resolve` mientras había una pausa activa, el sistema **cierra automáticamente** esa ventana de pausa en `ResolvedAtUtc` (con `ResumedBy = "system:auto-resume-on-resolve"`) y marca el incidente como `Resolved`.
7. **Impacto en el cálculo (`GET /api/incidents/{id}/sla`):** El DTO `SlaStatusResponse` debe agregar `TotalPausedMinutes` (`double`) y `PauseCount` (`int`). El tiempo pausado se resta del tiempo activo (`ElapsedActiveMinutes`) y suma minutos hacia adelante en `EffectiveDeadlineUtc`.

---

## Fase 2 — GitHub Spec Kit (`v1.2.5`): Bugfix + Feature de Punta a Punta (75 min · Unidad 2.4 Parte A)

Si tenés el CLI `specify` instalado, podés inicializar la estructura con `specify init . --integration claude` (o `copilot` / `codex`) y `specify extension add bug`. Si trabajás sin conexión al instalador, creá directamente las carpetas `.specify/memory/`, `.specify/bugs/resolved-sla-breach-drift/` y `specs/001-sla-pause-windows/`.

### Paso 2.1: Reparación disciplinada del Bug con el flujo `speckit-bug` (25 min)
1. **Evaluar la causa raíz (`/speckit-bug-assess`):**
   Pedile al agente (o ejecutá `/speckit-bug-assess "Un incidente P1 resuelto a los 40 min aparece como isBreached=true al consultarse horas después" slug=resolved-sla-breach-drift`):
   - Verificá que el agente identifique la línea exacta en `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs`: `SlaCalculator.Evaluate` usa siempre `timeProvider.GetUtcNow()` en vez de congelar el reloj en `incident.ResolvedAtUtc` cuando `incident.Status == IncidentStatus.Resolved`.
2. **Aplicar el fix acotado y su test de regresión (`/speckit-bug-fix` + `/speckit-bug-test`):**
   - Corregí `SlaCalculator.Evaluate` para usar `incident.ResolvedAtUtc.Value` cuando el incidente esté resuelto.
   - Agregá en `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs` el test `ResolvedIncident_FreezesSlaClock_AtResolvedAtUtc_RegressionTest` (creá un P1, avanzá 40 min el `FakeTimeProvider`, resolvelo, avanzá 10 horas más el reloj y comprobá que `ElapsedActiveMinutes == 40` e `IsBreached == false`).
   - Documentá el reporte en `.specify/bugs/resolved-sla-breach-drift/report.md` con veredicto `verified` y corré `dotnet test`. ¡Ya tenés **3 tests en verde**!

### Paso 2.2: Definir la Constitución del Proyecto (`.specify/memory/constitution.md`) (10 min)
Ejecutá `/speckit-constitution` (o pedile al agente que redacte `.specify/memory/constitution.md` alineado con `AGENTS.md`) fijando los **4 principios no negociables**:
1. *Tiempo determinista vía `System.TimeProvider`*.
2. *Contratos de error HTTP con `ProblemDetails` RFC 9457 (`400`, `404`, `409`, `422`)*.
3. *Trazabilidad y auditoría bancaria obligatoria en cada pausa/reanudación*.
4. *Test-First de integración con `WebApplicationFactory<Program>`*.

### Paso 2.3: Especificar, Planificar y Descomponer (`001-sla-pause-windows`) (20 min)
1. **Especificación (`/speckit-specify`):** Generá `specs/001-sla-pause-windows/spec.md` volcando las 7 decisiones de la Fase 1 en requerimientos **EARS** (`REQ-001` a `REQ-005`) y dos historias de usuario independientes (`US1`: Pausar/reanudar y recalcular SLA; `US2`: Rechazo de transiciones inválidas y datos faltantes con `409`/`400`/`422`) con escenarios **Given/When/Then**.
2. **Plan Técnico (`/speckit-plan`):** Generá `specs/001-sla-pause-windows/plan.md` detallando:
   - El `Constitution Check` (los 4 gates verificados).
   - Los cambios exactos en `Domain/IncidentModels.cs` (`IncidentStatus.WaitingForCustomer`, `SlaPauseReason`, `SlaPauseWindow`, `PauseSlaRequest`, `ResumeSlaRequest`, `SlaStatusResponse`).
   - La fórmula de `SlaCalculator.Evaluate`.
   - Los contratos de `POST /api/incidents/{id:guid}/sla/pause` y `POST /api/incidents/{id:guid}/sla/resume`.
3. **Lista de Tareas (`/speckit-tasks`):** Generá `specs/001-sla-pause-windows/tasks.md` con tareas numeradas (`T001`..`T006`), etiquetas `[US1]`/`[US2]`, marca `[P]` en los tests independientes y rutas exactas de archivos `.cs`.

> **Checkpoint Crítico:** ¡Revisá `spec.md`, `plan.md` y `tasks.md` antes de ejecutar `/speckit-implement`! Si un código de estado HTTP o un nombre de propiedad está mal en `plan.md`, corregilo en el Markdown ahora (cuesta 10 segundos) en lugar de pelear con el código C# después.

### Paso 2.4: Implementar y Verificar Convergencia (`/speckit-implement` + `/speckit-converge`) (20 min)
1. Ejecutá `/speckit-implement` para que el agente complete las tareas `T001` a `T006`.
2. Corré `dotnet test --nologo` y verificá que compila con **0 warnings** (`TreatWarningsAsErrors=true`) y pasan todos los tests de integración.
3. Ejecutá `/speckit-converge` (o pedile al agente que audite el código implementado contra cada requerimiento EARS y escenario GWT de `specs/001-sla-pause-windows/spec.md` y actualice el estado en `tasks.md` a `Converged`).

---

## Fase 3 — OpenSpec (`v1.15.0`): Cambio Iterativo *Brownfield* con Especificaciones Delta (60 min · Unidad 2.4 Parte B)

### El Nuevo Escenario (2 semanas después en producción)
Las pausas de SLA ya están en producción, pero llega un nuevo pedido regulatorio del Comité de Auditoría Bancaria:

> *"Detectamos que algunos incidentes `CriticalP1` quedaron pausados más de 2 horas esperando al cliente sin que ningún gerente se enterara. A partir de ahora, los incidentes `CriticalP1` tienen un **tope máximo acumulado de 30 minutos de pausa estándar**. Si una pausa en P1 supera los 30 minutos acumulados, solo se acreditan 30 minutos (el resto vuelve a contar como tiempo activo) y no se permite abrir nuevas pausas en ese P1 (devolver `422 Unprocessable Entity`), **salvo** que la pausa incluya un `SupervisorOverrideCode` no vacío. Además, `GET /api/incidents/{id}/sla` debe devolver `RemainingPauseBudgetMinutes` (`double?`, `null` para P2/P3 o cuando hay override; `0..30` para P1 estándar)."*

En un sistema *brownfield* que ya está andando, no queremos crear un documento aislado que quede obsoleto: queremos ver **exactamente qué requisitos cambian y cuáles se agregan** sobre la especificación viva del sistema (`openspec/specs/sla-tracking/spec.md`). Para eso usamos **OpenSpec**.

### Paso 3.1: Explorar el impacto (`/opsx:explore`) (10 min)
Revisá `openspec/specs/sla-tracking/spec.md` y pedile al agente (con `/opsx:explore` o en modo lectura) que analice cómo impacta el tope de 30 minutos para `CriticalP1` en `SlaPolicyCatalog`, `SlaCalculator` y el endpoint `/pause`.

### Paso 3.2: Proponer el Cambio Delta (`/opsx:propose cap-p1-pause-budget`) (20 min)
Ejecutá `/opsx:propose cap-p1-pause-budget` (o generá la carpeta `openspec/changes/cap-p1-pause-budget/`) con sus 4 artefactos:
1. `proposal.md`: **Why**, **What Changes**, **Capabilities** (`Modified Capabilities: sla-tracking`) e **Impact**.
2. ` specs/sla-tracking/spec.md` (el **Spec Delta**):
   - Un bloque `## MODIFIED Requirements` para `### Requirement: Active SLA Evaluation` (incorporando `RemainingPauseBudgetMinutes` y el tope de 30 min en `CriticalP1`).
   - Un bloque `## ADDED Requirements` para `### Requirement: Critical P1 Pause Budget Enforcement` con dos escenarios (`#### Scenario: Reject second pause on Critical P1 when 30-minute budget is exhausted` y `#### Scenario: Allow pause with SupervisorOverrideCode after budget exhaustion`).
3. `design.md`: las decisiones técnicas en `SlaPolicyCatalog`, `SlaCalculator` y `Program.cs`.
4. `tasks.md`: el checklist numerado (`1.1`, `1.2`, `1.3`, `2.1`).

### Paso 3.3: Aplicar el Cambio y Verificar (`/opsx:apply`) (20 min)
1. Ejecutá `/opsx:apply` para implementar las tareas de `openspec/changes/cap-p1-pause-budget/tasks.md`, incluyendo el test de integración `CriticalP1_PauseBudget_CapsAt30Minutes_UnlessSupervisorOverrideProvided`.
2. Corré `dotnet test --nologo` y comprobá que toda la suite pasa sin regresiones.

### Paso 3.4: Archivar el Cambio y Actualizar la Verdad del Sistema (`/opsx:archive`) (10 min)
Ejecutá `/opsx:archive` (o mové el cambio a `openspec/changes/archive/YYYY-MM-DD-cap-p1-pause-budget/` fusionando los bloques `MODIFIED` y `ADDED` dentro de `openspec/specs/sla-tracking/spec.md`).
- Comprobá cómo `openspec/specs/sla-tracking/spec.md` ahora refleja el comportamiento completo y actual del microservicio, listo para el próximo cambio evolutivo.

---

## Fase 4 — Auditoría Cruzada entre Duplas y Cierre (30 min)

Intercambiá tu repositorio con otra dupla y ejecutá esta lista de chequeo en 15 minutos:
1. `dotnet build GuardiaCloud.Sla.sln --no-restore` $\rightarrow$ ¿Compila con `0 Warning(s)` y `0 Error(s)`?
2. `dotnet test GuardiaCloud.Sla.sln --no-build` $\rightarrow$ ¿Pasan todos los tests de integración (incluyendo el bugfix de `ResolvedAtUtc`, el flujo de pausa/reanudación, el `409 Conflict` en doble pausa y el tope de 30 min en `CriticalP1` con `SupervisorOverrideCode`)?
3. ¿Existe trazabilidad 1 a 1 entre los escenarios **Given/When/Then** de `specs/001-sla-pause-windows/spec.md` + `openspec/specs/sla-tracking/spec.md` y los métodos `[Fact]` en `SlaApiIntegrationTests.cs`?
4. ¿Algún archivo de `src/` usó `DateTime.UtcNow` o `DateTimeOffset.UtcNow` violando el Principio I de la Constitución? (Verificalo con `grep -rn "UtcNow" src/` — solo debe aparecer `timeProvider.GetUtcNow()`).
