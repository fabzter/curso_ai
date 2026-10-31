# Guía de Ejecución por Equipos (Módulo 3 — 14 hs): GuardiaCloud Command Center v2.0

> **Modalidad:** Equipos de 3 a 5 personas · **Duración:** 14 hs (Unidades 3.1 a 3.4) · **Peso:** **70% de la nota final del curso** (Entregables #3 [25%], #4 [35%] y #5 [10%])

En el Módulo 3 vas a trabajar como una célula de ingeniería `.NET` de la consultora para entregar en producción **`GuardiaCloud Command Center v2.0`**, combinando todo lo que construiste en los Módulos 1 y 2:
- **Del Módulo 1:** Prototipado UI (U1.1), flujos de IDE (U1.2), la **Skill de equipo RFC 9457 (`SKILL.md`)** (U1.3), el **Harness (`AGENTS.md` + `CLAUDE.md` + hooks + subagentes)** (U1.4) y el **Servidor MCP en C# (`ModelContextProtocol` v2.3.0)** (U1.5).
- **Del Módulo 2:** Especificaciones ejecutables **EARS + Given/When/Then** (U2.1), análisis de impacto y descomposición en un **DAG de tareas paralelizables (`tasks.md`)** (U2.2), **Oráculo determinista (`NetArchTest.Rules` + `WebApplicationFactory`) y ejecución en `git worktrees` (HITL vs. Full AI)** (U2.3), y flujo **GitHub Spec Kit / OpenSpec** (U2.4).

---

## Unidad 3.1 — Presentación del Caso y Entendimiento Funcional (2 hs)

### Paso 3.1.1: Armado del equipo y verificación del repositorio semilla (20 min)
1. Definí los 4 roles dentro de tu equipo:
   - **Product & Spec Lead**
   - **Architect & Harness Lead**
   - **Backend & MCP Lead**
   - **QA, Oracle & Integration Lead**
2. Cloná/abrí `starter/` y verificá que los 3 tests base pasen en menos de 1 segundo:
   ```bash
   cd workshops/ws-m3-capstone-dotnet/starter
   dotnet test GuardiaCloud.CommandCenter.sln --nologo
   ```

### Paso 3.1.2: Arqueología asistida por IA y detección de las 8 ambigüedades (40 min)
Leé [`starter/pliego-licitacion-cliente.md`](starter/pliego-licitacion-cliente.md) e inspeccioná [`src/GuardiaCloud.CommandCenter.Api/Domain/CommandCenterEvaluator.cs`](starter/src/GuardiaCloud.CommandCenter.Api/Domain/CommandCenterEvaluator.cs).
Usá tu agente en modo lectura con rol de **Analista Adversarial** para cruzar el pliego contra el código C# actual y descubrir las **8 definiciones faltantes** sobre:
1. Cómo identificar un webhook duplicado en `BUG-301` y qué código HTTP devolver cuando se ignora un reintento.
2. Cuál es el porcentaje exacto de consumo de SLA que dispara la alerta proactiva en `FEAT-301` (`>= 80.0%`).
3. Cuántos minutos dura la ventana de enfriamiento (*cooldown*) entre alertas de un mismo incidente (`15 minutos`) y qué pasa si el incidente ya está cerrado (`ResolvedAtUtc != null`).
4. Cómo se valida el control dual de aprobadores en `FEAT-302` (comparación *case-insensitive* de emails).
5. Qué formato obligatorio debe tener el `DualApprovalToken` (`prefijo "FM-DUAL-"`).
6. Qué códigos HTTP y `extensions["errorCode"]` RFC 9457 corresponden a cada rechazo (`CC-404-INCIDENT-NOT-FOUND`, `CC-400-SAME-APPROVER`, `CC-422-INVALID-DUAL-TOKEN`, `CC-400-INVALID-CLIENT-TIER`).
7. Cómo impacta una exención de fuerza mayor en el cálculo de `TotalFinancialExposureUsd` del Dashboard (`FEAT-303`).
8. Qué rango define a `AtRiskIncidents` (`80.0% <= consumo <= 100.0%`) frente a `BreachedIncidents` (`> 100.0%`).

### Paso 3.1.3: Dos rondas de entrevista al "Cliente" (Instructor) (60 min)
Formulá tus preguntas de negocio al instructor (quien actúa como Director de Operaciones Regionales) y registrá las respuestas oficiales como base para la Unidad 3.2.

---

## Unidad 3.2 — Especificaciones, Prototipo UI y Revisión Cruzada (4 hs)

### Paso 3.2.1: Configuración del Harness del Equipo (45 min)
El *Architect & Harness Lead* y el *Backend & MCP Lead* configuran en el repositorio:
- `AGENTS.md` (<80 líneas) y `CLAUDE.md` (`@AGENTS.md`).
- La Skill `.agents/skills/dotnet-minimal-api-guardian/` adaptada al catálogo `CC-4xx`.
- El hook de compilación/pruebas para que ningún agente deje el build roto.

### Paso 3.2.2: Redacción de la Spec Funcional (`spec.md`), Spec Técnica (`plan.md`) y Prototipo UI (120 min)
1. Creá `specs/command-center-v2/spec.md` redactando los requerimientos **R1 (`BUG-301`)**, **R2 (`FEAT-301`)**, **R3 (`FEAT-302`)** y **R4 (`FEAT-303`)** en notación **EARS** (`WHEN / WHILE / IF…THEN / THE SYSTEM SHALL`) y los escenarios **Given/When/Then**.
2. Creá `specs/command-center-v2/plan.md` definiendo la tabla exacta de endpoints HTTP, DTOs inmutables, catálogo de errores RFC 9457 y decisiones de arquitectura (ADRs).
3. Generá el prototipo interactivo del **Tablero Ejecutivo de Guardia (`FEAT-303`)** con las herramientas de la Unidad 1.1 (v0, Stitch, Lovable o Claude Artifacts) respetando exactamente las propiedades de `TierExecutiveDashboardDto`.

### Paso 3.2.3: Revisión Adversarial Cruzada entre Equipos (45 min)
Intercambiá tu carpeta `specs/command-center-v2/` con otro equipo. Usá tu agente para buscar ambigüedades, casos borde no cubiertos o contradicciones entre `spec.md` y `plan.md`. Aplicá las correcciones y obtené el *sign-off* del instructor (**Parte A del Entregable #3**).

---

## Unidad 3.3 — Planificación, Análisis de Impacto y Grafo de Tareas (`tasks.md`) (2 hs)

### Paso 3.3.1: Análisis de Impacto y Descomposición en `tasks.md` (75 min)
Generá `specs/command-center-v2/tasks.md` dividiendo el trabajo en tareas atómicas e independientes para las 6 horas de la Unidad 3.4:
- **Regla de oro anti-colisiones:** Asigná cada slice (`BUG-301`, `FEAT-301`, `FEAT-302`, `FEAT-303`) a un integrante y un `git worktree` distinto, especificando para cada tarea:
  1. Archivos exactos que puede modificar.
  2. Modo de ejecución elegido (**`Full AI`** vs. **`Human-in-the-Loop`**) y por qué.
  3. Tiempo estimado (en minutos).
  4. Comando exacto de `dotnet test --filter FullyQualifiedName~...` que actúa como condición de parada (*Definition of Done*).

### Paso 3.3.2: Defensa del Plan ante el Instructor (30 min)
Presentá `tasks.md` y la estrategia de paralelización para completar el **Entregable #3 (25% de la nota final)**.

---

## Unidad 3.4 — Implementación Agéntica, QA Cruzado y Demo Final (6 hs)

### Bloque 1 — Sprint 1: Oráculo de Pruebas y Primeras Slices (2 hs)
1. **Primeros 30 min (TDD Agéntico en `main`):** El *QA, Oracle & Integration Lead* agrega en `tests/GuardiaCloud.CommandCenter.Tests/CommandCenterTests.cs` los tests de integración con `WebApplicationFactory<Program>` y `FixedTimeProvider(2026-10-30T14:00:00Z)` para `BUG-301`, `FEAT-301`, `FEAT-302` y `FEAT-303`.
2. **Siguientes 90 min (Ejecución en paralelo):**
   - En `wt-bug301`: reparación de `CommandCenterEvaluator.ApplyWebhookEvent` usando `ProcessedWebhookEventIds`.
   - En `wt-feat301`: implementación de `EvaluateProactiveEscalation` y `POST /api/command-center/escalations/evaluate/{incidentId}`.

### Bloque 2 — Checkpoint de Convergencia (`/speckit-converge`) (30 min)
Integrá las ramas del Sprint 1 a `main` y ejecutá la auditoría de convergencia contra `specs/command-center-v2/spec.md` verificando que no haya desvíos de contrato ni violaciones en `ArchitectureOracle`.

### Bloque 3 — Sprint 2: Cierre de Slices Regulatorias y Dashboard (2 hs)
1. En `wt-feat302` (**Modo HITL**): implementación de `ApplyForceMajeureExemption` y `POST /api/command-center/exemptions` validando aprobadores distintos (*case-insensitive*, `CC-400-SAME-APPROVER`) y prefijo `"FM-DUAL-"` (`CC-422-INVALID-DUAL-TOKEN`).
2. En `wt-feat303` (**Modo Full AI**): implementación de `BuildTierDashboard` y `GET /api/command-center/dashboard/{clientTier}` descontando incidentes con exención activa de `TotalFinancialExposureUsd`.
3. Integración final y corrida de los **8 tests del proyecto en verde** con `0 warnings`.

### Bloque 4 — QA de Aceptación Cruzado (45 min)
Cada equipo clona/ejecuta la solución de otro equipo, corre `dotnet test GuardiaCloud.CommandCenter.sln` y prueba manualmente los escenarios Given/When/Then de su `spec.md`.

### Bloque 5 — Demo en Vivo y Retrospectiva Basada en Métricas (45 min)
1. Completá [`plantilla-retrospectiva-metricas.md`](starter/plantilla-retrospectiva-metricas.md) con los tiempos reales medidos en ambos sprints.
2. En 10 minutos por equipo, mostrá:
   - La suite de 8 tests (`NetArchTest` + `WebApplicationFactory`) y los endpoints andando en vivo (**Entregable #4 — 35%**).
   - Los hallazgos de tu tabla de métricas y las 3 decisiones concretas que el equipo llevará a sus proyectos de consultoría el lunes siguiente (**Entregable #5 — 10%**).
