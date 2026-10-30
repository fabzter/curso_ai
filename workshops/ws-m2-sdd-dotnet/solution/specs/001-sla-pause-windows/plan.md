# Implementation Plan: Ventanas de Pausa y Reanudación Auditable de SLA (`001-sla-pause-windows`)

**Branch**: `001-sla-pause-windows` | **Date**: 2026-10-30 | **Spec**: `specs/001-sla-pause-windows/spec.md`

## Summary

Extender `GuardiaCloud.Sla.Api` (.NET 10 Minimal APIs) para soportar ventanas de pausa auditables (`SlaPauseWindow`) cuando un incidente espera respuesta del cliente (`WaitingForCustomer`), descontando el tiempo pausado del cálculo activo en `SlaCalculator` y desplazando `EffectiveDeadlineUtc`.

## Technical Context

- **Language/Version:** C# 13 / .NET 10 (`net10.0`), `Nullable=enable`, `TreatWarningsAsErrors=true`.
- **Framework:** ASP.NET Core Minimal APIs + `ProblemDetails` (RFC 9457).
- **Time Abstraction:** `System.TimeProvider` (`FakeTimeProvider` en tests).
- **Testing:** xUnit + `Microsoft.AspNetCore.Mvc.Testing` (`WebApplicationFactory<Program>`).

## Constitution Check

- [x] **I. Tiempo Determinista:** `SlaCalculator` y los endpoints `pause`/`resume` leen la hora exclusivamente desde `TimeProvider`.
- [x] **II. ProblemDetails (RFC 9457):** Validaciones devuelven `400`, `404`, `409` y `422` vía `Results.Problem(...)`.
- [x] **III. Trazabilidad y Auditoría Bancaria:** `SlaPauseWindow` exige `Reason`, `RequestedBy`, `EvidenceNote` y timestamps UTC.
- [x] **IV. Test-First con `WebApplicationFactory`:** Se agregan pruebas de integración extremo a extremo en `SlaApiIntegrationTests.cs`.

## Data Model & Contracts

### 1. Cambios en Dominio (`src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs`)
- `IncidentStatus`: agregar `WaitingForCustomer = 4`.
- `SlaPauseReason`: enum `WaitingForCustomerLogs = 1`, `WaitingForCustomerVpnAccess = 2`, `WaitingForCustomerValidation = 3`.
- `SlaPauseWindow`: entidad con `Id`, `Reason`, `RequestedBy`, `EvidenceNote`, `PausedAtUtc`, `ResumedAtUtc`, `ResumedBy`, `IsActive` y `GetDurationMinutes(DateTimeOffset evaluationPointUtc)`.
- `Incident`: agregar `List<SlaPauseWindow> PauseWindows { get; } = [];`.
- DTOs: `PauseSlaRequest`, `ResumeSlaRequest`, y ampliación de `SlaStatusResponse` con `TotalPausedMinutes` y `PauseCount`.

### 2. Contratos HTTP (`src/GuardiaCloud.Sla.Api/Program.cs`)
- `POST /api/incidents/{id:guid}/sla/pause`: valida estado y campos obligatorios, agrega `SlaPauseWindow` y cambia `Status` a `WaitingForCustomer`.
- `POST /api/incidents/{id:guid}/sla/resume`: valida pausa activa, cierra la ventana y cambia `Status` a `InProgress`.
- `POST /api/incidents/{id:guid}/resolve`: si existe una ventana activa al resolver, la cierra automáticamente en `ResolvedAtUtc`.
