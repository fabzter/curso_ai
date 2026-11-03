# Temario v2 (Propuesta Evolucionada): Desarrollo de Software con IA (.NET & Azure)

- **Fecha:** 30 de octubre de 2026
- **Autores:** Max Déboli & Fabrizio Hernández
- **Base:** Evolución sobre el borrador inicial v1 (`2026-10-28_temario-desarrollo-sw-con-ia.md`), adaptada a consultoría de ingeniería sobre stack **.NET + Azure** y con talleres prácticos (Workshops) detallados por unidad.

---

## Qué evolucionamos en esta versión v2 (Resumen de mejoras)

1. **Aterrizaje de punta a punta en el ecosistema .NET y Azure:**
   - **IDEs (simple y estándar):** el curso se dicta sobre **VS Code (con GitHub Copilot), Cursor y Windsurf**. Cada participante puede usar su IDE habitual si lo prefiere, pero las demos, guías y soporte del aula se basan en estos tres.
   - **Agentes propios en .NET (Unidad 1.3):** incorporamos **`Microsoft.Extensions.AI`** (`IChatClient`) y **Microsoft Agent Framework (`Microsoft.Agents.AI`, sucesor unificado de Semantic Kernel + AutoGen)** conectado a **Azure AI Foundry**, en lugar de limitarnos a SDKs de Python/TypeScript.
   - **Servidores MCP en C# (Unidad 1.5):** el taller práctico usa el **SDK oficial de C# para MCP (`ModelContextProtocol` y `ModelContextProtocol.AspNetCore` en NuGet, v2.3+)** y suma el **Azure MCP Server oficial (`microsoft/mcp`)**.
   - **Oráculo de verificación en .NET (Módulos 2 y 3):** aterrizamos el concepto de *"tests como oráculo"* con **xUnit**, **`WebApplicationFactory`**, **Testcontainers** (SQL Server / PostgreSQL / Redis reales en contenedor) y tests de arquitectura con **`NetArchTest`** para evitar que el agente rompa capas.
2. **Cumplimiento real del 60–70% de práctica guiada (Workshops de 2,5 a 3,75 hs por unidad):**
   - En el borrador v1, los bloques explícitamente prácticos sumaban ~36% de los Módulos 1 y 2. En esta v2 comprimimos la teoría expositiva y convertimos el corazón de cada unidad en un **Workshop práctico estructurado**, logrando **62,5% de práctica real en los Módulos 1 y 2** (y **70% en el total de las 52 horas**).
3. **Un "Repositorio Semilla" (Brownfield .NET + Azure) como hilo conductor desde el Día 1:**
   - Para que las 6 horas de implementación del Módulo 3 rindan al máximo sin perder tiempo en *boilerplate*, trabajamos desde la Unidad 1.2 sobre una solución empresarial .NET de referencia. En cada unidad construís una pieza del *harness* (`AGENTS.md`, Skills de C#, servidor MCP en C#, pipeline SDD) que tu equipo reutiliza directamente en el proyecto final del Módulo 3.
4. **Actualización de herramientas SDD a sus versiones vigentes (octubre 2026):**
   - En **GitHub Spec Kit (`v1.2.5`)** actualizamos el flujo completo de skills (`/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` y **`/speckit-converge`**, más la extensión de bugs `/speckit-bug-*`).
   - En **OpenSpec (`v1.15.0`)** destacamos su flujo de **deltas sobre código existente (brownfield)** (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`), clave para el trabajo diario de una consultora sobre sistemas productivos.

---

## Resumen del curso

Programa intensivo de **52 horas** que lleva a equipos de ingeniería de usar la IA como un chat ad-hoc ("vibe coding") a **operar sistemas de agentes con ingeniería de contexto (Harness Engineering) y Desarrollo Guiado por Especificaciones (SDD)**, cerrando con la entrega de un proyecto real sobre **.NET y Azure** construido de punta a punta.

- **Perfil de los participantes:** desarrolladores, tech leads y arquitectos con experiencia en Git, desarrollo en **.NET (C# / ASP.NET Core)** o frontend moderno, servicios en **Azure** y trabajo en equipo ágil.
- **Enfoque pedagógico:** cada unidad combina **35–38% de marco conceptual y demostración en vivo** con **62–65% de Workshop práctico guiado** (y casi 90% de práctica en el Módulo 3). Todos los artefactos que construís en los Módulos 1 y 2 se encadenan hacia el proyecto integrador del Módulo 3.

| Módulo | Unidades | Horas | Horas de Workshop |
|---|---|---:|---:|
| **1. Herramientas de IA y Harness Engineering** | 1.1 Diseño · 1.2 Herramientas de desarrollo · 1.3 Agentes y Skills · 1.4 Harness Engineering · 1.5 MCPs | 20 hs | 12,5 hs (62,5%) |
| **2. Metodologías adaptadas a la IA (SDD)** | 2.1 Spec · 2.2 Estimación, impacto y planning · 2.3 Implementation (Full AI vs. HITL) · 2.4 Herramientas para SDD | 18 hs | 11,25 hs (62,5%) |
| **3. Ejecución de Proyecto de Desarrollo** | 3.1 Entendimiento funcional · 3.2 Specs · 3.3 Planificación · 3.4 Implementación y Demo | 14 hs | 12,5 hs (89,3%) |
| **Total** | **13 unidades** | **52 hs** | **36,25 hs (69,7%)** |

---

## Módulo 1 – Herramientas de IA y Harness Engineering (20 hs)

**Objetivo del módulo:** dominar el ecosistema actual de herramientas, entender cómo opera el bucle de un agente por dentro y configurar un *harness* de equipo (instrucciones, skills, hooks y servidores MCP en C#) sobre una solución .NET real.

---

### 1.1 Diseño y Prototipado para Ingeniería (4 hs)

Uso de IA generativa para pasar de una necesidad de negocio a prototipos navegables, extraer un *design system* legible por agentes y ejecutar el *handoff* hacia un frontend conectado a APIs .NET (o componentes Blazor).

**Objetivos de aprendizaje:**
- Describir flujos de interfaz complejos (estados vacíos, carga, error, validaciones y permisos) mediante *prompts* estructurados y referencias visuales.
- Documentar *design tokens* y reglas de componentes para que los agentes de código mantengan consistencia visual sin inventar estilos.
- Ejecutar el *handoff* de diseño a código: conectar una UI generada en React/Tailwind contra un contrato OpenAPI de ASP.NET Core o transformar el marcado en componentes **Blazor (`.razor`)**.

**Artefacto entregable:** Prototipo navegable de 3–4 pantallas + archivo de reglas de diseño (`design-tokens.json` / guía de componentes) listo para consumir desde el *harness*.

| Bloque | Duración | Contenido |
|---|---:|---|
| Panorama y prompting de UI | 0:45 | De texto, boceto o captura a pantalla funcional. Herramientas vigentes: **Google Stitch**, **v0 (Vercel)**, **Figma Make**, **Lovable** y **Claude Artifacts**. Cómo estructurar el prompt: rol de usuario, tarea, estados de pantalla, jerarquía visual y restricciones. |
| Design systems legibles por IA y handoff a .NET | 0:45 | Tokens (color, tipografía, espaciado) y reglas de componentes. Cómo pasar del código generado (React/Tailwind/HTML) a una arquitectura .NET: consumo de contratos OpenAPI en SPA o conversión asistida a componentes **Blazor**. |
| **[Workshop 1.1]** Prototipado y paquete de handoff | **2:30** | **Práctica guiada (150 min):** (1) Diseñar en duplas un flujo de 3–4 pantallas del dominio del curso en Stitch / v0 / Lovable; (2) iterar estados de borde y accesibilidad; (3) extraer tokens y generar el paquete de *handoff* (componentes base + contrato de datos esperado por la pantalla). Revisión cruzada y criterios de calidad. |

---

### 1.2 Herramientas de Desarrollo en el Flujo Diario .NET (4 hs)

Recorrido práctico por los asistentes y agentes integrados al IDE sobre una solución .NET multi-proyecto, con criterios empíricos para elegir herramientas y evitar retrabajo.

**Objetivos de aprendizaje:**
- Distinguir las capacidades y límites de autocompletado, edición multi-archivo y modo agente entre los tres IDEs estándar del curso: **VS Code (con GitHub Copilot)**, **Cursor** y **Windsurf** (cada participante puede usar su IDE habitual por su cuenta).
- Aplicar reglas de proyecto y anclaje de contexto (archivos de reglas del proyecto, referencias a archivos, documentación oficial) para resolver tareas diarias en C# sin degradar la arquitectura.
- Auditar código generado por IA para detectar alucinaciones de paquetes NuGet (*slopsquatting*), fugas de secretos, problemas de licencias y antipatrones en EF Core / `async-await`.

**Artefacto entregable:** Configuración base de instrucciones en el IDE + batería de tests xUnit y reporte de refactorización sobre el repositorio semilla .NET.

| Bloque | Duración | Contenido |
|---|---:|---|
| Mapa del ecosistema y la paradoja de productividad | 0:45 | Los tres IDEs estándar del curso: **VS Code + GitHub Copilot** vs. forks AI-first (**Cursor**, **Windsurf**), y su relación con los agentes de terminal (**Claude Code**, **Codex**). Qué cambia entre ellos en modo agente, edición multi-archivo y reglas de proyecto. Qué muestra la evidencia empírica (estudio METR y DORA): por qué usar IA sin método genera *"workslop"* y retrabajo. |
| Calidad, seguridad y matriz de decisión | 0:45 | Riesgos reales en .NET: dependencias NuGet inventadas, *queries* EF Core ineficientes (`N+1`), omisión de `CancellationToken`, secretos en `appsettings.json`. Matriz para elegir herramienta según tamaño de solución, privacidad y costo de tokens. |
| **[Workshop 1.2]** 5 flujos diarios sobre una solución .NET brownfield | **2:30** | **Práctica guiada (150 min) sobre el Repositorio Semilla (.NET + Azure):** (1) Arqueología y mapeo de código legado; (2) Refactorización segura de un servicio C# acoplado; (3) Generación de tests unitarios y de integración (**xUnit + WebApplicationFactory**); (4) Diagnóstico de un bug de concurrencia/EF Core a partir de logs y stack trace; (5) Code review asistido de un PR con fallas de seguridad inyectadas. |

---

### 1.3 Agentes, Patrones Agénticos y Skills Reutilizables (4 hs)

Cómo funciona un agente por dentro, cuándo usar un flujo determinista vs. un agente autónomo, cómo empaquetar conocimiento del equipo en **Skills (`SKILL.md`)** y cómo construir agentes propios en **.NET**.

**Objetivos de aprendizaje:**
- Explicar el bucle *percibir–razonar–actuar*, el uso de herramientas (*tool calling*), la gestión de ventana de contexto y las condiciones de parada.
- Elegir el patrón agéntico mínimo viable (*prompt chaining*, *routing*, *orquestador–subagentes*, *evaluador–optimizador*, ejecución paralela).
- Diseñar, escribir y probar una **Skill de equipo** siguiendo el estándar abierto `SKILL.md` (carga progresiva de instrucciones + scripts de verificación + plantillas).
- Construir un agente programático en C# con **`Microsoft.Extensions.AI`** y **Microsoft Agent Framework (`Microsoft.Agents.AI`)** conectado a **Azure AI Foundry**.

**Artefacto entregable (Parte 1 del entregable evaluable del Módulo 1):** Una **Skill de equipo (`SKILL.md` + script validador)** para estandarizar convenciones de ingeniería .NET (ej. creación de endpoints Minimal API con `ProblemDetails` RFC 9457 y validación, o auditoría de migraciones EF Core).

| Bloque | Duración | Contenido |
|---|---:|---|
| Anatomía del agente y patrones de orquestación | 0:45 | Chat vs. workflow determinista vs. agente autónomo. Bucle de ejecución, *tool calling*, compactación de contexto y memoria. Los 5 patrones agénticos esenciales y cuándo **no** usar un agente. |
| El estándar abierto Agent Skills (`SKILL.md`) y SDKs en .NET | 0:45 | Arquitectura de una Skill (`SKILL.md`, `scripts/`, `references/`), carga bajo demanda (*progressive disclosure*) y diferencia con el prompt de sistema y con MCP. Panorama de SDKs para agentes de producto: **`Microsoft.Extensions.AI` (`IChatClient`) + Microsoft Agent Framework (`Microsoft.Agents.AI` / Semantic Kernel en Azure AI Foundry)** comparado con Claude Agent SDK y OpenAI Agents SDK. |
| **[Workshop 1.3]** Creación de una Skill de equipo + mini-agente en C# | **2:30** | **Práctica guiada (150 min):** **Parte A (1:45):** Construir desde cero una Skill reutilizable para el equipo sobre el repo .NET (con frontmatter óptimo, reglas accionables y un script que verifique el resultado) y probar su activación automática. **Parte B (0:45):** Levantar un agente en C# con `Microsoft.Extensions.AI` y `Microsoft.Agents.AI` exponiendo funciones C# nativas (`AIFunctionFactory`). |

---

### 1.4 Harness Engineering: Claude Code, Codex y Devin (6 hs)

El modelo es solo una parte: el **harness** (contexto de repositorio, herramientas, permisos, sandbox, hooks y bucle de verificación automática) define qué tan bien trabaja el agente en un equipo real.

**Objetivos de aprendizaje:**
- Escribir archivos de contexto **`AGENTS.md` / `CLAUDE.md`** concisos, de alta señal y compatibles entre múltiples herramientas, evitando la degradación por exceso de contexto.
- Configurar y operar **Claude Code** a fondo: permisos, *Plan Mode*, subagentes, skills, **hooks (`PreToolUse` / `PostToolUse`)** atados al CLI de `.NET` (`dotnet build`, `dotnet format`, `dotnet test`) y ejecución *headless* en CI (GitHub Actions / Azure Pipelines).
- Operar **OpenAI Codex** (CLI local con sandbox y Codex en la nube con tareas en paralelo) y evaluar cuándo delegar tickets completos a **Devin** (usando *Knowledge*, *Playbooks* y *DeepWiki*).

**Artefacto entregable:** Configuración completa de *Harness* en el repositorio .NET (`AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` con hooks de compilación/formato en C#, y comandos personalizados).

| Bloque | Duración | Contenido |
|---|---:|---|
| Fundamentos de Harness & Context Engineering | 0:45 | Qué es el *harness*. Por qué los `AGENTS.md` autogenerados e inflados empeoran el rendimiento y suben el costo en tokens (+20%), y cómo redactar instrucciones humanas efectivas. Interoperabilidad real: el estándar `AGENTS.md` (Linux Foundation) y el puente `@AGENTS.md` para `CLAUDE.md`. |
| Profundización en Claude Code, Codex y Devin | 1:30 | **Claude Code:** modos, memoria, `/plan`, subagentes, hooks de ciclo de vida y modo *headless* (`claude -p`) en CI/CD. **Codex:** CLI en Rust + Codex Cloud, niveles de sandbox/aprobación y ejecución paralela. **Devin:** sesiones en la nube, *Knowledge*, *Playbooks* y *DeepWiki* (recorrido y demo de delegación punta a punta). Matriz comparativa: autonomía, control, privacidad y costos. |
| **[Workshop 1.4]** Ingeniería de Harness sobre una solución .NET | **3:45** | **Práctica guiada (225 min):** (1) Auditar y escribir el `AGENTS.md` + `CLAUDE.md` del repositorio semilla .NET (máximo 120 líneas, comandos exactos de filtro de `dotnet test`); (2) Configurar un hook `PostToolUse` que valide compilación y formato en cada edición de archivos `.cs`; (3) Crear un subagente revisor de arquitectura .NET; (4) Resolver el mismo ticket de backend en **Claude Code** y en **Codex CLI**, comparando planes, uso de contexto, tiempo y calidad del diff. |

---

### 1.5 Model Context Protocol (MCP) en .NET y Azure (2 hs)

El protocolo estándar para conectar agentes con sistemas externos, bases de datos, telemetría de Azure y herramientas internas de la consultora.

**Objetivos de aprendizaje:**
- Comprender la arquitectura cliente–servidor de MCP (*tools*, *resources*, *prompts*) y sus transportes (`stdio` local vs. *Streamable HTTP* remoto en ASP.NET Core).
- Configurar servidores MCP existentes (GitHub / Azure DevOps, **Azure MCP Server**, motor de base de datos) aplicando principios de mínimo privilegio y prevención de *prompt injection*.
- Desarrollar un **servidor MCP propio en C#** utilizando los paquetes oficiales **`ModelContextProtocol`** y **`ModelContextProtocol.AspNetCore`** en NuGet.

**Artefacto entregable (Parte 2 del entregable evaluable del Módulo 1):** Servidor MCP en C# (.NET) funcional conectado al agente del participante, exponiendo herramientas tipadas con `[McpServerTool]`.

| Bloque | Duración | Contenido |
|---|---:|---|
| Arquitectura MCP, servidores existentes y seguridad | 0:45 | Primitivas del protocolo: *Tools*, *Resources* y *Prompts*. Transportes `stdio` y HTTP. Configuración práctica del **Azure MCP Server (`microsoft/mcp`)**, GitHub/Azure DevOps MCP y DB MCP. Riesgos de seguridad: *prompt injection* indirecto, *tool poisoning*, manejo de secretos y alcance de permisos. |
| **[Workshop 1.5]** Construcción de un servidor MCP en C# (.NET) | **1:15** | **Práctica guiada (75 min):** Crear un servidor MCP en .NET desde cero con el SDK oficial `ModelContextProtocol` (NuGet `v2.3+`) e inyección de dependencias (`Microsoft.Extensions.Hosting`). Exponer 2 *tools* con `[McpServerTool]` (consulta de reglas/catálogo interno y validador de contratos/telemetría), registrarlo en Claude Code / VS Code / Codex y ejecutar un flujo completo donde el agente combine la **Skill de la Unidad 1.3 + el servidor MCP en C#**. |

---

## Módulo 2 – Metodologías Adaptadas a la IA: Spec-Driven Development (18 hs)

**Objetivo del módulo:** adoptar **Spec-Driven Development (SDD)** como disciplina de ingeniería de equipo, donde la especificación verificable es el artefacto principal, los tests y reglas arquitectónicas en .NET actúan como oráculo determinista, y el código se planifica, genera y valida sin perder el control del sistema.

---

### 2.1 Especificaciones Ejecutables por Agentes (Spec) (4 hs)

Cómo redactar especificaciones funcionales y técnicas sin ambigüedad que sirvan simultáneamente como contrato de negocio, guía de generación para el agente y base de las pruebas de aceptación.

**Objetivos de aprendizaje:**
- Explicar por qué la claridad del enunciado domina la tasa de éxito de los agentes (y cómo una spec ambigua derrumba la precisión del modelo en 20–40 puntos porcentuales).
- Redactar criterios de aceptación libres de ambigüedad combinando notación **EARS** (*Easy Approach to Requirements Syntax*: `WHEN... WHILE... THE SYSTEM SHALL...`) y escenarios **Given/When/Then**.
- Diseñar una **Especificación Técnica .NET** completa: contratos OpenAPI / `ProblemDetails`, modelo de datos EF Core, decisiones de arquitectura (ADRs), requisitos no funcionales y casos borde.

**Artefacto entregable:** Especificación Funcional + Especificación Técnica + ADR de una nueva funcionalidad sobre el repositorio .NET, auditada contra ambigüedades.

| Bloque | Duración | Contenido |
|---|---:|---|
| De requerimiento ambiguo a contrato ejecutable | 0:45 | Por qué el *prompt* conversacional no escala en equipos. Evidencia empírica sobre fallas de interpretación en agentes de horizonte largo. Niveles de especificación: Constitución del proyecto $\rightarrow$ Spec funcional $\rightarrow$ Spec técnica $\rightarrow$ Tareas. |
| Anatomía de una buena Spec Funcional y Técnica en .NET | 0:45 | Contexto, objetivos y *no-objetivos* explícitos. Notación **EARS** y escenarios **Given/When/Then**. Qué debe incluir la Spec Técnica en .NET/Azure: contratos de API (OpenAPI/TypeSpec), esquemas e índices EF Core, manejo de errores e idempotencia, ADRs y trazabilidad en Git. |
| **[Workshop 2.1]** Redacción y auditoría adversarial de una Spec | **2:30** | **Práctica guiada (150 min):** (1) A partir de un pedido de negocio deliberadamente incompleto, usar un agente con rol de *Analista Adversarial* para descubrir huecos, contradicciones y casos borde; (2) Redactar la Spec Funcional (EARS + GWT) y la Spec Técnica (.NET API + modelo de datos + ADR); (3) Ejecutar una revisión cruzada entre pares donde el agente de otro equipo intenta "malinterpretar" la spec antes de aprobarla por PR. |

---

### 2.2 Estimación, Análisis de Impacto y Planning con Agentes (4 hs)

Cómo cambian el análisis de impacto, la descomposición de trabajo y la estimación en una consultora cuando una parte sustancial de la implementación la ejecutan agentes.

**Objetivos de aprendizaje:**
- Utilizar agentes en modo exploración/lectura para generar un **Informe de Impacto y Riesgos** verificable sobre un repositorio .NET existente (archivos afectados, migraciones, cambios rompientes de contrato y deuda de tests).
- Descomponer una especificación en un **grafo (DAG) de tareas atómicas, independientes y verificables**, definiendo fronteras de archivos para evitar conflictos de *merge* entre agentes paralelos.
- Estimar proyectos separando las fases que la IA comprime (escritura de código repetitivo y tests base) de las que la IA **no** comprime o incluso expande si se gestiona mal (revisión de código, integración, validación de seguridad y pruebas de aceptación).

**Artefacto entregable (Parte 2 del entregable evaluable del Módulo 2, junto con 2.1):** Informe de Impacto + Plan de Tareas (`tasks.md`) con estimación comparada (tradicional vs. asistida por agentes) y matriz de asignación humano/agente.

| Bloque | Duración | Contenido |
|---|---:|---|
| Análisis de impacto asistido y descomposición en DAG | 0:45 | Cómo mapear código afectado, dependencias NuGet, contratos de API, tablas y cobertura de tests existente con agentes. Reglas para partir una Spec en tareas pequeñas con *Definition of Done* verificable por comando. La trampa de los agentes en paralelo (27,7% de conflictos de merge) y cómo prevenirla aislando módulos/vertical slices. |
| Estimación en la era de agentes y métricas de ingeniería | 0:45 | Qué se acelera y qué se vuelve el nuevo cuello de botella (el costo de revisar diffs grandes). Estimar por tipo de tarea, madurez del oráculo de tests y nivel de autonomía. Variables nuevas: presupuesto de tokens y tiempo de revisión. Métricas reales: *Lead Time*, *Change Failure Rate*, tasa de retrabajo y % de cambios que convergen contra la Spec. |
| **[Workshop 2.2]** Impacto, plan de tareas y estimación sobre el caso 2.1 | **2:30** | **Práctica guiada (150 min):** Tomar la Spec aprobada en la Unidad 2.1: (1) Ejecutar un análisis de impacto automatizado sobre la solución .NET y validar cada hallazgo contra el código real; (2) Generar el grafo de tareas (`tasks.md`) con dependencias, archivos tocados por tarea y comando de verificación; (3) Estimar cada tarea en modo tradicional vs. con agentes (HITL / Full AI) y defender el plan ante el instructor. |

---

### 2.3 Modos de Implementación: Full AI vs. Human-in-the-Loop (4 hs)

Criterios de ingeniería para decidir el grado de autonomía en cada tarea, cómo construir un **oráculo de verificación determinista en .NET** y cómo revisar eficientemente código generado por agentes.

**Objetivos de aprendizaje:**
- Seleccionar el modo de ejecución óptimo (**Human-in-the-Loop** vs. **Full AI autónomo**) en función del riesgo de dominio, la reversibilidad y la cobertura del oráculo de pruebas.
- Construir una **red de contención determinista en .NET** (tests de integración con `WebApplicationFactory` y **Testcontainers**, reglas de arquitectura con **`NetArchTest`** y analizadores de Roslyn) que impida que un agente dé por terminada una tarea inválida.
- Ejecutar trabajo agéntico en paralelo usando **`git worktrees`** y aplicar técnicas estructuradas de revisión de código generado.

**Artefacto entregable:** Funcionalidad implementada en ambos modos con suite de pruebas de integración/arquitectura pasando en verde y cuadro comparativo de métricas (tiempo de generación, tiempo de revisión, iteraciones y calidad).

| Bloque | Duración | Contenido |
|---|---:|---|
| Espectro de autonomía y el Oráculo de Verificación en .NET | 0:45 | Cuándo usar *Human-in-the-Loop* (aprobación de plan, revisión paso a paso, *pair programming*) y cuándo delegar en *Full AI* (entorno aislado en `git worktree` o contenedor, tests como oráculo, PR automático). Cómo blindar una solución .NET para agentes: **TDD agéntico**, **Testcontainers**, **`NetArchTest`** (arquitectura verificable por máquina) y `TreatWarningsAsErrors`. |
| Técnicas de revisión eficiente de código agéntico | 0:45 | Por qué revisar un PR de 1.500 líneas generado por IA falla. Revisión guiada por Spec + invariantes arquitectónicas + verificación de pruebas antes de leer la implementación línea por línea. |
| **[Workshop 2.3]** Laboratorio comparado: HITL vs. Full AI en .NET | **2:30** | **Práctica guiada (150 min):** Dividir el plan de la Unidad 2.2 en dos `git worktrees` sobre la solución .NET: (1) Escribir primero el test de arquitectura (`NetArchTest`) y el test de integración de contrato como oráculo; (2) Implementar la Tarea A en modo **Human-in-the-Loop** y la Tarea B en modo **Full AI autónomo**; (3) Medir tiempo total, costo de tokens, defectos escapados y esfuerzo de revisión en un *debrief* comparativo. |

---

### 2.4 Herramientas y Frameworks para SDD (6 hs)

Dominio práctico de las herramientas que estructuran el ciclo *Spec $\rightarrow$ Plan $\rightarrow$ Tareas $\rightarrow$ Implementación $\rightarrow$ Convergencia*, tanto para desarrollos desde cero (*greenfield*) como para evolución de sistemas existentes (*brownfield*).

**Objetivos de aprendizaje:**
- Clasificar los enfoques de SDD (*Spec-first*, *Spec-anchored* y *Spec-as-source*) y elegir la herramienta adecuada según el contexto del cliente y del proyecto.
- Operar **GitHub Spec Kit (`v1.2.5`)** de punta a punta sobre .NET (`/speckit-constitution` $\rightarrow$ `/speckit-specify` $\rightarrow$ `/speckit-plan` $\rightarrow$ `/speckit-tasks` $\rightarrow$ `/speckit-implement` $\rightarrow$ **`/speckit-converge`** y la extensión de bugs `/speckit-bug-*`).
- Operar **OpenSpec (`v1.15.0`)** para cambios iterativos sobre sistemas existentes (*brownfield*) mediante especificaciones delta (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`).
- Evaluar **AWS Kiro**, **BMAD Method** y **Tessl**, y ensamblar el flujo SDD definitivo que el equipo usará en el Módulo 3.

**Artefacto entregable:** Flujo SDD del equipo configurado y probado en el repositorio (plantillas, comandos/skills de SDD y *checklist* de convergencia) listo para iniciar el Módulo 3.

| Bloque | Duración | Contenido |
|---|---:|---|
| Taxonomía de SDD: Spec-first, Spec-anchored y Spec-as-source | 0:45 | El marco de referencia de la industria (Böckeler / Thoughtworks): por qué *Spec-anchored* es el punto de equilibrio para sistemas empresariales de larga vida. Cuándo elegir un flujo orientado a *greenfield* vs. uno orientado a deltas *brownfield*. |
| Panorama comparativo: Kiro, BMAD Method y Tessl | 1:30 | **AWS Kiro:** IDE orientado a specs (`.kiro/specs/`: `requirements.md` en EARS, `design.md`, `tasks.md`), *Agent Hooks* y *Steering* (demo en vivo). **BMAD Method (`v6.12`/`v7`):** orquestación por roles ágiles (Analyst, PM, Architect, SM, Dev, QA). **Tessl:** *Spec Registry* (tiles de librerías vía MCP para evitar alucinaciones de API) y exploración de *Spec-as-source*. Matriz de decisión para proyectos de consultoría. |
| **[Workshop 2.4]** Práctica intensiva con GitHub Spec Kit, OpenSpec y armado del flujo del equipo | **3:45** | **Práctica guiada (225 min):** **Parte A – GitHub Spec Kit (`v1.2.5`) sobre .NET (1:30):** inicializar `specify init`, definir la constitución .NET/Azure y ejecutar una funcionalidad completa hasta validar `/speckit-converge` (más prueba rápida de `/speckit-bug-assess`). **Parte B – OpenSpec (`v1.15.0`) en modo Brownfield (1:00):** usar `/opsx:explore` y `/opsx:propose` para introducir un cambio de requisito sobre un módulo existente, aplicar y archivar deltas en `openspec/specs/`. **Parte C – Flujo SDD propio del equipo (1:15):** configurar y dejar andando el pipeline SDD elegido por cada equipo para el proyecto del Módulo 3. |

---

## Módulo 3 – Ejecución de Proyecto de Desarrollo (14 hs)

**Objetivo del módulo:** aplicar de forma integrada todo el instrumental de los Módulos 1 y 2 en equipos de **3 a 5 personas** sobre un caso de negocio realista en **.NET y Azure**, partiendo de una solución base pre-configurada (*brownfield seed*) y cerrando con una demo funcional en vivo y métricas reales de ingeniería.

> **Diseño anti-fricción para las 14 horas:** los equipos no arrancan desde un `dotnet new` vacío. Reciben un **Repositorio Base Empresarial (.NET 9/10 + Azure)** con arquitectura limpia ya esqueleto, base de datos en contenedor (Testcontainers), pipeline de CI, OpenAPI y UI base funcionando, más un pliego de negocio con nuevos módulos por construir y defectos críticos por resolver. Así, el 100% del tiempo del Módulo 3 se invierte en **ingeniería asistida por agentes**.

---

### 3.1 Presentación del Caso y Entendimiento Funcional (2 hs)

**Objetivos de aprendizaje:**
- Extraer requerimientos ocultos, restricciones de negocio y casos borde entrevistando al "cliente" (el instructor) con asistencia de agentes.
- Auditar rápidamente una solución .NET existente para alinear el entendimiento funcional con el estado real del código.

**Artefacto entregable:** Documento de Entendimiento Funcional, Mapa de Alcance y Registro de Supuestos validado por el cliente (instructor).

| Bloque | Duración | Contenido |
|---|---:|---|
| Presentación del caso de negocio y arquitectura base | 0:30 | Contexto del cliente, usuarios, problema de negocio, objetivos del sprint integrador y recorrido rápido por el Repositorio Base (.NET + Azure). Armado de equipos (3–5 integrantes) y definición de roles (Product/Spec Lead, Architect/Harness Lead, Feature Developers, QA/Verification Lead). |
| **[Workshop 3.1]** Descubrimiento funcional y arqueología con IA | **1:30** | **Práctica en equipo (90 min):** (1) Usar agentes para cruzar el pliego del caso contra el repositorio base e identificar brechas; (2) Preparar y ejecutar dos rondas de entrevista estructurada al "cliente" (instructor) para destrabar ambigüedades; (3) Consolidar y validar el Documento de Entendimiento Funcional y el alcance comprometido del equipo. |

---

### 3.2 Especificaciones y Diseño del Proyecto (4 hs)

**Objetivos de aprendizaje:**
- Configurar la Constitución del proyecto (`AGENTS.md` / `CLAUDE.md`) y producir las Especificaciones Funcionales y Técnicas completas del proyecto en el flujo SDD elegido (Spec Kit u OpenSpec).
- Auditar la especificación de otro equipo combinando revisión humana y agentes adversariales para eliminar ambigüedades antes de escribir código.

**Artefacto entregable (Parte 1 del entregable evaluable del Módulo 3):** Constitución del repo + Prototipo de UI + Spec Funcional (EARS/GWT) + Spec Técnica (.NET API contracts, modelo de datos EF Core, ADRs) aprobadas tras revisión cruzada.

| Bloque | Duración | Contenido |
|---|---:|---|
| Guía de estructuración y criterios de evaluación de las Specs | 0:30 | Estándar de calidad esperado para la Constitución, las Specs Funcionales/Técnicas y el prototipo de UI. Reglas para la auditoría cruzada entre equipos. |
| **[Workshop 3.2]** Redacción de Specs, prototipo UI y revisión cruzada | **3:30** | **Práctica en equipo (210 min):** (1) Configurar `AGENTS.md`/`CLAUDE.md`, Skills y servidor MCP C# del equipo en el repo (0:45); (2) Generar las Specs Funcionales (EARS + criterios de aceptación) y el prototipo de pantallas con las herramientas de la Unidad 1.1 (1:00); (3) Redactar la Spec Técnica (.NET Minimal APIs, contratos OpenAPI, cambios en EF Core y tests de arquitectura esperados) (1:00); (4) **Revisión cruzada:** cada equipo audita la Spec de otro equipo buscando huecos/contradicciones, aplica ajustes y obtiene el *sign-off* del instructor (0:45). |

---

### 3.3 Planificación, Impacto y Estrategia de Ejecución (2 hs)

**Objetivos de aprendizaje:**
- Generar el análisis de impacto y riesgos técnicos sobre la solución .NET y transformar las Specs aprobadas en un plan de tareas paralelizable sin colisiones entre desarrolladores y agentes.

**Artefacto entregable (Parte 2 del entregable evaluable del Módulo 3):** Informe de Impacto y Riesgos + Grafo de Tareas (`tasks.md`) con estimación, asignación de responsables/agentes, estrategia de ramas/`git worktrees` y comandos de verificación.

| Bloque | Duración | Contenido |
|---|---:|---|
| Reglas de paralelización y oráculo de aceptación | 0:15 | Cómo organizar ramas, `git worktrees` y contratos de interfaz (interfaces C# / mocks / OpenAPI) para que 3–5 personas con agentes trabajen en paralelo durante las 6 horas de implementación sin bloquearse. |
| **[Workshop 3.3]** Análisis de impacto, descomposición en tareas y aprobación del plan | **1:45** | **Práctica en equipo (105 min):** (1) Ejecutar análisis de impacto y riesgos con el agente sobre el repo base (0:30); (2) Descomponer las Specs en tareas pequeñas y verificables (`tasks.md`), clasificando explícitamente cuáles se ejecutarán en modo **Full AI** y cuáles en **Human-in-the-Loop** (0:45); (3) Estimar tiempos, repartir el tablero para las 6 hs de implementación y validar el plan con el instructor (0:30). |

---

### 3.4 Implementación Agéntica, QA Cruzado y Demo Final (6 hs)

**Objetivos de aprendizaje:**
- Ejecutar dos sprints de desarrollo agéntico coordinado en equipo sobre .NET y Azure, utilizando tests de integración y de arquitectura como oráculo, verificando convergencia contra la Spec y midiendo resultados reales.

**Artefacto entregable (Entregables evaluables finales del curso):** Proyecto .NET funcionando en vivo con tests en verde y PRs integrados (35%) + Presentación de Demo y Retrospectiva con métricas de ingeniería (10%).

| Bloque | Duración | Contenido |
|---|---:|---|
| **[Workshop 3.4 – Parte 1]** Sprint 1: Oráculo de pruebas y cimientos verticales | **2:00** | **Ejecución en equipo (120 min):** Puesta en marcha de hooks, Skills y servidor MCP C#. Escritura agéntica de los tests de contrato/integración (xUnit + Testcontainers) y reglas `NetArchTest` primero. Implementación de las primeras tajadas verticales (backend .NET + persistencia) y apertura de los primeros PRs. |
| Checkpoint de convergencia y desbloqueo | 0:30 | Ejecución de `/speckit-converge` (o verificación contra Spec) por equipo. Detección temprana de desvíos arquitectónicos o cuellos de botella de integración. Ajustes explícitos a la Spec o al plan si emergieron nuevos datos. |
| **[Workshop 3.4 – Parte 2]** Sprint 2: Agentes en paralelo, UI y cierre de features | **2:00** | **Ejecución en equipo (120 min):** Implementación de las funcionalidades principales e integración del frontend con la API .NET usando agentes en paralelo (`git worktrees`), revisión cruzada de PRs asistida por IA y estabilización del pipeline de CI. |
| **[Workshop 3.4 – Parte 3]** Integración, QA de aceptación contra Spec y pulido | **0:45** | **Validación (45 min):** Pruebas de aceptación ejecutadas contra los escenarios Given/When/Then de la Spec de la Unidad 3.2. Corrección de defectos finales y preparación del entorno de demo. |
| Demo por equipo, métricas y retrospectiva | 0:45 | Demo funcional en vivo por equipo (producto andando + recorrido por su *harness* y sus *specs*). Presentación de métricas recolectadas (tiempo estimado vs. real, % de tareas Full AI vs. HITL, conflictos de merge, defectos detectados por el oráculo vs. en QA) y lecciones aprendidas para llevar a los proyectos de la consultora el lunes siguiente. |

---

## Evaluación y entregables

La evaluación es **100% práctica y acumulativa**: cada entregable parcial de los Módulos 1 y 2 construye activos de ingeniería que el equipo utiliza en el Módulo 3.

| Entregable | Momento | Peso | Qué se evalúa (Criterios de rúbrica) |
|---|---|---:|---|
| **1. Skill de equipo (`SKILL.md`) + Servidor MCP en C# (.NET)** | Fin del Módulo 1 (Unidades 1.3 y 1.5) | **15%** | Activación precisa de la Skill, claridad de instrucciones, script de validación funcional y servidor MCP en C# (`ModelContextProtocol`) operativo con herramientas tipadas y seguras. |
| **2. Especificación (EARS/GWT + Técnica .NET) y Plan de Tareas de una funcionalidad** | Fin del Módulo 2 (Unidades 2.1 y 2.2) | **15%** | Ausencia de ambigüedades, contratos de API/datos completos, descomposición en tareas atómicas verificables y estimación justificada. |
| **3. Constitución (`AGENTS.md`), Specs y Plan del Proyecto Integrador** | Módulo 3 (Unidades 3.2 y 3.3) | **25%** | Calidad de la ingeniería de contexto del repo, trazabilidad negocio $\rightarrow$ spec $\rightarrow$ tareas, prototipo UI consistente y estrategia de paralelización sin colisiones. |
| **4. Proyecto .NET funcionando, suite de pruebas oráculo y Demo** | Módulo 3 (Unidad 3.4) | **35%** | Cumplimiento de los criterios de aceptación de la Spec, tests de integración/arquitectura pasando en CI, calidad del código C# generado y fluidez de la demo. |
| **5. Retrospectiva de ingeniería basada en métricas** | Cierre del curso (Unidad 3.4) | **10%** | Rigor en el registro de métricas (estimado vs. real, uso de tokens/modos de autonomía, retrabajo evitado) y plan concreto de transferencia al trabajo diario en la consultora. |

---

## Requisitos previos del entorno de trabajo

Para aprovechar el 70% de carga práctica sin fricciones de instalación en el aula, cada participante debe contar con:
1. **Stack .NET & Contenedores:** **.NET 9 SDK (o .NET 10 SDK)**, **Docker Desktop** (o Rancher Desktop / Podman compatible con **Testcontainers**), **Git** y **Node.js 22+** / **Python 3.11+ con `uv`** (requeridos por los CLIs de Spec Kit y OpenSpec).
2. **IDE estándar del curso:** **VS Code (con GitHub Copilot)**, **Cursor** o **Windsurf**. Si alguien prefiere otro IDE puede usarlo, pero las guías y el soporte en el aula se basan en estos tres.
3. **Acceso a al menos un Harness de agentes:** **Claude Code**, **GitHub Copilot (con Agent Mode / CLI)** u **OpenAI Codex**. *(Las herramientas **Devin** y **AWS Kiro** se cubren mediante demostración guiada del instructor en caso de no contar con licencias individuales para todos los asistentes).*
4. **Cuenta de GitHub** con acceso al repositorio semilla del curso.
