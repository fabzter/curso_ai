# Design: `cap-p1-pause-budget`

## Decisiones Técnicas
1. **Regla en `SlaPolicyCatalog`:** Exponer `GetMaxPauseBudgetMinutes(IncidentPriority priority)` devolviendo `30` para `CriticalP1` y `null` para el resto de las prioridades.
2. **Cálculo en `SlaCalculator.Evaluate`:**
   - Calcular `rawPausedMinutes` como la suma de duraciones de todas las `PauseWindows`.
   - Verificar `hasSupervisorOverride = incident.PauseWindows.Any(w => !string.IsNullOrWhiteSpace(w.SupervisorOverrideCode))`.
   - Si `maxBudget.HasValue && !hasSupervisorOverride`, truncar `creditedPausedMinutes = Math.Min(rawPausedMinutes, maxBudget.Value)` y exponer `RemainingPauseBudgetMinutes = Math.Max(0, maxBudget.Value - creditedPausedMinutes)`.
3. **Validación preventiva en `POST /api/incidents/{id:guid}/sla/pause`:**
   - Si `alreadyPausedMinutes >= maxBudget.Value && !hasOverride`, rechazar con HTTP `422 Unprocessable Entity` vía `Results.Problem(...)`.
