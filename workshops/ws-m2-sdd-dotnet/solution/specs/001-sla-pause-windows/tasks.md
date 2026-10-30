---
description: "Task list for 001-sla-pause-windows"
---

# Tasks: Ventanas de Pausa y Reanudación Auditable de SLA (`001-sla-pause-windows`)

**Input**: `specs/001-sla-pause-windows/spec.md`, `specs/001-sla-pause-windows/plan.md`

## Phase 1: Dominio y Cálculo de SLA

- [x] T001 [US1] Agregar `IncidentStatus.WaitingForCustomer`, `SlaPauseReason`, `SlaPauseWindow`, `PauseSlaRequest`, `ResumeSlaRequest` y campos `TotalPausedMinutes`/`PauseCount` en `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs`
- [x] T002 [US1] Actualizar `SlaCalculator.Evaluate` en `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs` para restar las ventanas de pausa del tiempo activo y desplazar `EffectiveDeadlineUtc`

## Phase 2: Endpoints Minimal API y Reglas de Estado

- [x] T003 [US1] Implementar `POST /api/incidents/{id:guid}/sla/pause` y `POST /api/incidents/{id:guid}/sla/resume` más cierre automático de pausa en `/resolve` dentro de `src/GuardiaCloud.Sla.Api/Program.cs`
- [x] T004 [US2] Validar códigos de error `400 Bad Request`, `404 Not Found`, `409 Conflict` y `422 Unprocessable Entity` con `Results.Problem` en `src/GuardiaCloud.Sla.Api/Program.cs`

## Phase 3: Verificación e Integración (`WebApplicationFactory`)

- [x] T005 [P] [US1] Agregar test de integración `PauseAndResumeSla_OnHighP2_ExcludesPausedWindowAndShiftsDeadline` en `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs`
- [x] T006 [P] [US2] Agregar test de integración `DoublePause_ReturnsProblemDetails409Conflict` en `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs`

---

## Convergence Assessment (`/speckit-converge`)

- **Date:** 2026-10-30
- **Build check:** `dotnet build GuardiaCloud.Sla.sln --no-restore` $\rightarrow$ `0 Warning(s), 0 Error(s)`
- **Test check:** `dotnet test GuardiaCloud.Sla.sln --no-build` $\rightarrow$ `Passed!`
- **Status:** `Converged` (Todos los requerimientos REQ-001..REQ-005 y criterios de aceptación de US1 y US2 están implementados y verificados por pruebas de integración).
