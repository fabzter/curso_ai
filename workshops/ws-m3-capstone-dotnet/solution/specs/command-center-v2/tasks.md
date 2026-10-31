# Grafo de Tareas Paralelizable (`tasks.md` — Unidad 3.3)

| ID | Tarea | Rol Responsable | Worktree / Rama | Modo (`HITL` / `Full AI`) | Comando de Verificación (Oráculo) |
|---|---|---|---|---|---|
| **T-01** | Escribir primero los 5 tests de aceptación HTTP en `CommandCenterTests.cs` (TDD Agéntico). | *QA & Oracle Lead* | `main` (Sprint 1 inicio) | **HITL** | `dotnet build` (los tests compilan y fallan según lo esperado) |
| **T-02** | Reparar `BUG-301` en `CommandCenterEvaluator.ApplyWebhookEvent` usando `ProcessedWebhookEventIds`. | *Backend & MCP Lead* | `wt-bug301` | **Full AI** | `dotnet test --filter FullyQualifiedName~WebhookEvent_IsIdempotent` |
| **T-03** | Implementar `FEAT-301` (`EvaluateProactiveEscalation` + ruta HTTP `/escalations/evaluate/{incidentId}`). | *Product & Spec Lead* | `wt-feat301` | **Full AI** | `dotnet test --filter FullyQualifiedName~ProactiveEscalation` |
| **T-04** | Implementar `FEAT-302` (`ApplyForceMajeureExemption` + validaciones RFC 9457 `CC-400-SAME-APPROVER` y `CC-422-INVALID-DUAL-TOKEN`). | *Architect & Harness Lead* | `wt-feat302` | **HITL** (auditoría regulatoria) | `dotnet test --filter FullyQualifiedName~ForceMajeureExemption` |
| **T-05** | Implementar `FEAT-303` (`BuildTierDashboard` + ruta HTTP `/dashboard/{clientTier}`). | *QA & Integration Lead* | `wt-feat303` | **Full AI** | `dotnet test --filter FullyQualifiedName~TierDashboard` |
