# Mapa Maestro de Proyectos Base y Workshops (.NET 10)
## Curso: Desarrollo de Software con IA (52 Horas · 3 Módulos · 13 Unidades)

Este directorio contiene **todos los proyectos base (`.NET 10` / C# 13), ejercicios guiados (`starter/`), soluciones verificadas (`solution/`), prototipos UI y rúbricas docentes** que respaldan cada slide y cada bloque práctico de los 7 días del curso.

---

## 1. Tabla de Correspondencia: Día / Unidad / Slide → Carpeta de Código

| Día | Unidades | Deck de Clase (`presentaciones/`) | Carpeta de Código en `workshops/` | Solución `.NET 10` (`.sln`) | Verificación (`dotnet test`) |
|---|---|---|---|---|---|
| **Día 1** (8 hs) | **U1.1** (Diseño UI + Handoff .NET) y **U1.2** (VS Code, Cursor, Windsurf + 5 Flujos Diarios) | `Unidad-1.1-*.pptx` y `Unidad-1.2-*.pptx` (Slides 1–13 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-dia1-proyecto-base-dotnet/`](ws-m1-dia1-proyecto-base-dotnet/) | `GuardiaCloud.Sla.sln` | `starter/`: **2/2 passed**<br>`solution/`: **10/10 passed** |
| **Día 2** (Mañana · 4 hs) | **U1.3** (Agentes, Patrones, `SKILL.md` y `Microsoft.Extensions.AI`) | `Unidad-1.3-*.pptx` (Slides 13–16 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-skills-mcp-dotnet/`](ws-m1-skills-mcp-dotnet/) (Fases 1 y 3) | `GuardiaCloud.Sla.McpWorkshop.sln` | `solution/`: **6/6 passed** + `verify-minimal-api.sh` OK |
| **Día 2** (Tarde · 6 hs) | **U1.4** (Harness Engineering: Claude Code, Codex, Devin, `AGENTS.md` y Hooks) | `Unidad-1.4-*.pptx` (Slides 17–20 de `00-Modulo-1-Completo.pptx`) | [`ws-m2-harness-oracle-dotnet/`](ws-m2-harness-oracle-dotnet/) (Fases 1, 2 y Subagente) | `GuardiaCloud.Sla.HarnessLab.sln` | `solution/`: **7/7 passed** + `post-edit-dotnet-hook.sh` OK |
| **Día 3** (Bloque 1 · 2 hs) | **U1.5** (Model Context Protocol en C# `v2.3.0` + Seguridad Anti-Inyección · **Entrega #1 = 15%**) | `Unidad-1.5-*.pptx` (Slides 21–23 de `00-Modulo-1-Completo.pptx`) | [`ws-m1-skills-mcp-dotnet/`](ws-m1-skills-mcp-dotnet/) (Fase 2: `SlaMcpTools.cs`) | `GuardiaCloud.Sla.McpWorkshop.sln` | `solution/`: **6/6 passed** |
| **Día 3** (Bloque 2 · 4 hs) y **Día 4** (Bloque 1 · 4 hs) | **U2.1** (Specs EARS + Given/When/Then + *Spec Critic*) y **U2.2** (Impacto Brownfield, Estimación y DAG `tasks.md`) | `Unidad-2.1-*.pptx` y `Unidad-2.2-*.pptx` (Slides 1–5 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-sdd-dotnet/`](ws-m2-sdd-dotnet/) (`specs/001-sla-pause-windows/`) | `GuardiaCloud.Sla.sln` | `starter/`: **2/2 passed**<br>`solution/`: **6/6 passed** |
| **Día 4** (Bloque 2 · 4 hs) | **U2.3** (Full AI vs. HITL en `git worktree` + Oráculo `NetArchTest.Rules` v1.3.2) | `Unidad-2.3-*.pptx` (Slides 6–7 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-harness-oracle-dotnet/`](ws-m2-harness-oracle-dotnet/) (Fases 3 y 4) | `GuardiaCloud.Sla.HarnessLab.sln` | `solution/`: **7/7 passed** |
| **Día 5** (6 hs) | **U2.4** (GitHub Spec Kit `v1.2.5` + OpenSpec `v1.15.0` Deltas Brownfield · **Entrega #2 = 15%**) | `Unidad-2.4-*.pptx` (Slides 8–9 de `00-Modulo-2-Completo.pptx`) | [`ws-m2-sdd-dotnet/`](ws-m2-sdd-dotnet/) (`.specify/` + `openspec/`) | `GuardiaCloud.Sla.sln` | `solution/`: **6/6 passed** |
| **Días 6 y 7** (14 hs) | **U3.1 a U3.4** (Proyecto Integrador Capstone en Equipos · **Entregas #3, #4 y #5 = 70%**) | `Unidades-3.1-a-3.4-*.pptx` (`00-Modulo-3-Completo.pptx`) | [`ws-m3-capstone-dotnet/`](ws-m3-capstone-dotnet/) | `GuardiaCloud.CommandCenter.sln` | `starter/`: **1/1 passed**<br>`solution/`: **8/8 passed** |

---

## 2. Cómo Ejecutar Todos los Proyectos y Tests de un Vistazo

Desde la raíz del repositorio (o tras descomprimir el `.zip`):

```bash
# Día 1 (Unidades 1.1 y 1.2) — Proyecto Base GuardiaCloud.Sla
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/starter/GuardiaCloud.Sla.sln
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/solution/GuardiaCloud.Sla.sln

# Unidades 1.3 y 1.5 — Agent Skills (SKILL.md), Agente Microsoft.Extensions.AI y Servidor MCP en C#
./workshops/ws-m1-skills-mcp-dotnet/solution/.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh
dotnet test workshops/ws-m1-skills-mcp-dotnet/solution/GuardiaCloud.Sla.McpWorkshop.sln

# Unidades 1.4 y 2.3 — Harness Engineering, Hooks .NET y Oráculo NetArchTest.Rules
dotnet test workshops/ws-m2-harness-oracle-dotnet/solution/GuardiaCloud.Sla.HarnessLab.sln

# Unidades 2.1, 2.2 y 2.4 — Spec-Driven Development (GitHub Spec Kit + OpenSpec)
dotnet test workshops/ws-m2-sdd-dotnet/solution/GuardiaCloud.Sla.sln

# Módulo 3 (Unidades 3.1 a 3.4) — Proyecto Integrador Capstone (GuardiaCloud.CommandCenter)
dotnet test workshops/ws-m3-capstone-dotnet/solution/GuardiaCloud.CommandCenter.sln
```
