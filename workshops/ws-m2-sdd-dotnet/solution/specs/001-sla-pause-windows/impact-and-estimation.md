# Informe de Impacto Brownfield y Estimación Comparada (Unidad 2.2)
## Feature: `001-sla-pause-windows` sobre `GuardiaCloud.Sla.sln`

### 1. Matriz de Archivos Afectados (Auditoría en Modo Solo Lectura)
| Archivo | Tipo de Cambio | Riesgo de Colisión | Estrategia en el Grafo DAG (`tasks.md`) |
|---|---|---|---|
| `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs` | Modificación (agregar `PauseReason`, `SlaPauseWindow` y lista en `Incident`) | Alto (archivo compartido) | Congelar en **Fase 1 Secuencial (`T001`)** antes de abrir ramas paralelas |
| `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs` | Extensión (suites xUnit en rojo para fusión de pausas y RFC 9457) | Medio | Escribir en **Fase 1 Secuencial (`T002`)** como oráculo determinista |
| `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs` | Modificación (algoritmo puro de recorte y unión de intervalos solapados) | Bajo si se aísla | Ejecutar en **Fase 2 Paralela (`T003 [P]`)** en `git worktree` |
| `src/GuardiaCloud.Sla.Api/Program.cs` | Modificación (endpoint `POST /api/incidents/{id}/pauses` + validaciones RFC 9457) | Bajo si no toca `Services` | Ejecutar en **Fase 2 Paralela (`T004 [P]`)** en rama separada |

---

### 2. Estimación en Dos Columnas (Generación con IA vs. Verificación Humana)

| Tarea del DAG | Modo (`HITL` / `Full AI`) | Estimación Tradicional (sin IA) | Tiempo de Generación con IA | Tiempo de Verificación y Code Review | Total con IA | Ahorro Neto |
|---|---|---:|---:|---:|---:|---:|
| **T001** Contratos Domain y DTOs | HITL | 30 min | 5 min | 10 min | **15 min** | 50% |
| **T002** Suite Oráculo xUnit en rojo | HITL | 60 min | 10 min | 20 min | **30 min** | 50% |
| **T003 [P]** Unión matemática de intervalos | Full AI (`worktree`) | 75 min | 5 min | 15 min | **20 min** | 73% |
| **T004 [P]** Endpoint Minimal API + RFC 9457 | HITL | 45 min | 10 min | 15 min | **25 min** | 44% |
| **Total Feature `001-sla-pause-windows`** | Mixto | **210 min (3.5 hs)** | **30 min** | **60 min** | **90 min (1.5 hs)** | **57%** |
