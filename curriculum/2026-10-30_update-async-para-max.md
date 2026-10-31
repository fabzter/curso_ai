# Update Async para Max: Evolución a Temario v2 (.NET + Azure) y 4 Workshops Prácticos Construidos

- **Fecha:** 30 de octubre de 2026
- **De:** Fab
- **Para:** Max Déboli
- **Archivos principales de referencia en el repo:**
  - Temario v2 completo (listo para cliente/alumnos, en español rioplatense): [`curriculum/2026-10-30_temario-v2-propuesta.md`](2026-10-30_temario-v2-propuesta.md)
  - Auditoría detallada unidad por unidad (v1 $\rightarrow$ v2): [`curriculum/2026-10-30_syllabus-review-v1.md`](2026-10-30_syllabus-review-v1.md)
  - Verificación de versiones y SDKs (.NET/Azure + SDD, oct. 2026): [`research/2026-10-30_tooling-and-dotnet-azure-verification.md`](../research/2026-10-30_tooling-and-dotnet-azure-verification.md)
  - 4 Paquetes de Workshops / Capstone (`.NET 10`, compilando y con suites xUnit en verde): [`workshops/`](../workshops/)

---

## 1. Resumen Ejecutivo (TL;DR en 2 minutos)

Tomé tu borrador de temario (**52 hs, 3 módulos, 13 unidades**) como estructura maestra —la secuencia pedagógica de **Herramientas (20 hs) $\rightarrow$ Metodología SDD (18 hs) $\rightarrow$ Proyecto Integrador (14 hs)** y los pesos de evaluación (**15% + 15% + 25% + 35% + 10% = 100%**) están impecables y se mantienen intactos— y avancé en **cuatro frentes** para dejar tanto el programa como los talleres listos para revisión asíncrona este fin de semana:

1. **Rebalanceo real al ~65–70% de práctica guiada:**
   - En el draft inicial se declaraba "60–70% práctico", pero al sumar los bloques explícitamente prácticos de los Módulos 1 y 2 daban **13.75 hs de 38 hs (~36%)**.
   - Reestructuré la distribución interna de las unidades (compactando bloques expositivos sin quitar ningún tema) para que cada unidad tenga un taller práctico de **1h 15m a 3h 45m**, llevando la práctica real a **62.5% en Módulos 1–2 (23.75 hs)** y **69.7% en el curso completo (36.25 hs de 52 hs)**.
2. **Aterrizaje nativo en el ecosistema .NET y Azure (verificado a octubre 2026):**
   - En la Unidad 1.2 sumé **Visual Studio 2022/2026 (Copilot Agent Mode)** y **JetBrains Rider (AI + Junie)** junto a VS Code/Cursor/Windsurf, abordando las particularidades reales de Roslyn, MSBuild y licenciamiento de C# Dev Kit.
   - En la Unidad 1.3 reemplacé el cierre exclusivo en Python/TS por el stack oficial de agentes en .NET: **`Microsoft.Extensions.AI` (`v10.11.0`, `IChatClient`)** y **Microsoft Agent Framework (`Microsoft.Agents.AI` `v1.27.0` / Semantic Kernel sobre Azure AI Foundry)**.
   - En la Unidad 1.5 cambié la práctica del servidor MCP de TypeScript/Python al **SDK oficial de C# en NuGet (`ModelContextProtocol` `v2.3.0` y `ModelContextProtocol.AspNetCore`)**, sumando además el **Azure MCP Server (`microsoft/mcp`)**.
   - En la Unidad 2.3 aterricé el "oráculo de verificación" al stack .NET real: **`NetArchTest.Rules` (`v1.3.2`)** para reglas de arquitectura verificables por máquina + **`WebApplicationFactory<Program>`** + `System.TimeProvider`.
3. **Enfoque *Brownfield* y Repositorio Semilla Único (`GuardiaCloud.Sla`):**
   - Como en una consultora el 80%+ del trabajo ocurre sobre sistemas existentes (*brownfield*) y no en proyectos vacíos, diseñé un dominio transversal (**`GuardiaCloud.Sla`**: plataforma de auditoría y liquidación de SLAs críticos para banca y seguros) que sirve de hilo conductor en los Módulos 1, 2 y 3.
   - Esto resuelve además el mayor riesgo del **Módulo 3 (14 hs)**: en vez de arrancar desde `dotnet new` vacío y perder 3 horas en configuración, los equipos reciben una solución base `.NET 10` andando, con arquitectura limpia, un bug productivo sembrado y 3 *Vertical Slices* listas para especificar, planificar y desarrollar en paralelo.
4. **Desarrollo completo de los 4 Workshops troncales (con código `.NET 10` compilando y tests en verde):**
   - Construí los 4 paquetes completos en [`workshops/`](../workshops/) (especificación, guía paso a paso para los participantes en español rioplatense, guía del facilitador con hojas de respuestas para los *role-plays*, rúbricas sobre 100 puntos, proyecto `starter/` y proyecto `solution/`).

---

## 2. Mapa de Mejoras Unidad por Unidad (Temario v1 $\rightarrow$ Temario v2)

| Unidad | Horas | Qué tenía el Draft v1 | Qué sumamos / mejoramos en el Temario v2 | Práctica v2 |
|---|---:|---|---|---:|
| **1.1 Diseño** | 4 hs | Figma Make, v0, Lovable, Stitch, Artifacts (2h15m teoría / 1h45m práctica). | Agregamos el bloque crítico para .NET: **cómo conectar prototipos React/Tailwind generados por IA con backends ASP.NET Core (vía OpenAPI) o convertirlos a componentes Blazor (`.razor`)**. | **2h 30m** (62.5%) |
| **1.2 Herramientas de Desarrollo** | 4 hs | Cursor, Windsurf, Copilot, JetBrains AI, Claude Code, Codex (2h30m teoría / 1h30m práctica). | Sumamos **Visual Studio + Rider (Junie)**, riesgos reales en C# (`N+1` en EF Core, falta de `CancellationToken`, paquetes NuGet alucinados) y un taller de **5 flujos diarios sobre código .NET legado**. | **2h 30m** (62.5%) |
| **1.3 Agentes y Skills** | 4 hs | Bucle agéntico, patrones, `SKILL.md` y cierre con Claude/OpenAI SDKs (2h45m teoría / 1h15m práctica). | Estándar abierto `agentskills.io` (*progressive disclosure* en 3 niveles + script validador) y desarrollo de agentes en C# con **`Microsoft.Extensions.AI` (`v10.11.0`) + `Microsoft.Agents.AI` (`v1.27.0`)**. | **2h 30m** (62.5%) |
| **1.4 Harness Engineering** | 6 hs | Claude Code, Devin y Codex (4h00m teoría / 2h00m práctica). | Interoperabilidad real **`AGENTS.md` + puente `@AGENTS.md` en `CLAUDE.md`**, evidencia sobre por qué los archivos autogenerados degradan al agente, hooks `PostToolUse` atados a `dotnet build`/`dotnet test` y laboratorio comparado **Claude Code vs. Codex CLI**. | **3h 45m** (62.5%) |
| **1.5 MCP en .NET y Azure** | 2 hs | Qué es MCP, configuración y "crear un servidor MCP en TS o Python" (1h15m teoría / 0h45m práctica). | **Servidor MCP 100% en C# con el paquete oficial `ModelContextProtocol` (`v2.3.0`)**, anotaciones de seguridad (`ReadOnlyHint`), defensa contra *Prompt Injection Indirecto* y conexión con la Skill de la Unidad 1.3. | **1h 15m** (62.5%) |
| **2.1 Especificaciones (Spec)** | 4 hs | Spec funcional/técnica, GWT y contratos (2h30m teoría / 1h30m práctica). | Notación **EARS (`WHEN / WHILE / IF…THEN / THE SYSTEM SHALL`)** combinada con **Given/When/Then**, contratos `ProblemDetails` RFC 9457 y taller de **Auditoría Adversarial de un brief ambiguo**. | **2h 30m** (62.5%) |
| **2.2 Estimación, Impacto y Planning** | 4 hs | Impacto, descomposición, estimación y métricas (2h45m teoría / 1h15m práctica). | Descomposición en **DAG de tareas con fronteras de archivos** para evitar el 27.7% de conflictos de merge entre agentes paralelos, y separación explícita entre tiempo de codificación (se comprime) vs. tiempo de especificación y revisión (nuevo cuello de botella). | **2h 30m** (62.5%) |
| **2.3 Full AI vs. HITL** | 4 hs | Espectro de autonomía, tests como oráculo y revisión de código (2h30m teoría / 1h30m práctica). | **Oráculo determinista en .NET (`NetArchTest.Rules` + `WebApplicationFactory` + `TimeProvider`)** y laboratorio práctico en dos **`git worktrees`** ejecutando una tarea financiera en HITL y una tarea operativa en Full AI. | **2h 30m** (62.5%) |
| **2.4 Herramientas SDD** | 6 hs | Spec Kit, Kiro, BMAD, OpenSpec, Tessl (4h00m teoría / 2h00m práctica). | Taxonomía SDD (*Spec-first*, *Spec-anchored*, *Spec-as-source*), comandos actualizados de **GitHub Spec Kit `v1.2.5`** (incluyendo `/speckit-converge` y la extensión `bug`) y flujo **OpenSpec `v1.15.0`** para cambios *brownfield* mediante deltas (`ADDED/MODIFIED Requirements`). | **3h 45m** (62.5%) |
| **3.1 a 3.4 Proyecto Integrador** | 14 hs | Caso práctico en equipos de 3–5 personas en 4 etapas (1.5h teoría / 12.5h práctica). | **Repositorio Semilla Empresarial `.NET 10` (`GuardiaCloud.CommandCenter.sln`)** pre-configurado, topología de 4 roles por equipo, pliego con 8 ambigüedades para el *role-play* de la U3.1, 1 bug + 3 *Vertical Slices* para trabajar en `git worktrees` sin pisarse, y las 3 rúbricas oficiales (70% de la nota). | **12h 30m** (89.3%) |

---

## 3. Detalle de los 4 Paquetes de Workshops Construidos (`.NET 10`)

Cada paquete dentro de [`workshops/`](../workshops/) incluye:
- `00-WORKSHOP-SPEC.md` (objetivos medibles, cronograma minuto a minuto, prerrequisitos y estructura)
- `01-GUIA-PASO-A-PASO.md` (guía práctica para el alumno redactada en voseo rioplatense)
- `02-GUIA-FACILITADOR-Y-RUBRICA.md` (guía docente, respuestas de *role-play*, *troubleshooting* y rúbrica sobre 100 puntos)
- `starter/` (solución `.NET 10` inicial que compila con `TreatWarningsAsErrors=true` y pasa sus tests base)
- `solution/` (solución `.NET 10` de referencia con todos los artefactos y tests de aceptación pasando en verde)

### Workshop 1 — `workshops/ws-m1-skills-mcp-dotnet/` (Unidades 1.3 + 1.5 · Entregable #1 = 15% de la nota)
- **Qué construye el participante:**
  1. Una **Skill de equipo (`.agents/skills/dotnet-minimal-api-guardian/SKILL.md`)** con carga progresiva hacia `references/rfc9457-catalogo-errores.md` y un script verificador determinista (`scripts/verify-minimal-api.sh`).
  2. Un **Servidor MCP oficial en C# (`GuardiaCloud.Sla.McpServer`)** con `ModelContextProtocol` (`v2.3.0`), exponiendo 3 herramientas (`get_client_sla_policy`, `inspect_incident_sla_status`, `validate_rfc9457_contract`) con anotaciones `ReadOnlyHint = true` y sanitización contra un ataque de **Prompt Injection Indirecto** sembrado en el incidente `INC-2026-1002`.
  3. Un **Agente de Triage en C# (`SlaTriageAgent`)** con `Microsoft.Extensions.AI` (`v10.11.0`, `IChatClient` + `FunctionInvokingChatClient` + `AIFunctionFactory.Create`) y condiciones de parada (`MaximumIterationsPerRequest = 4`), testeable 100% *offline* en el aula en 175 ms.

### Workshop 2 — `workshops/ws-m2-sdd-dotnet/` (Unidades 2.1 + 2.4 · Entregable #2 = 15% de la nota)
- **Qué construye el participante:**
  1. Audita un pedido ambiguo del Gerente de Operaciones (`brief-cliente-ambiguo.md`), destraba **7 ambigüedades ocultas** en un *role-play* en vivo con el instructor y redacta requerimientos en notación **EARS + Given/When/Then**.
  2. Diagnostica y repara un bug productivo en `SlaCalculator.cs` (que ignoraba `ResolvedAtUtc`) usando la extensión de bugs de **GitHub Spec Kit (`v1.2.5`)** (`/speckit-bug-assess` $\rightarrow$ `/speckit-bug-fix` $\rightarrow$ `/speckit-bug-test`).
  3. Implementa las **Ventanas de Pausa Auditable de SLA** (`POST /pause` y `POST /resume`) con el ciclo completo de Spec Kit (`/speckit-constitution` $\rightarrow$ `/speckit-specify` $\rightarrow$ `/speckit-plan` $\rightarrow$ `/speckit-tasks` $\rightarrow$ `/speckit-implement` $\rightarrow$ **`/speckit-converge`**).
  4. Aplica un cambio regulatorio *brownfield* (tope de 30 min de pausa en incidentes P1 salvo `SupervisorOverrideCode`) usando deltas en **OpenSpec (`v1.15.0`)** (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`).

### Workshop 3 — `workshops/ws-m2-harness-oracle-dotnet/` (Unidades 1.4 + 2.3 · Práctica Troncal de Harness y Oráculos)
- **Qué construye el participante:**
  1. Reemplaza un `AGENTS.md` inflado/autogenerado por uno curado (<60 líneas), crea el puente `@AGENTS.md` en `CLAUDE.md`, activa el hook `PostToolUse` (`scripts/post-edit-dotnet-hook.sh`) y configura el subagente revisor `.claude/agents/dotnet-arch-reviewer.md`.
  2. Programa dos reglas de arquitectura limpia con **`NetArchTest.Rules` (`v1.3.2`)** en `ArchitectureOracleTests.cs`, detecta automáticamente una clase intrusa (`LegacyVibeCodedHelper.cs`) que acoplaba `Domain` con `Infrastructure` y la elimina.
  3. Ejecuta el laboratorio comparado en dos **`git worktrees`**: implementa la **Tarea A** (motor financiero de créditos SLA con redondeo bancario y topes por tier) en modo **Human-in-the-Loop** y la **Tarea B** (exportador de resumen de guardia) en modo **Full AI autónomo**, midiendo tiempos e iteraciones en `comparativa-hitl-vs-full-ai.md`.

### Workshop 4 / Capstone — `workshops/ws-m3-capstone-dotnet/` (Unidades 3.1 a 3.4 · 14 hs · Entregables #3 [25%], #4 [35%] y #5 [10%] = 70% de la nota)
- **Qué construye cada equipo de 3–5 personas:**
  - Sobre la solución semilla `GuardiaCloud.CommandCenter.sln`, los 4 roles del equipo entrevistan al cliente (U3.1, 8 reglas ocultas), redactan las Specs EARS/GWT y el prototipo UI con revisión adversarial cruzada (U3.2), arman el grafo de tareas paralelizable `tasks.md` (U3.3) y ejecutan 2 sprints en `git worktrees` (U3.4) para entregar:
    - `BUG-301`: Idempotencia de webhooks mediante `ProcessedWebhookEventIds`.
    - `FEAT-301`: Escalamiento proactivo al $\ge 80\%$ del SLA con *cooldown* de 15 minutos.
    - `FEAT-302`: Exenciones por fuerza mayor con validación de doble aprobador (*case-insensitive*, `CC-400-SAME-APPROVER`) y token `FM-DUAL-*` (`CC-422-INVALID-DUAL-TOKEN`).
    - `FEAT-303`: Tablero ejecutivo consolidado por tier descontando exenciones de la exposición financiera en USD.

---

## 4. Tres Puntos para Definir Juntos (Cuando lo revises el finde)

1. **Confirmación de Stack Principal de la Consultora:** Armé todos los ejemplos y talleres sobre **.NET 10 (compatible con .NET 8/9) + Azure**, que encaja perfecto con perfil enterprise. ¿Confirmamos que la mayoría de los participantes de la consultora trabajan en .NET/Azure, o hay algún grupo fuerte en otro stack (ej. Node/TS, Java o Python) para agregarles notas de adaptación?
2. **Herramientas del Día a Día en la Consultora (IDE y ALM):** ¿Sabes si usan principalmente **GitHub Enterprise** o **Azure DevOps** (Repos/Boards/Pipelines), y si en C# predomina **Visual Studio**, **Rider** o **VS Code**?
3. **Licencias de Harnesses en el Aula:** Mantuvimos tu criterio del draft v1 (al menos 1 *harness* activo por participante entre **Claude Code / Copilot / Codex**, y **Devin + Kiro** por demo guiada si no tienen licencias para todos). Además, diseñé los suites de pruebas de los workshops para que compilen y pasen 100% local/offline sin bloquearse por llaves de API externas.
