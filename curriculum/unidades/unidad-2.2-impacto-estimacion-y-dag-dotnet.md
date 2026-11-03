# Guía Paso a Paso del Alumno — Unidad 2.2: Estimación, Análisis de Impacto Brownfield y Planificación en Grafos (DAG)

> **Módulo 2 · Unidad 2.2 (4 hs: 1h 30m encuadre + 2h 30m Workshop Práctico)**  
> **Entrada:** `specs/001-sla-pause-windows/spec.md` y `plan.md` (creados en la Unidad 2.1)  
> **Salida:** Informe de Impacto Brownfield + `specs/001-sla-pause-windows/tasks.md` (Grafo DAG sin colisiones)

---

## 1. Objetivo del Taller
Transformar la especificación técnica de las ventanas de pausa de SLA en un **plan de ejecución en grafo (`tasks.md`)** donde múltiples desarrolladores y agentes puedan trabajar en paralelo sin sufrir el **27.67% de conflictos de merge** documentado en equipos multi-agente (*AgenticFlict*).

---

## 2. Paso 1 (40 min): Análisis de Impacto Automatizado en Modo Solo Lectura

Ejecutá tu agente (en modo `/plan` o *read-only*) sobre `GuardiaCloud.Sla.sln` con el siguiente prompt:

```text
Analizá la solución GuardiaCloud.Sla.sln en modo solo lectura tomando como entrada specs/001-sla-pause-windows/spec.md y plan.md.
No modifiques ningún archivo. Generá un Informe de Impacto Técnico con:
1. Lista exacta de archivos .cs existentes que deberán modificarse y por qué.
2. Nuevos archivos/tipos C# a crear en Domain y Api.
3. Riesgos de regresión sobre el cálculo actual de SlaCalculator.Evaluate.
4. Qué contratos pueden congelarse primero para habilitar trabajo paralelo.
```

---

## 3. Paso 2 (50 min): Construcción del Grafo Acíclico Dirigido (`tasks.md`)

Redactá `specs/001-sla-pause-windows/tasks.md` respetando tres reglas de ingeniería:
1. **Fase 1 Secuencial (Contratos + Oráculo en Rojo):** Primero se crean los records/DTOs e interfaces en `Domain` y se escriben los tests de integración que fallan.
2. **Fase 2 Paralela (`[P]`):** Dos tareas solo pueden marcarse como `[P]` si **no tocan ningún archivo `.cs` en común**.
3. **Verificación explícita por tarea:** Cada tarea incluye el comando `dotnet test --filter ...` que demuestra que está terminada.

```markdown
# Tasks DAG — 001-sla-pause-windows

## Fase 1: Contratos y Oráculo de Pruebas (Secuencial — Bloqueante)
- [ ] **T001** [HITL] Definir `PauseReason`, `SlaPauseWindow` y firmas en `GuardiaCloud.Sla.Domain`
  - **Archivos:** `src/GuardiaCloud.Sla.Domain/SlaPauseWindow.cs`, `src/GuardiaCloud.Sla.Domain/Incident.cs`
  - **Verificación:** `dotnet build --no-restore`
- [ ] **T002** [HITL] Escribir suites de integración xUnit en rojo para fusión de pausas y errores RFC 9457
  - **Archivos:** `tests/GuardiaCloud.Sla.Tests/SlaPauseWindowsTests.cs`
  - **Verificación:** `dotnet test --filter SlaPauseWindowsTests` (compila y falla de forma esperada)

## Fase 2: Implementación en Ramas / Worktrees Paralelos `[P]`
- [ ] **T003 [P]** [Full AI] Implementar algoritmo puro de recorte y unión de intervalos solapados
  - **Depende de:** T001, T002
  - **Archivos exclusivos:** `src/GuardiaCloud.Sla.Domain/SlaCalculator.cs`
  - **Verificación:** `dotnet test --filter OverlappingPauseWindows`
- [ ] **T004 [P]** [HITL] Implementar endpoint `POST /api/incidents/{id}/pauses` y validaciones RFC 9457
  - **Depende de:** T001, T002
  - **Archivos exclusivos:** `src/GuardiaCloud.Sla.Api/Program.cs`
  - **Verificación:** `dotnet test --filter InvalidPauseWindow`
```

---

## 4. Paso 3 (35 min): Estimación de Esfuerzo en Dos Columnas

Completá para cada tarea de `tasks.md` la tabla comparativa de estimación:

| Tarea | Modo (`HITL` / `Full AI`) | Estimación Tradicional (sin IA) | Tiempo de Generación con IA | Tiempo de Verificación y Review Humano | Total con IA |
|---|---|---:|---:|---:|---:|
| **T001** Contratos Domain | HITL | 30 min | 5 min | 10 min | **15 min** |
| **T002** Tests Oráculo xUnit | HITL | 60 min | 10 min | 20 min | **30 min** |
| **T003** Unión de intervalos | Full AI | 75 min | 5 min | 15 min | **20 min** |
| **T004** Endpoint Minimal API | HITL | 45 min | 10 min | 15 min | **25 min** |

---

## 5. Paso 4 (25 min): Auditoría Cruzada del Grafo
Intercambiá tu `tasks.md` con otra dupla y verificá:
- [ ] Ningún archivo `.cs` aparece en dos tareas paralelas `[P]` de la misma fase.
- [ ] Toda tarea tiene un comando `dotnet build` o `dotnet test` determinista.
