# Guía del Presentador y Facilitador Paso a Paso — Curso Completo (52 Horas)
## Desarrollo de Software con IA en Ecosistemas .NET 10 y Azure

- **Autores:** Max Déboli & Fabrizio Hernández
- **Audiencia:** Ingenieros de software, Tech Leads y Arquitectos de consultora de software (Buenos Aires)
- **Duración total:** 52 horas presenciales (30% encuadre conceptual y demos en vivo = 15.75 hs · 70% práctica guiada y workshops = 36.25 hs)
- **Stack técnico primario (`D-014`):** `.NET 10` (C# 13, ASP.NET Core Minimal APIs, EF Core, `ProblemDetails` RFC 9457, `TimeProvider`, xUnit, `WebApplicationFactory`, `Testcontainers`, `NetArchTest.Rules` v1.3.2, `ModelContextProtocol` C# SDK v2.3.0, `Microsoft.Extensions.AI` v10.11.0, `Microsoft.Agents.AI` v1.27.0) + **Azure**
- **IDEs estándar del curso (`D-024`):** **VS Code (con GitHub Copilot), Cursor y Windsurf** *(cada desarrollador puede usar su IDE habitual por su cuenta si lo prefiere)* + Harnesses de terminal/cloud (**Claude Code**, **OpenAI Codex** y **Devin**)
- **Repositorios de trabajo:**
  - Módulos 1 y 2: `GuardiaCloud.Sla.sln` (`workshops/ws-m1-skills-mcp-dotnet/`, `workshops/ws-m2-sdd-dotnet/`, `workshops/ws-m2-harness-oracle-dotnet/`)
  - Módulo 3 (Capstone): `GuardiaCloud.CommandCenter.sln` (`workshops/ws-m3-capstone-dotnet/`)

---

## Mapa General por Día (7 Jornadas Presenciales = 52 Horas)

| Día | Horas | Unidades Cubiertas | Foco Principal | Entregable / Salida del Día |
|---|---:|---|---|---|
| **Día 1** | 8 hs | **U1.1** (4 hs) + **U1.2** (4 hs) | Diseño UI con IA + Handoff a .NET y Dominio del IDE (VS Code, Cursor y Windsurf) sobre código C# legado | Prototipo de 3 pantallas + `design-tokens.json` + Componente tipado + PR con los 5 flujos diarios en verde (`dotnet test`) |
| **Día 2** | 10 hs | **U1.3** (4 hs) + **U1.4** (6 hs) | Agentes, Patrones, `SKILL.md`, `Microsoft.Extensions.AI` y Harness Engineering (Claude Code, Codex, Devin, `AGENTS.md` y Hooks) | Skill `dotnet-minimal-api-guardian` + Agente C# `SlaTriageAgent` + `AGENTS.md` curado (<60 líneas) + Hook `PostToolUse` activo |
| **Día 3** | 6 hs | **U1.5** (2 hs) + **U2.1** (4 hs) | Servidores MCP en C# (`ModelContextProtocol` v2.3.0) y Especificaciones Ejecutables (EARS, Given/When/Then y Auditoría Adversarial) | **Entregable Evaluable #1 (15% nota)** completado + `spec.md` y `plan.md` de `001-sla-pause-windows` aprobados |
| **Día 4** | 8 hs | **U2.2** (4 hs) + **U2.3** (4 hs) | Análisis de Impacto Brownfield, Planificación en Grafos (`tasks.md` DAG) e Implementación Full AI vs. HITL con Oráculo `NetArchTest` | Grafo `tasks.md` libre de conflictos + Suite de 7 tests (`NetArchTest` + `WebApplicationFactory`) + Informe `comparativa-hitl-vs-full-ai.md` |
| **Día 5** | 6 hs | **U2.4** (6 hs) | Herramientas para SDD: GitHub Spec Kit (`v1.2.5`), OpenSpec (`v1.15.0` deltas brownfield), AWS Kiro, BMAD y Tessl | **Entregable Evaluable #2 (15% nota)** completado (`001-sla-pause-windows` + delta OpenSpec `cap-p1-pause-budget`) |
| **Día 6** | 8 hs | **U3.1** (2 hs) + **U3.2** (4 hs) + **U3.3** (2 hs) | Proyecto Integrador Capstone (Parte 1): Relevamiento con IA, Constitución, Specs, Prototipo UI, Peer-Review Cruzado y Plan DAG | **Entregable Evaluable #3 (25% nota)** completado sobre `GuardiaCloud.CommandCenter.sln` |
| **Día 7** | 6 hs | **U3.4** (6 hs) | Proyecto Integrador Capstone (Parte 2): 2 Sprints Agénticos en `git worktrees`, Checkpoint `/speckit-converge`, QA Cruzado y Demo | **Entregable Evaluable #4 (35% nota)** + **Entregable Evaluable #5 (10% nota)** (8 tests en verde + Demo + Retrospectiva de métricas) |

---

# DÍA 1 — Diseño Asistido por IA, Handoff a .NET y Dominio del IDE (8 Horas)

> **Decks de apoyo:**
> - `curriculum/2026-11-03_dia-1-paso-a-paso.pptx`
> - `curriculum/slides/dia-1-unidades-1.1-y-1.2-paso-a-paso.pptx`

## Bloque 1 (Mañana · 4 Horas) — Unidad 1.1: Diseño de Producto e Interfaces con IA y Handoff a .NET

### 1. Objetivos de Aprendizaje y Salida Observable
1. Generar un flujo navegable de 3 pantallas a partir de un prompt estructurado de dominio usando **Google Stitch**, **v0**, **Lovable**, **Figma Make** o **Claude Artifacts**.
2. Extraer tokens de diseño (`design-tokens.json`) e invariantes visuales para que las iteraciones posteriores no rompan el layout.
3. Ejecutar un **Handoff limpio hacia .NET 10**: acoplar la interfaz generada al contrato OpenAPI (`ProblemDetails` RFC 9457) de `GuardiaCloud.Sla.Api` o traducirla a un componente tipado Blazor (`.razor`).

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 1.1 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:20` | 20 min | **Bienvenida, Reglas del Juego y Onboarding del Repo Semilla** | Proyectar Slides 1 a 3 de `dia-1-paso-a-paso.pptx`. Presentar la regla de oro (*"La IA abarata generar código, pero encarece no saber especificar ni verificar"*). Hacer que todos clonen el repo semilla, corran `dotnet test` y abran **VS Code, Cursor o Windsurf**. |
| `00:20 – 01:00` | 40 min | **Encuadre Conceptual: Mapa de Herramientas UI y Prompting de Producto** | Proyectar Slide 4. Explicar cuándo usar **Google Stitch** (exploración rápida), **v0 / Lovable** (flujos React/Tailwind completos), **Figma Make** (sobre Design System existente) y **Claude Artifacts** (micro-herramientas interactivas en vivo). Mostrar las **5 capas de un prompt de diseño profesional**. |
| `01:00 – 01:30` | 30 min | **Demo en Vivo: Del Prompt Vago al Contrato C# Tipado + Tokens** | Hacer en vivo el contraste: (1) tirar un prompt vago (*"haceme un dashboard de incidentes"*) y señalar por qué no sirve en ingeniería (inventa campos que no existen en el backend); (2) pegar el prompt estructurado acoplado al record `IncidentSlaSummaryDto` de `GuardiaCloud.Sla.Api`. |
| `01:30 – 02:10` | 40 min | **Workshop 1.1 — Paso 1: Generación de las 3 Pantallas Nucleares** | Proyectar Slide 5. Los participantes trabajan en duplas generando: (1) Tablero de Guardia SLA, (2) Drawer de Registro de Pausa, y (3) Timeline de Auditoría de Incumplimiento. |
| `02:10 – 02:45` | 35 min | **Workshop 1.1 — Paso 2: Estados de Borde y Congelamiento de Tokens** | Hacer que cada dupla fuerce 3 estados de borde sin romper el layout: alerta ámbar al `>= 80%` de SLA consumido, banner de error RFC 9457 (`SLA-422-P1-PAUSE-CAP-EXCEEDED`) y exportación de `ui/design-tokens.json`. |
| `02:45 – 03:30` | 45 min | **Workshop 1.1 — Paso 3: Handoff al Repositorio .NET 10** | Proyectar Slide 6. Usando VS Code / Cursor / Windsurf, cada dupla convierte la tarjeta principal del prototipo en un componente tipado (`SlaStatusCard.razor` o cliente tipado contra OpenAPI) respetando las propiedades exactas del DTO C#. |
| `03:30 – 04:00` | 30 min | **Workshop 1.1 — Paso 4: Revisión Cruzada y Cierre del Bloque** | Dos duplas proyectan su flujo de 3 pantallas y su componente C#. Validar con la checklist de salida de la Unidad 1.1. |

### 3. Guion de Demo en Vivo para el Presentador (Unidad 1.1)
- **Frase clave de apertura:** *"El mayor error cuando un equipo .NET prueba v0, Lovable o Stitch es tratarlos como herramientas para diseñadores aislados. Si no le pasás el contrato de datos de tu API C# en el prompt, la herramienta te dibuja una pantalla hermosa con 8 campos que tu backend no tiene."*
- **Prompt exacto para pegar en vivo (Stitch / v0 / Claude Artifacts):**
  ```text
  Actuá como Diseñador Senior de Producto B2B. Necesito diseñar la consola operativa "GuardiaCloud SLA" para ingenieros de guardia.
  Restricción técnica obligatoria: Los componentes deben mapear exactamente a este contrato DTO de nuestro backend .NET 10 Minimal API:
  - incidentId (string, ej. "INC-2026-1001")
  - clientTier (enum: "Platinum" | "Gold" | "Silver")
  - severity (enum: "P1" | "P2" | "P3")
  - consumedRatio (double entre 0.0 y 1.5)
  - isBreached (bool)
  - pauseWindows (array de { reason: "WaitingForCustomer" | "MaintenanceWindow", startsAtUtc, endsAtUtc })

  Generá 3 vistas conectadas:
  1. Grilla principal con filtro por severity y barra de progreso (verde <0.80, ámbar >=0.80, rojo si isBreached == true).
  2. Modal "Registrar Ventana de Pausa" con aviso visible: "En incidentes P1 la pausa máxima acumulada es de 30 minutos".
  3. Estado de error estandarizado mostrando un payload ProblemDetails RFC 9457 (campos: title, detail, errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED", traceId).
  ```
- **Bloqueos frecuentes en aula y cómo destrabarlos:**
  - *Problema:* El alumno itera el prompt 4 veces y la herramienta le cambia los colores y la navegación entera.
  - *Intervención:* Mostrar cómo pedirle primero a la herramienta que extraiga el bloque JSON de `design-tokens.json` y pegarlo como restricción fija al inicio del prompt siguiente.

---

## Bloque 2 (Tarde · 4 Horas) — Unidad 1.2: Herramientas de Desarrollo con IA (VS Code, Cursor y Windsurf) en .NET 10

### 1. Objetivos de Aprendizaje y Salida Observable
1. Configurar el IDE estándar del curso (**VS Code con GitHub Copilot, Cursor o Windsurf**, o el IDE habitual del desarrollador) con instrucciones de repositorio (`AGENTS.md`, `.github/copilot-instructions.md`, `.cursor/rules`, `.windsurfrules`).
2. Ejecutar con criterio los **5 flujos diarios de ingeniería** sobre una solución `.NET 10` brownfield: comprensión de código legado, refactoring seguro C# 13, generación de tests xUnit con `FakeTimeProvider`, debugging asistido de un bug real y code review de seguridad/performance.
3. Detectar y prevenir los 4 riesgos críticos de la IA en C#: alucinación de paquetes NuGet (*slopsquatting*), consultas `N+1` en EF Core, omisión de `CancellationToken` y uso directo de `DateTime.UtcNow`.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 1.2 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:35` | 35 min | **Estandarización de IDEs (`D-024`), Modos de Uso y Evidencia METR** | Proyectar Slides 7 y 8 de `dia-1-paso-a-paso.pptx`. Explicar los 3 modos en **VS Code + Copilot, Cursor y Windsurf** (Autocomplete vs. Inline Edit vs. Agent Mode). Presentar el estudio RCT de **METR (jul 2025)**: por qué desarrolladores senior tardaron 19% más usando IA sin disciplina de verificación. |
| `00:35 – 01:05` | 30 min | **Configuración de Reglas de Workspace Unificadas** | Mostrar en vivo cómo escribir un `AGENTS.md` breve + `.github/copilot-instructions.md` / `.cursor/rules/dotnet10.mdc` para que cualquier miembro del equipo tenga las mismas restricciones arquitectónicas. |
| `01:05 – 01:30` | 25 min | **Los 4 Errores Clásicos de la IA en C# (.NET 10) + Ejercicio de Reglas** | Mostrar ejemplos reales de código C# defectuoso generado por LLMs (`DateTime.Now`, `.Result`, `N+1`, paquetes NuGet inventados). Los alumnos escriben y commitean las reglas de su workspace (15 min). |
| `01:30 – 01:55` | 25 min | **Workshop 1.2 — Flujo 1: Arqueología y Mapa de Código Legado** | Proyectar Slide 9. Los alumnos usan `@workspace` / `#codebase` sobre `GuardiaCloud.Sla.sln` para trazar el flujo de evaluación de SLA y descubrir un comentario obsoleto/engañoso en `SlaCalculator.cs`. |
| `01:55 – 02:25` | 30 min | **Workshop 1.2 — Flujo 2: Refactoring Seguro a C# 13** | Con Inline Edit / Agent Mode, refactorizar condicionales anidados a *switch expressions* exhaustivos de C# 13, corriendo `dotnet test` tras cada cambio. |
| `02:25 – 03:00` | 35 min | **Workshop 1.2 — Flujo 3: Generación de Tests de Borde con `FakeTimeProvider`** | Proyectar Slide 10. Generar tests parametrizados `[Theory]` en xUnit usando `FakeTimeProvider` (minuto exacto 60.0, cruce de medianoche, pausas solapadas, incidente cerrado). |
| `03:00 – 03:30` | 30 min | **Workshop 1.2 — Flujo 4: Debugging Asistido del Bug `ResolvedAtUtc`** | El test de incidente cerrado falla. Los alumnos usan el agente del IDE para diagnosticar la causa raíz en `SlaCalculator.cs` (`var effectiveEnd = incident.ResolvedAtUtc ?? nowUtc;`) y dejar la suite en verde. |
| `03:30 – 04:00` | 30 min | **Workshop 1.2 — Flujo 5: Code Review Asistido de Seguridad y Cierre del Día 1** | Proyectar Slide 11. Auditar un PR contaminado (secretos en configuración, falta de `CancellationToken`, `N+1` y error 500 crudo). Cerrar conectando con el Día 2 (`SKILL.md`, Hooks y MCP). |

### 3. Guion de Demo en Vivo y Facilitación (Unidad 1.2)
- **Frase clave de apertura:** *"El autocompletado te ahorra tipear; el Agent Mode mal usado te genera 400 líneas de deuda técnica en 10 segundos. Hoy vamos a aprender a domar VS Code, Cursor y Windsurf con reglas explícitas y con `dotnet test` como juez."*
- **Bloqueos frecuentes en aula:**
  - *Problema:* El agente genera tests en el Flujo 3 que usan `DateTimeOffset.UtcNow` real y pasan de casualidad, pero no prueban el borde exacto.
  - *Intervención:* Mostrar en pantalla cómo obligar al agente a instanciar `new FakeTimeProvider(new DateTimeOffset(2026, 10, 30, 12, 0, 0, TimeSpan.Zero))` y avanzar el reloj con `clock.Advance(TimeSpan.FromMinutes(60))`.

---

# DÍA 2 — Agentes, Agent Skills (`SKILL.md`), SDKs .NET y Harness Engineering (10 Horas)

> **Decks de apoyo:**
> - `curriculum/slides/dia-2-unidades-1.3-y-1.4-paso-a-paso.pptx`
> - `curriculum/slides/modulo-1-fundamentos-herramientas-agentes.pptx`
> **Paquetes de Workshop utilizados:**
> - `workshops/ws-m1-skills-mcp-dotnet/` (Fases 1 y 3)
> - `workshops/ws-m2-harness-oracle-dotnet/` (Parte 1: Harness, `AGENTS.md`, Hooks y Subagentes)

## Bloque 1 (4 Horas) — Unidad 1.3: Agentes, Patrones Agénticos y Agent Skills Reutilizables (`SKILL.md`)

### 1. Objetivos de Aprendizaje y Salida Observable
1. Distinguir entre un *workflow determinista* y un *agente autónomo* con bucle de herramientas (*Percepción $\rightarrow$ Razonamiento $\rightarrow$ Acción $\rightarrow$ Observación*).
2. Empaquetar conocimiento de arquitectura del equipo en una **Agent Skill (`SKILL.md` + `references/` + `scripts/`)** bajo el estándar abierto `agentskills.io` con *progressive disclosure*.
3. Construir un agente programático en C# con **`Microsoft.Extensions.AI` (`v10.11.0`, `IChatClient`, `UseFunctionInvocation`, `AIFunctionFactory`)** y conocer su integración con **`Microsoft.Agents.AI` (`v1.27.0`)** y **Azure AI Foundry**.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 1.3 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:40` | 40 min | **Anatomía del Loop Agéntico y los 4 Patrones de Orquestación** | Explicar el bucle de tool-calling, cuándo NO usar un agente (si el flujo es fijo) y los 4 patrones: *Prompt Chaining*, *Routing*, *Orchestrator-Workers* y *Evaluator-Optimizer*. |
| `00:40 – 01:10` | 30 min | **El Estándar Abierto `SKILL.md` (`agentskills.io`) y Progressive Disclosure** | Mostrar por qué meter todas las normas de la consultora en un prompt gigante degrada al modelo, mientras que una carpeta `.agents/skills/<nombre>/` carga solo ~50 tokens de YAML y abre `references/` y `scripts/` bajo demanda. |
| `01:10 – 01:30` | 20 min | **SDKs de Agentes en .NET 10 (`Microsoft.Extensions.AI` v10.11.0 y `Microsoft.Agents.AI` v1.27.0)** | Mostrar cómo `IChatClient` y `FunctionInvokingChatClient` estandarizan el bucle agéntico en C# sobre Azure OpenAI / Foundry (comparando brevemente con Claude Agent SDK y OpenAI Agents SDK). |
| `01:30 – 03:05` | 95 min | **Workshop (`ws-m1-skills-mcp-dotnet` — Fase 1): Construcción y Verificación de `SKILL.md`** | Abrir `workshops/ws-m1-skills-mcp-dotnet/01-GUIA-PASO-A-PASO.md` (Fase 1). Los alumnos completan `.agents/skills/dotnet-minimal-api-guardian/SKILL.md`, vinculan `references/rfc9457-catalogo-errores.md` y hacen pasar `./scripts/verify-minimal-api.sh`. |
| `03:05 – 04:00` | 55 min | **Workshop (`ws-m1-skills-mcp-dotnet` — Fase 3): Agente de Triage en C# (`SlaTriageAgent.cs`)** | Los alumnos implementan `SlaTriageAgent.cs` usando `ChatClientBuilder`, `UseFunctionInvocation(c => c.MaximumIterationsPerRequest = 4)` y `AIFunctionFactory.Create`, ejecutando el test de bucle multi-herramienta en xUnit. |

### 3. Notas Clave del Facilitador (Unidad 1.3)
- **Referencia exacta del repo:** `workshops/ws-m1-skills-mcp-dotnet/02-GUIA-FACILITADOR-Y-RUBRICA.md`.
- **Demostración clave:** Mostrar qué ocurre si un agente entra en un bucle infinito de llamadas a herramientas y cómo `MaximumIterationsPerRequest = 4` en `FunctionInvokingChatClient` actúa como cortafuegos de costos en producción.

---

## Bloque 2 (6 Horas) — Unidad 1.4: Harness Engineering (Claude Code, OpenAI Codex y Devin)

### 1. Objetivos de Aprendizaje y Salida Observable
1. Diseñar una jerarquía limpia de archivos de contexto (`AGENTS.md` + puente `@AGENTS.md` en `CLAUDE.md`) aplicando la evidencia del estudio de **ETH Zurich (`arXiv:2602.11988`)**.
2. Configurar **Claude Code (`v2.1.314`)** con permisos granulares, modo `/plan`, subagentes en `.claude/agents/` y **Hooks deterministas (`PostToolUse`)** que ejecuten `dotnet build` y `dotnet test` automáticamente tras cada edición.
3. Operar **OpenAI Codex (`rust-v0.166.0`)** en terminal/cloud y evaluar cuándo delegar tickets autónomos a **Devin** (usando *Knowledge* y *Playbooks*).

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 1.4 — 360 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **¿Qué es el Harness? Interoperabilidad `AGENTS.md` / `CLAUDE.md` y Estudio ETH Zurich** | Explicar las 4 capas del arnés (Contexto, Herramientas, Sandboxing, Hooks de retroalimentación). Mostrar el hallazgo de **ETH Zurich (`arXiv:2602.11988`)**: los `AGENTS.md` autogenerados por LLMs bajan la precisión y suben 20–23% el gasto de tokens; los curados por humanos (<60–80 líneas) mejoran el éxito. |
| `00:45 – 01:30` | 45 min | **Deep-Dive en Claude Code (`v2.1.314`) para Proyectos .NET** | Demostrar en vivo `/plan`, gestión de contexto (`/compact`, `/clear`), subagentes (`.claude/agents/`), hooks (`PreToolUse`, `PostToolUse`, `Stop`) y modo headless `claude -p` para pipelines de GitHub Actions / Azure DevOps. |
| `01:30 – 02:15` | 45 min | **Deep-Dive en OpenAI Codex (`rust-v0.166.0`) y Devin (Cognition)** | Mostrar los modos de sandbox de Codex CLI (`read-only`, `workspace-write`, `danger-full-access`), delegación paralela y cómo estructurar *Knowledge* y *Playbooks* en Devin para tareas repetitivas de migración .NET. |
| `02:15 – 03:15` | 60 min | **Workshop (`ws-m2-harness-oracle-dotnet` — Fase 1): Poda Quirúrgica de `AGENTS.md`** | Abrir `workshops/ws-m2-harness-oracle-dotnet/01-GUIA-PASO-A-PASO.md`. Los alumnos toman el `AGENTS.md` inflado de `starter/` y lo reducen a <60 líneas de alta señal verificables, creando `CLAUDE.md` con `@AGENTS.md`. |
| `03:15 – 04:20` | 65 min | **Workshop — Fase 2: Configuración del Hook Determinista `PostToolUse` en `.NET`** | Configurar `.claude/settings.json` para que cada edición de código C# dispare `./scripts/post-edit-dotnet-hook.sh` (`dotnet build --no-restore` + `dotnet test`). Probar cómo el agente se autocorrige cuando introduce un error de compilación. |
| `04:20 – 05:10` | 50 min | **Workshop — Fase 3: Creación del Subagente Revisor de Arquitectura** | Configurar `.claude/agents/dotnet-arch-reviewer.md` con herramientas restringidas a solo lectura (`Read`, `Grep`, `Glob`) para auditar cambios sin riesgo de mutación. |
| `05:10 – 06:00` | 50 min | **Workshop — Fase 4: Comparativa Práctica Lado a Lado (Claude Code vs. Codex)** | Resolver el mismo requerimiento acotado de `.NET` usando ambos harnesses y comparar en plenaria: tiempo de resolución, adherencia a `AGENTS.md` y limpieza del diff. |

---

# DÍA 3 — Servidores MCP en C# (.NET 10) y Especificaciones Ejecutables (6 Horas)

> **Decks de apoyo:**
> - `curriculum/slides/dia-3-unidades-1.5-y-2.1-paso-a-paso.pptx`
> - `curriculum/slides/modulo-1-fundamentos-herramientas-agentes.pptx` & `modulo-2-spec-driven-development.pptx`
> **Paquetes de Workshop utilizados:**
> - `workshops/ws-m1-skills-mcp-dotnet/` (Fase 2 y Cierre Evaluable #1 — 15% de la nota)
> - `workshops/ws-m2-sdd-dotnet/` (Parte 1: Descubrimiento Adversarial y Redacción de `spec.md` + `plan.md`)

## Bloque 1 (2 Horas) — Unidad 1.5: Model Context Protocol (MCP) en .NET 10 y Azure

### 1. Objetivos de Aprendizaje y Salida Observable
1. Conectar servidores MCP existentes (**Azure MCP Server `microsoft/mcp`**, GitHub / Azure DevOps, bases de datos) a VS Code, Cursor, Windsurf o Claude Code bajo principio de mínimo privilegio.
2. Construir, asegurar y testear un **Servidor MCP propio en C#** usando el paquete NuGet oficial **`ModelContextProtocol` (`v2.3.0`)** con defensa activa contra *Indirect Prompt Injection*.
3. Completar y entregar el **Entregable Evaluable #1 del curso (15% de la nota final)**.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 1.5 — 120 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **Arquitectura MCP, SDK Oficial de C# (`v2.3.0`) y Seguridad Defensiva** | Explicar `Host -> Client -> Server`, primitivas (`Tools`, `Resources`, `Prompts`), transportes (`stdio` vs. `ModelContextProtocol.AspNetCore` Streamable HTTP) y por qué en `stdio` ningún log puede ir a `stdout`. Demostrar el vector de ataque de *Indirect Prompt Injection* en tickets de soporte (`INC-2026-1002`). |
| `00:45 – 01:40` | 55 min | **Workshop (`ws-m1-skills-mcp-dotnet` — Fase 2): Implementación de `SlaMcpTools.cs` en C#** | Los alumnos implementan `inspect_incident_sla_status` (con sanitización `SanitizeUntrustedNotes`) y `validate_rfc9457_contract` decorados con `[McpServerTool(ReadOnlyHint = true, DestructiveHint = false)]`. |
| `01:40 – 02:00` | 20 min | **Prueba Integrada en Vivo y Entrega del Módulo 1 (15% Nota Final)** | Correr `dotnet test` (6/6 tests en verde en `GuardiaCloud.Sla.McpWorkshop.sln`), registrar `.mcp.json` en VS Code / Cursor / Claude Code y calificar con la rúbrica de 100 puntos de `02-GUIA-FACILITADOR-Y-RUBRICA.md`. |

---

## Bloque 2 (4 Horas) — Unidad 2.1: El Arte de Especificar (EARS, Given/When/Then y Auditoría Adversarial)

### 1. Objetivos de Aprendizaje y Salida Observable
1. Comprender la evidencia empírica de **Larbi et al. (`arXiv:2507.20439`)** y **SWE-EVO (`arXiv:2512.18470`)**: por qué más del 60% de los fallos de agentes nacen de requerimientos ambiguos o incompletos.
2. Utilizar al agente en rol de **Crítico Adversarial (*Spec Critic*)** para destapar huecos lógicos antes de escribir código.
3. Redactar una **Especificación Funcional (`spec.md`)** en notación **EARS + Given/When/Then** y una **Especificación Técnica (`plan.md`)** para `.NET 10` sin ambigüedades pendientes.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 2.1 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **Por qué Falla el 'Vibe Coding' en Sistemas Empresariales: Evidencia y Jerarquía SDD** | Presentar los datos de Larbi et al. (-20 a -40 pp en Pass@1 por ambigüedad) y SWE-EVO. Introducir la pirámide documental: `Constitución` $\rightarrow$ `Spec Funcional (EARS/GWT)` $\rightarrow$ `Spec Técnica (plan.md + ADRs)` $\rightarrow$ `Tareas (DAG)`. |
| `00:45 – 01:30` | 45 min | **Sintaxis EARS, Escenarios Given/When/Then y el Prompt *Spec Critic*** | Enseñar los 5 patrones de EARS (*Ubiquitous, Event-Driven `WHEN`, State-Driven `WHILE`, Unwanted Behavior `IF/THEN`, Where*). Demostrar en vivo cómo un prompt *Spec Critic* encuentra 7 huecos en un pedido de negocio aparentemente simple. |
| `01:30 – 02:05` | 35 min | **Workshop (`ws-m2-sdd-dotnet` — Paso 1): Auditoría Adversarial del Brief del Cliente** | Abrir `workshops/ws-m2-sdd-dotnet/starter/brief-cliente-ambiguo.md`. Las duplas usan su agente para listar las 7 ambigüedades ocultas sobre las ventanas de pausa de SLA. |
| `02:05 – 02:35` | 30 min | **Workshop — Paso 2: Entrevista Role-Play con el 'Gerente de Operaciones'** | El presentador actúa como Gerente de Operaciones (usando la hoja de respuestas de `02-GUIA-FACILITADOR-Y-RUBRICA.md`) y responde solo lo que las duplas preguntan explícitamente. |
| `02:35 – 03:25` | 50 min | **Workshop — Paso 3: Redacción de `specs/001-sla-pause-windows/spec.md`** | Redacción de los requisitos en notación EARS y criterios de aceptación Given/When/Then (incluyendo fusión de intervalos solapados y tope de 30 min en P1). |
| `03:25 – 04:00` | 35 min | **Workshop — Paso 4: Redacción de `plan.md` y Peer-Review Cruzado** | Definir el contrato HTTP Minimal API, DTOs C#, códigos RFC 9457 (`SLA-400-INVALID-PAUSE-WINDOW`, `SLA-400-UNSUPPORTED-PAUSE-REASON`, `SLA-422-P1-PAUSE-CAP-EXCEEDED`) y auditar la spec de otra dupla. |

---

# DÍA 4 — Análisis de Impacto, Grafos de Tareas (DAG), Oráculos .NET y Full AI vs. HITL (8 Horas)

> **Decks de apoyo:**
> - `curriculum/slides/dia-4-unidades-2.2-y-2.3-paso-a-paso.pptx`
> - `curriculum/slides/modulo-2-spec-driven-development.pptx`
> **Paquetes de Workshop utilizados:**
> - `workshops/ws-m2-sdd-dotnet/` (Descomposición en `tasks.md`)
> - `workshops/ws-m2-harness-oracle-dotnet/` (Parte 2: Oráculo `NetArchTest.Rules` v1.3.2 y Laboratorio Comparativo HITL vs. Full AI)

## Bloque 1 (4 Horas) — Unidad 2.2: Estimación, Análisis de Impacto Brownfield y Planificación en Grafos (DAG)

### 1. Objetivos de Aprendizaje y Salida Observable
1. Ejecutar un **Análisis de Impacto Brownfield** con agentes en modo solo lectura para mapear acoplamientos, contratos afectados y riesgos de regresión en una solución `.NET 10`.
2. Descomponer `plan.md` en un **Grafo Acíclico Dirigido (`tasks.md`)** con fronteras explícitas de archivos para evitar la trampa del **27.67% de conflictos de merge** en trabajo paralelo (*AgenticFlict*).
3. Recalibrar la estimación de ingeniería separando el **tiempo de generación** (comprimido por la IA) del **tiempo de verificación, revisión e integración**.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 2.2 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **Análisis de Impacto con Agentes y el Problema de los Conflictos Paralelos (`AgenticFlict`)** | Mostrar cómo usar `/plan` o modo lectura para auditar qué proyectos `.csproj`, entidades y tests toca un cambio. Explicar por qué lanzar 3 agentes en paralelo sin fronteras de archivos rompe el 27.67% de los merges. |
| `00:45 – 01:30` | 45 min | **Nuevas Reglas de Estimación con IA y Prevención del 'Workslop'** | Explicar cómo estimar en consultoría cuando el código se escribe rápido pero la revisión humana y las pruebas de integración son el cuello de botella. Presentar la plantilla de estimación de dos columnas (*Generación vs. Verificación*). |
| `01:30 – 02:10` | 40 min | **Workshop 2.2 — Paso 1: Mapa de Impacto Automatizado sobre `GuardiaCloud.Sla.sln`** | Las duplas ejecutan un prompt de análisis de impacto sobre el repositorio y generan la matriz de archivos afectados por `001-sla-pause-windows`. |
| `02:10 – 03:00` | 50 min | **Workshop 2.2 — Paso 2: Construcción del Grafo DAG en `tasks.md`** | Descomponer la implementación en 6 a 8 tareas atómicas (<150 LOC), declarando dependencias secuenciales (Fase 1: contratos y tests en rojo) vs. tareas paralelizables `[P]` con conjuntos de archivos disjuntos. |
| `03:00 – 03:35` | 35 min | **Workshop 2.2 — Paso 3: Ejercicio de Estimación Comparada** | Estimar cada tarea de `tasks.md` bajo modalidad tradicional vs. asistida por IA (asignando presupuesto de tokens y tiempo de code review). |
| `03:35 – 04:00` | 25 min | **Workshop 2.2 — Paso 4: Auditoría de Colisiones del Grafo** | Intercambiar `tasks.md` entre duplas y verificar que ninguna tarea marcada `[P]` edite el mismo archivo `.cs`. |

---

## Bloque 2 (4 Horas) — Unidad 2.3: Implementación (Full AI vs. Human-in-the-Loop) y Oráculos en .NET 10

### 1. Objetivos de Aprendizaje y Salida Observable
1. Decidir por tarea cuándo operar en modo **Human-in-the-Loop (HITL)** vs. **Full AI (Autónomo en `git worktree`)** según la criticidad de negocio y la fortaleza del oráculo.
2. Construir un **Oráculo de Verificación Determinista en .NET 10** combinando compilación estricta, **Fitness Functions de Arquitectura (`NetArchTest.Rules` v1.3.2)** y pruebas de integración (`WebApplicationFactory<Program>`).
3. Ejecutar el laboratorio comparativo midiendo tiempo real, iteraciones y limpieza del diff entre HITL y Full AI.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 2.3 — 240 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **El Espectro de Autonomía (HITL vs. Full AI) y Aislamiento con `git worktree`** | Explicar cómo funciona `git worktree add ../worktree-feat-b -b feat/b` para correr un agente autónomo en paralelo sin ensuciar el árbol de trabajo principal. Presentar la matriz de decisión por riesgo y completitud del oráculo. |
| `00:45 – 01:30` | 45 min | **Diseño del Oráculo de 4 Capas en .NET 10 y `NetArchTest.Rules` (`v1.3.2`)** | Demostrar por qué los tests funcionales no alcanzan cuando programa un agente autónomo (el agente puede meter `Microsoft.AspNetCore` o acceso a datos dentro de `Domain` con tal de que el test pase). Mostrar `ArchitectureFitnessTests.cs`. |
| `01:30 – 02:15` | 45 min | **Workshop (`ws-m2-harness-oracle-dotnet` — Fase 3): Oráculo Arquitectónico con `NetArchTest`** | Los alumnos escriben las 3 reglas en `ArchitectureFitnessTests.cs`, detectan la violación sembrada en `LegacyVibeCodedHelper.cs`, la eliminan y dejan el oráculo arquitectónico en verde. |
| `02:15 – 03:00` | 45 min | **Workshop — Fase 4A (Modo HITL): Cálculo de Créditos Financieros Mensuales** | Implementar la Tarea A (lógica financiera con redondeo bancario `MidpointRounding.ToEven` y topes contractuales) en modo **Human-in-the-Loop** con checkpoints de aprobación humana. |
| `03:00 – 03:40` | 40 min | **Workshop — Fase 4B (Modo Full AI en `git worktree`): Resumen de Guardia** | Crear un `git worktree`, escribir primero los tests de aceptación en rojo para la Tarea B (endpoint de exportación de resumen de turno) y dejar que el agente la resuelva en bucle autónomo contra `dotnet test`. |
| `03:40 – 04:00` | 20 min | **Debrief Empírico y Cierre del Informe `comparativa-hitl-vs-full-ai.md`** | Comparar en el pizarrón las métricas reales medidas por las duplas (tiempo de reloj, número de corridas de `dotnet test`, líneas modificadas y defectos). |

---

# DÍA 5 — Herramientas para SDD: GitHub Spec Kit (`v1.2.5`) y OpenSpec (`v1.15.0`) (6 Horas)

> **Decks de apoyo:**
> - `curriculum/slides/dia-5-unidad-2.4-sdd-tools-paso-a-paso.pptx`
> - `curriculum/slides/modulo-2-spec-driven-development.pptx`
> **Paquete de Workshop utilizado:**
> - `workshops/ws-m2-sdd-dotnet/` (Cierre del Entregable Evaluable #2 — 15% de la nota final)

## Jornada Completa (6 Horas) — Unidad 2.4: Herramientas para Spec-Driven Development (SDD)

### 1. Objetivos de Aprendizaje y Salida Observable
1. Clasificar las herramientas SDD según la taxonomía de **Martin Fowler / Birgitta Böckeler** (*Spec-first*, *Spec-anchored*, *Spec-as-source*) y comparar **GitHub Spec Kit**, **OpenSpec**, **AWS Kiro**, **BMAD Method** y **Tessl**.
2. Ejecutar un flujo de corrección de bug (`/speckit-bug-*`) y de feature completa (`/speckit-constitution` $\rightarrow$ `/speckit-converge`) con **GitHub Spec Kit (`v1.2.5`)** sobre `.NET 10`.
3. Ejecutar un flujo de **deltas brownfield** (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`) con **Fission-AI OpenSpec (`v1.15.0`)** y entregar el **Entregable Evaluable #2 (15% de la nota)**.

### 2. Cronograma Minuto a Minuto del Presentador (Unidad 2.4 — 360 min)

| Reloj | Duración | Actividad | Qué proyectar / Qué hace el presentador |
|---|---:|---|---|
| `00:00 – 00:45` | 45 min | **Taxonomía SDD (*Spec-first / Spec-anchored / Spec-as-source*) y Panorama de Mercado** | Explicar por qué *Spec-anchored* es el estándar pragmático hoy en consultoría `.NET`. Comparar AWS Kiro (`.kiro/specs/`), BMAD (`v6.12.4`) y Tessl (`tessl.io`). |
| `00:45 – 01:30` | 45 min | **GitHub Spec Kit (`v1.2.5`) vs. OpenSpec (`v1.15.0`): Cuándo Usar Cada Uno** | Demostrar en vivo la estructura de directorios de Spec Kit (`.specify/memory/constitution.md`, `specs/001-.../`, `/speckit-converge`) frente a la estructura de deltas de OpenSpec (`openspec/specs/` + `openspec/changes/archive/`). |
| `01:30 – 02:15` | 45 min | **Workshop (`ws-m2-sdd-dotnet` — Fase 1): Flujo `/speckit-bug-*` en `.NET 10`** | Abrir `workshops/ws-m2-sdd-dotnet/01-GUIA-PASO-A-PASO.md`. Documentar y corregir el bug de deriva de SLA en incidentes resueltos generando `.specify/bugs/resolved-sla-breach-drift/report.md` y su test de regresión. |
| `02:15 – 03:45` | 90 min | **Workshop — Fase 2: Implementación y Convergencia con Spec Kit (`001-sla-pause-windows`)** | Ejecutar `/speckit-implement` y `/speckit-converge` para construir el cálculo de ventanas de pausa fusionadas y el endpoint `POST /api/incidents/{id}/pauses` verificando contra `spec.md`. |
| `03:45 – 05:00` | 75 min | **Workshop — Fase 3: Cambio Brownfield con OpenSpec (`cap-p1-pause-budget`)** | El negocio introduce un cambio regulatorio sobre el sistema ya construido: limitar a 30 minutos las pausas en incidentes P1. Los alumnos crean la propuesta en `openspec/changes/cap-p1-pause-budget/`, implementan el código `SLA-422-P1-PAUSE-CAP-EXCEEDED`, pasan los tests y archivan el delta en `openspec/changes/archive/`. |
| `05:00 – 06:00` | 60 min | **Workshop — Fase 4: Empaquetado del Flujo SDD del Equipo y Evaluación del Módulo 2 (15% Nota)** | Verificar las 4 suites de integración en `GuardiaCloud.Sla.Tests` (`dotnet test` 100% en verde) y calificar con la rúbrica oficial de `workshops/ws-m2-sdd-dotnet/02-GUIA-FACILITADOR-Y-RUBRICA.md`. |

---

# DÍAS 6 Y 7 — Módulo 3: Proyecto Integrador Capstone en Equipos (14 Horas = 70% de la Nota)

> **Decks de apoyo:**
> - `curriculum/slides/dia-6-y-7-modulo-3-capstone-paso-a-paso.pptx`
> - `curriculum/slides/modulo-3-capstone-proyecto-integrador.pptx`
> **Paquete de Workshop utilizado:**
> - `workshops/ws-m3-capstone-dotnet/` (`GuardiaCloud.CommandCenter.sln`)

## Día 6 (8 Horas) — Unidades 3.1, 3.2 y 3.3: Descubrimiento, Especificación, Auditoría Cruzada y Plan DAG

### 1. Estructura y Roles por Equipo (3 a 5 Integrantes)
Al iniciar el Día 6, el presentador organiza la clase en equipos de 3 a 5 personas y asigna los 4 roles rotativos sobre `workshops/ws-m3-capstone-dotnet/starter/`:
1. **Spec & Architecture Lead:** Custodia `AGENTS.md`, `spec.md` y `plan.md`.
2. **Harness, MCP & Backend Lead:** Configura hooks `.NET`, servidor MCP y lógica de dominio en `CommandCenterEvaluator.cs`.
3. **QA, Verification Oracle & Security Lead:** Escribe primero los tests en `CommandCenterTests.cs` (`NetArchTest.Rules` + `WebApplicationFactory`).
4. **UI Prototype & API Integration Lead:** Diseña el prototipo del Tablero Ejecutivo (`FEAT-303`) y verifica los contratos DTO / RFC 9457.

### 2. Cronograma Minuto a Minuto del Presentador — Día 6 (480 min)

| Unidad / Reloj | Duración | Actividad | Qué proyectar / Rol del presentador y de los equipos |
|---|---:|---|---|
| **U3.1** · `00:00 – 00:40` | 40 min | **Entrega del Pliego de Licitación y Auditoría Brownfield con IA** | Los equipos abren `pliego-licitacion-cliente.md` y auditan el código de `starter/` (`GuardiaCloud.CommandCenter.sln`) con sus agentes para detectar `BUG-301` y las 8 ambigüedades deliberadas del pliego. |
| **U3.1** · `00:40 – 01:25` | 45 min | **Entrevista en Vivo con el 'Director de Operaciones' (Role-Play)** | El presentador usa la tabla de 8 respuestas oficiales de `workshops/ws-m3-capstone-dotnet/02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md` (umbral exacto `>= 80.0%`, cooldown de 15 min, prefijo `FM-DUAL-`, doble aprobador distinto, etc.). |
| **U3.1** · `01:25 – 02:00` | 35 min | **Cierre del Documento de Alcance Funcional** | Cada equipo consolida las 8 definiciones de negocio validadas. |
| **U3.2** · `02:00 – 03:30` | 90 min | **Constitución `AGENTS.md` y Redacción de `specs/command-center-v2/spec.md`** | Los equipos configuran `AGENTS.md` + `CLAUDE.md` y redactan los requisitos EARS + Given/When/Then para `BUG-301`, `FEAT-301`, `FEAT-302` y `FEAT-303`. |
| **U3.2** · `03:30 – 05:00` | 90 min | **Redacción de `plan.md` (Contratos HTTP y Códigos `CC-4xx`) + Prototipo UI** | Definir esquemas de request/response, códigos RFC 9457 (`CC-400-SAME-APPROVER`, `CC-422-INVALID-DUAL-TOKEN`) y generar el prototipo interactivo de `FEAT-303`. |
| **U3.2** · `05:00 – 06:00` | 60 min | **Auditoría Adversarial Cruzada entre Equipos (*Cross-Team Spec Review*)** | El Equipo A audita la especificación del Equipo B usando su agente como *Spec Critic*. Ningún equipo pasa a la Unidad 3.3 con frases vagas sin umbrales numéricos. |
| **U3.3** · `06:00 – 07:15` | 75 min | **Análisis de Impacto y Construcción del Grafo de Tareas (`tasks.md`)** | Dividir el trabajo en tareas atómicas para el Día 7, asignando modo **Full AI en `git worktree`** (`BUG-301`, `FEAT-301`, `FEAT-303`) vs. **HITL** (`FEAT-302` control dual regulatorio). |
| **U3.3** · `07:15 – 08:00` | 45 min | **Congelamiento de Contratos en `main` y Entrega del Entregable #3 (25% Nota)** | Los equipos congelan las firmas de DTOs en `main` y entregan el paquete de diseño/planificación (**25% de la nota final del curso**). |

---

## Día 7 (6 Horas) — Unidad 3.4: Dos Sprints de Implementación Agéntica, QA Cruzado, Demo y Retrospectiva

### 1. Cronograma Minuto a Minuto del Presentador — Día 7 (360 min)

| Reloj | Duración | Actividad | Qué proyectar / Rol del presentador y de los equipos |
|---|---:|---|---|
| `00:00 – 02:00` | 120 min | **Sprint 1: Oráculo de Pruebas Primero + Resolución de `BUG-301` y `FEAT-301`** | El *QA & Oracle Lead* escribe primero los tests de arquitectura (`NetArchTest.Rules`) e integración en `CommandCenterTests.cs`. En paralelo, los desarrolladores abren sus `git worktrees` y resuelven la idempotencia de webhooks (`BUG-301`) y el escalamiento proactivo al 80% con cooldown de 15 min (`FEAT-301`). |
| `02:00 – 02:30` | 30 min | **Checkpoint Obligatorio de Convergencia (`/speckit-converge`)** | Todos los equipos hacen merge de sus ramas del Sprint 1 a `main`, corren `dotnet test` y ejecutan `/speckit-converge` para detectar cualquier desviación respecto a `spec.md` antes de seguir. |
| `02:30 – 04:30` | 120 min | **Sprint 2: Exención Regulatoria Dual (`FEAT-302` en HITL) y Tablero Ejecutivo (`FEAT-303` en Full AI)** | Implementación supervisada paso a paso de `FEAT-302` (validando `CC-400-SAME-APPROVER` y `CC-422-INVALID-DUAL-TOKEN`) e implementación autónoma de `FEAT-303` + conexión con el prototipo UI. |
| `04:30 – 05:15` | 45 min | **QA Cruzado de Aceptación entre Equipos** | El Equipo B ejecuta pruebas contra los endpoints del Equipo A guiándose únicamente por el `spec.md` del Equipo A, verificando que los 8 tests del oráculo pasen en limpio (`dotnet test`). |
| `05:15 – 06:00` | 45 min | **Demos en Vivo (Entregable #4 — 35%) y Retrospectiva de Métricas (Entregable #5 — 10%)** | Cada equipo dispone de 10 minutos para: (1) demostrar su solución `.NET 10` andando en vivo con los 8 tests en verde, y (2) presentar su tabla de métricas reales (`retrospectiva-metricas.md`: % tareas Full AI vs. HITL, tiempo de generación vs. verificación, conflictos de merge evitados y 3 acuerdos para llevar a la consultora el lunes). |

---

## Resumen de las 5 Rúbricas Oficiales de Evaluación del Curso (100% de la Nota)

| # | Entregable | Unidad de Entrega | Peso | Ubicación de la Rúbrica Analítica (100 pts) y Solución de Referencia |
|---|---|---|---:|---|
| **#1** | **Skill de Equipo (`SKILL.md`) + Servidor MCP en C# + Agente `Extensions.AI`** | Cierre Módulo 1 (U1.5) | **15%** | `workshops/ws-m1-skills-mcp-dotnet/02-GUIA-FACILITADOR-Y-RUBRICA.md` (`solution/`: 6 tests pasando) |
| **#2** | **Ciclo SDD Completo (`spec.md` EARS/GWT + Spec Kit + Delta OpenSpec)** | Cierre Módulo 2 (U2.4) | **15%** | `workshops/ws-m2-sdd-dotnet/02-GUIA-FACILITADOR-Y-RUBRICA.md` (`solution/`: 4 suites pasando) |
| **#3** | **Constitución `AGENTS.md`, Specs, Prototipo UI y Grafo `tasks.md` del Capstone** | Módulo 3 (Cierre U3.3) | **25%** | `workshops/ws-m3-capstone-dotnet/02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md` (Rúbrica A) |
| **#4** | **Sistema `.NET 10` Funcionando, Oráculo (`NetArchTest` + `WebApplicationFactory`) y Demo** | Módulo 3 (Cierre U3.4) | **35%** | `workshops/ws-m3-capstone-dotnet/02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md` (Rúbrica B — `solution/`: 8 tests pasando) |
| **#5** | **Retrospectiva de Ingeniería Basada en Métricas (`retrospectiva-metricas.md`)** | Módulo 3 (Cierre U3.4) | **10%** | `workshops/ws-m3-capstone-dotnet/02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md` (Rúbrica C) |
