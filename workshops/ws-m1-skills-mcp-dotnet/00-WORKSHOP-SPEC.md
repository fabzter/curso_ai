# Especificación del Workshop: Skills de Equipo (`SKILL.md`), Servidor MCP Oficial en C# y Agentes con `Microsoft.Extensions.AI`

- **ID del Workshop:** `ws-m1-skills-mcp-dotnet`
- **Unidades del Temario v2 cubiertas:** **Unidad 1.3** (*Agentes, Patrones Agénticos y Skills Reutilizables*) + **Unidad 1.5** (*Model Context Protocol (MCP) en .NET y Azure*)
- **Duración total:** **3 horas 45 minutos (225 min)** de práctica guiada intensiva *(puede dictarse en dos bloques: Parte 1 [2h 30m] durante la Unidad 1.3 y Parte 2 [1h 15m] durante la Unidad 1.5, o como taller integrador de cierre del Módulo 1)*.
- **Stack técnico:** **.NET 10 (C# 13, `Microsoft.Extensions.Hosting`, `System.TimeProvider`, xUnit)**, estándar abierto **Agent Skills (`SKILL.md` / `agentskills.io`)**, SDK oficial **`ModelContextProtocol` (`v2.3.0`)** y **`Microsoft.Extensions.AI` (`v10.11.0`)**.
- **Peso en la evaluación del curso:** **15% de la nota final** (Entregable Evaluable #1 del curso — cierre del Módulo 1).

---

## 1. Propósito y Contexto de Negocio

Cuando un equipo de ingeniería `.NET` adopta agentes de codificación (Claude Code, GitHub Copilot Agent Mode, Cursor o Codex) sin estandarizar su conocimiento interno ni sus conexiones a datos operativos, aparecen dos fallas sistemáticas:
1. **Deriva de convenciones arquitectónicas (*Convention Drift*):** cada desarrollador obtiene código distinto; el agente inventa respuestas JSON ad-hoc en vez de respetar **RFC 9457 (`ProblemDetails`)**, usa `DateTime.UtcNow` directo en vez de `System.TimeProvider`, u omite códigos de error canónicos del equipo.
2. **Ceguera operativa y alucinación de reglas (*Context Blindness*):** el agente no conoce las matrices contractuales de SLA por tier de cliente (`Bancario-Tier1`, `Aseguradora-Gold`, `Retail-Standard`) ni el estado real de los incidentes activos, o queda expuesto a ataques de **Prompt Injection Indirecto** cuando lee notas de tickets cargadas por terceros.

En este workshop vas a construir los tres pilares que resuelven ese problema sobre el dominio **`GuardiaCloud.Sla`**:
1. **Una Skill de equipo reutilizable (`.agents/skills/dotnet-minimal-api-guardian/SKILL.md`)** con carga progresiva de contexto (`references/rfc9457-catalogo-errores.md`) y un script de verificación determinista (`scripts/verify-minimal-api.sh`).
2. **Un Servidor MCP oficial en C# (`GuardiaCloud.Sla.McpServer`)** con el paquete NuGet `ModelContextProtocol` (`v2.3.0`), exponiendo 3 herramientas tipadas con `[McpServerTool]`, anotaciones de seguridad (`ReadOnly`, `Idempotent`, `Destructive`, `OpenWorld`) y sanitización contra *prompt injection* indirecto.
3. **Un Agente de Triage programático en .NET (`SlaTriageAgent`)** construido con `Microsoft.Extensions.AI` (`v10.11.0`, `IChatClient` + `FunctionInvokingChatClient` + `AIFunctionFactory.Create`) que encadena llamadas a las herramientas MCP con condiciones de parada deterministas (`MaximumIterationsPerRequest = 4`).

---

## 2. Objetivos de Aprendizaje Medibles

Al finalizar el workshop, cada participante/dupla será capaz de:
1. **Diseñar y validar una Agent Skill (`SKILL.md`):** Redactar el frontmatter YAML (`name`, `description` con disparadores y anti-disparadores), estructurar la carga progresiva hacia `references/` y automatizar su validación con `scripts/verify-minimal-api.sh`.
2. **Desarrollar un Servidor MCP en C# (.NET 10):** Configurar `Host.CreateApplicationBuilder` con transporte `stdio` sin contaminar `stdout`, exponer herramientas con `[McpServerToolType]` y `[McpServerTool]`, y declarar metadatos de seguridad (`ReadOnlyHint`, `DestructiveHint`, `OpenWorldHint`).
3. **Mitigar riesgos de seguridad en MCP:** Aplicar validación por lista blanca (*allow-list*) en parámetros de entrada y neutralizar intentos de *prompt injection* indirecto embebidos en descripciones de incidentes (`SYSTEM OVERRIDE...`).
4. **Orquestar un bucle agéntico en C# con `Microsoft.Extensions.AI`:** Construir un pipeline `IChatClient` con `.AsBuilder().UseFunctionInvocation(...)`, registrar funciones C# con `AIFunctionFactory.Create(...)` y verificar el bucle *percibir–razonar–actuar* mediante tests deterministas en xUnit.

---

## 3. Agenda y Cronograma (225 minutos)

| Fase | Tiempo | Minutos | Actividad práctica | Artefacto producido |
|---|---:|---:|---|---|
| **Fase 0** | 0:00 – 0:15 | 15 min | Apertura de `starter/`, compilación inicial, ejecución de los 2 tests base y diagnóstico de por qué falla `verify-minimal-api.sh`. | Entorno `.NET 10` verificado (`dotnet test` base en verde en <1 s). |
| **Fase 1** | 0:15 – 1:15 | 60 min | **Ingeniería de Agent Skills (Unidad 1.3A):** Diseño del frontmatter YAML, reglas de *progressive disclosure* hacia `references/rfc9457-catalogo-errores.md` y validación con `verify-minimal-api.sh`. | `.agents/skills/dotnet-minimal-api-guardian/SKILL.md` aprobando el verificador determinista. |
| **Fase 2** | 1:15 – 2:30 | 75 min | **Servidor MCP en C# y Seguridad (Unidad 1.5):** Implementación de `inspect_incident_sla_status` y `validate_rfc9457_contract` en `SlaMcpTools.cs`, sanitización anti-inyección y registro `.mcp.json`. | Servidor MCP C# compilando + 5 tests de herramientas y seguridad MCP en verde. |
| **Fase 3** | 2:30 – 3:20 | 50 min | **Agente en C# con `Microsoft.Extensions.AI` (Unidad 1.3B):** Construcción de `SlaTriageAgent.cs` con `ChatClientBuilder`, `UseFunctionInvocation` (`MaximumIterationsPerRequest = 4`) y `AIFunctionFactory`. | `SlaTriageAgent.cs` + 6to test de bucle multi-tool en verde. |
| **Fase 4** | 3:20 – 3:45 | 25 min | **Prueba Integrada en Vivo y Cierre:** Conexión del servidor MCP en el *harness* (Claude Code / VS Code Copilot / Codex) combinando la Skill + las 3 tools MCP. | Demostración cruzada entre duplas y entrega calificada con rúbrica de 100 pts. |

---

## 4. Requisitos Previos Verificables

Antes de iniciar el taller, ejecutá en tu terminal:
```bash
dotnet --version          # .NET SDK 10.0.x (o 9.0.x ajustando TargetFramework)
bash --version            # Para correr el verificador determinista de la Skill
```
> **Diseño 100% resiliente para el aula (Offline-First + Live-Ready):** Todos los ejercicios y los 6 tests automatizados de `GuardiaCloud.Sla.McpTests` usan `DeterministicTriageChatClient` (`IChatClient`) e inyección de `FixedTimeProvider`, por lo que **no requieren conexión a internet ni llaves pagas de Azure OpenAI/Anthropic** para compilar y verificar el bucle de *tool calling* en clase. En la Fase 4 podés conectarlo en vivo a tu IDE/CLI mediante `.mcp.json`.

---

## 5. Estructura del Paquete del Workshop

```text
workshops/ws-m1-skills-mcp-dotnet/
├── 00-WORKSHOP-SPEC.md                 # Este documento (especificación, objetivos y cronograma)
├── 01-GUIA-PASO-A-PASO.md              # Guía práctica para el participante (en español rioplatense)
├── 02-GUIA-FACILITADOR-Y-RUBRICA.md    # Guía docente, notas de seguridad MCP y rúbrica (100 pts)
├── starter/                            # Solución .NET 10 inicial ("Antes" del workshop, 2 tests verdes)
│   ├── AGENTS.md / CLAUDE.md
│   ├── .mcp.json.example
│   ├── GuardiaCloud.Sla.McpWorkshop.sln
│   ├── .agents/skills/dotnet-minimal-api-guardian/
│   │   ├── SKILL.md                    # Esqueleto con TODOs para completar en Fase 1
│   │   ├── references/rfc9457-catalogo-errores.md
│   │   └── scripts/verify-minimal-api.sh
│   ├── src/GuardiaCloud.Sla.McpServer/
│   └── tests/GuardiaCloud.Sla.McpTests/
└── solution/                           # Solución .NET 10 de referencia ("Después" del workshop, 6 tests verdes)
    ├── AGENTS.md / CLAUDE.md
    ├── .mcp.json
    ├── GuardiaCloud.Sla.McpWorkshop.sln
    ├── .agents/skills/dotnet-minimal-api-guardian/
    │   ├── SKILL.md                    # Skill completa validada por verify-minimal-api.sh
    │   ├── references/rfc9457-catalogo-errores.md
    │   └── scripts/verify-minimal-api.sh
    ├── src/GuardiaCloud.Sla.McpServer/
    └── tests/GuardiaCloud.Sla.McpTests/
```
