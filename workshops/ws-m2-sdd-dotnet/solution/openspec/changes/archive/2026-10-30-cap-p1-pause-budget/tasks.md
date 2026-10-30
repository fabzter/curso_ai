# Tasks: `cap-p1-pause-budget`

- [x] 1.1 Agregar `SupervisorOverrideCode` a `SlaPauseWindow` y `PauseSlaRequest`, `RemainingPauseBudgetMinutes` a `SlaStatusResponse`, y `GetMaxPauseBudgetMinutes` en `SlaPolicyCatalog` (`src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs`).
- [x] 1.2 Aplicar el tope de 30 minutos de pausa en `SlaCalculator.Evaluate` cuando `Priority == CriticalP1` y no exista `SupervisorOverrideCode` (`src/GuardiaCloud.Sla.Api/Services/SlaServices.cs`).
- [x] 1.3 Rechazar con `422 Unprocessable Entity` nuevas pausas en `POST /api/incidents/{id:guid}/sla/pause` cuando el presupuesto P1 esté agotado sin `SupervisorOverrideCode` (`src/GuardiaCloud.Sla.Api/Program.cs`).
- [x] 2.1 Agregar test de integración `CriticalP1_PauseBudget_CapsAt30Minutes_UnlessSupervisorOverrideProvided` en `tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs`.
