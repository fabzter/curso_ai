# Proposal: Tope de 30 minutos al presupuesto de pausa en incidentes Critical P1 (`cap-p1-pause-budget`)

## Why
Luego de dos semanas en producción con las ventanas de pausa de SLA habilitadas, los bancos clientes detectaron que algunos incidentes `CriticalP1` permanecieron pausados durante más de 2 horas sin escalamiento gerencial. El comité de auditoría exige limitar el tiempo de pausa acreditable en incidentes `CriticalP1` a un máximo acumulado de **30 minutos**, salvo que un Supervisor autorice explícitamente la pausa mediante un `SupervisorOverrideCode`.

## What Changes
- **Tope de pausa en `CriticalP1`:** Los incidentes con prioridad `CriticalP1` tienen un presupuesto estándar de pausa acreditable de **30 minutos acumulados** (`CriticalP1StandardPauseBudgetMinutes = 30`).
- **Excepción auditable por Supervisor:** `PauseSlaRequest` y `SlaPauseWindow` aceptan un campo opcional `SupervisorOverrideCode`. Si el incidente `CriticalP1` ya consumió $\ge 30$ minutos de pausa y no posee `SupervisorOverrideCode`, cualquier intento de abrir una nueva pausa se rechaza con HTTP `422 Unprocessable Entity` (`ProblemDetails`).
- **Tope en el cálculo de `SlaCalculator`:** Si una pausa activa o cerrada en un `CriticalP1` sin `SupervisorOverrideCode` supera los 30 minutos acumulados, solo se acreditan hasta 30 minutos en `TotalPausedMinutes` (el excedente vuelve a correr como tiempo activo `ElapsedActiveMinutes`).
- **Exposición de presupuesto restante:** `SlaStatusResponse` incorpora `RemainingPauseBudgetMinutes` (`double?`, `null` para `HighP2`/`StandardP3` o cuando hay override de supervisor; `0..30` para `CriticalP1` estándar).

## Capabilities
- **New Capabilities:** *(ninguna)*
- **Modified Capabilities:**
  - `sla-tracking`: Agrega el tope de presupuesto de pausa de 30 minutos para incidentes `CriticalP1` y la excepción por `SupervisorOverrideCode`.

## Impact
- `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs`
- `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs`
- `src/GuardiaCloud.Sla.Api/Program.cs`
- `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs`
