# Especificación del Workshop: Harness Engineering, Oráculos de Arquitectura con `NetArchTest` y Laboratorio HITL vs. Full AI (`git worktrees`)

- **ID del Workshop:** `ws-m2-harness-oracle-dotnet`
- **Unidades del Temario v2 cubiertas:** **Unidad 1.4** (*Harness Engineering: Claude Code, Codex y Devin*) + **Unidad 2.3** (*Modos de Implementación: Full AI vs. Human-in-the-Loop*)
- **Duración total:** **3 horas 45 minutos (225 min)** de práctica guiada intensiva *(puede dictarse dividida en Parte 1 [1h 45m] en la Unidad 1.4 y Parte 2 [2h 00m] en la Unidad 2.3, o como taller continuo)*.
- **Stack técnico:** **.NET 10 (C# 13, ASP.NET Core Minimal APIs, `System.TimeProvider`, `ProblemDetails` RFC 9457)**, **`NetArchTest.Rules` (`v1.3.2`)**, **xUnit + `WebApplicationFactory<Program>`**, **Claude Code / OpenAI Codex CLI** y **`git worktrees`**.
- **Peso en la evaluación del curso:** Parte de las **Prácticas Guiadas por Unidad (15% de la nota final)** y base técnica obligatoria para el **Proyecto Integrador del Módulo 3 (40%)**.

---

## 1. Propósito y Contexto de Negocio

La diferencia entre un agente que genera *"workslop"* (código que compila a medias pero rompe la arquitectura y exige dos horas de retrabajo humano) y un agente que entrega un PR listo para producción no está en "escribir un prompt más ingenioso", sino en dos piezas de ingeniería de software:
1. **El Harness del Repositorio (Unidad 1.4):** Un archivo `AGENTS.md` curado por humanos (<100 líneas, alta señal) con el puente `@AGENTS.md` en `CLAUDE.md`, un hook automático `PostToolUse` (`scripts/post-edit-dotnet-hook.sh`) que compila y corre pruebas tras cada edición de código C#, y un subagente revisor (`dotnet-arch-reviewer`).
2. **El Oráculo de Verificación Determinista (Unidad 2.3):** Una red de contención automática compuesta por reglas de arquitectura ejecutables con **`NetArchTest.Rules` (`v1.3.2`)**, `TreatWarningsAsErrors=true` y pruebas de integración HTTP con `WebApplicationFactory<Program>` y reloj determinista (`TimeProvider`).

Solo cuando el **Harness + Oráculo** están activos, el equipo puede decidir con criterio ingenieril qué tareas ejecutar en modo **Human-in-the-Loop (HITL)** y cuáles delegar en paralelo en modo **Full AI autónomo** usando **`git worktrees`**.

---

## 2. Objetivos de Aprendizaje Medibles

Al finalizar el workshop, cada participante/dupla será capaz de:
1. **Curar un `AGENTS.md` + `CLAUDE.md` interoperable:** Reemplazar un archivo de contexto autogenerado e inflado por un `AGENTS.md` de alta señal (<100 líneas) con comandos exactos de filtrado xUnit (`dotnet test --filter`) y el puente `@AGENTS.md`.
2. **Configurar Hooks de Ciclo de Vida y Subagentes:** Conectar `scripts/post-edit-dotnet-hook.sh` en `.claude/settings.json` (`PostToolUse` sobre `Edit|Write|MultiEdit`) y definir el subagente `.claude/agents/dotnet-arch-reviewer.md`.
3. **Programar un Oráculo de Arquitectura en C# con `NetArchTest.Rules`:** Escribir pruebas automáticas en `ArchitectureOracleTests.cs` que detecten y bloqueen violaciones de arquitectura limpia (como la clase intrusa `LegacyVibeCodedHelper.cs` que acopla `Domain` con `Infrastructure` y omite `sealed`).
4. **Ejecutar y medir el laboratorio comparado HITL vs. Full AI en `git worktrees`:**
   - Implementar la **Tarea A** (*Motor de Créditos Financieros por Incumplimiento Mensual*, `POST /api/sla/credits/calculate`) en modo **Human-in-the-Loop**.
   - Implementar en paralelo la **Tarea B** (*Exportador de Resumen Operativo de Guardia*, `GET /api/sla/incidents/export-summary`) en modo **Full AI autónomo** dentro de un `git worktree` aislado, e integrar ambas ramas registrando tiempos, iteraciones y defectos contenidos por el oráculo.

---

## 3. Agenda y Cronograma (225 minutos)

| Fase | Tiempo | Minutos | Actividad práctica | Artefacto producido |
|---|---:|---:|---|---|
| **Fase 0** | 0:00 – 0:15 | 15 min | Apertura de `starter/`, corrida de los 2 tests base y ejecución de `./scripts/post-edit-dotnet-hook.sh` para observar el fallo del Harness inicial. | Diagnóstico de los 3 defectos de Harness y Arquitectura en `starter/`. |
| **Fase 1** | 0:15 – 1:05 | 50 min | **Harness Engineering (Unidad 1.4):** Reescritura de `AGENTS.md` (<100 líneas), creación de `CLAUDE.md` (`@AGENTS.md`), activación de `.claude/settings.json` y del subagente `dotnet-arch-reviewer.md`. | Harness interoperable activo y validado por el paso 1 del hook. |
| **Fase 2** | 1:05 – 1:55 | 50 min | **Oráculo de Arquitectura con `NetArchTest` (Unidad 2.3A):** Escritura de las reglas `Domain_Should_Not_Depend_On_Infrastructure_Or_AspNetCoreHttp` y `Domain_Classes_Should_Be_Sealed`, detección de `LegacyVibeCodedHelper.cs` y remediación. | `ArchitectureOracleTests.cs` (3 tests verdes) + eliminación de deuda arquitectónica. |
| **Fase 3** | 1:55 – 3:15 | 80 min | **Laboratorio HITL vs. Full AI en `git worktrees` (Unidad 2.3B):** Creación del `git worktree`, implementación de **Tarea A (HITL)** en rama principal y **Tarea B (Full AI)** en el worktree paralelo con tests `WebApplicationFactory`. | Endpoints `/credits/calculate` y `/export-summary` + 7 tests en verde tras `git merge`. |
| **Fase 4** | 3:15 – 3:45 | 30 min | **Auditoría con Subagente y Debrief Comparativo:** Ejecución de `dotnet-arch-reviewer` y completado de `comparativa-hitl-vs-full-ai.md`. | Scorecard empírico HITL vs. Full AI y cierre del taller. |

---

## 4. Requisitos Previos Verificables

```bash
dotnet --version          # .NET SDK 10.0.x
git --version             # Soporte para git worktree
bash --version            # Para ejecutar scripts/post-edit-dotnet-hook.sh
```

---

## 5. Estructura del Paquete del Workshop

```text
workshops/ws-m2-harness-oracle-dotnet/
├── 00-WORKSHOP-SPEC.md                 # Este documento (especificación, objetivos y cronograma)
├── 01-GUIA-PASO-A-PASO.md              # Guía práctica paso a paso para el participante (en voseo rioplatense)
├── 02-GUIA-FACILITADOR-Y-RUBRICA.md    # Guía docente, respuestas del debrief y rúbrica (100 pts)
├── starter/                            # Solución .NET 10 inicial ("Antes" del workshop, 2 tests base)
│   ├── AGENTS.md                       # Borrador inflado autogenerado (antipatrón a corregir en Fase 1)
│   ├── .claude/settings.json.example   # Configuración del hook PostToolUse
│   ├── .claude/agents/dotnet-arch-reviewer.md
│   ├── scripts/post-edit-dotnet-hook.sh
│   ├── GuardiaCloud.Sla.HarnessLab.sln
│   ├── src/GuardiaCloud.Sla.Api/       # Incluye LegacyVibeCodedHelper.cs (violación de arquitectura intencional)
│   └── tests/GuardiaCloud.Sla.Tests/
└── solution/                           # Solución .NET 10 de referencia ("Después" del workshop, 7 tests verdes)
    ├── AGENTS.md / CLAUDE.md           # Contexto curado (<60 líneas) + puente @AGENTS.md
    ├── .claude/settings.json
    ├── .claude/agents/dotnet-arch-reviewer.md
    ├── scripts/post-edit-dotnet-hook.sh
    ├── comparativa-hitl-vs-full-ai.md  # Scorecard empírico de referencia
    ├── GuardiaCloud.Sla.HarnessLab.sln
    ├── src/GuardiaCloud.Sla.Api/       # Limpio de violaciones + Tarea A (HITL) y Tarea B (Full AI) completas
    └── tests/GuardiaCloud.Sla.Tests/   # 3 tests NetArchTest + 4 tests WebApplicationFactory en verde
```
