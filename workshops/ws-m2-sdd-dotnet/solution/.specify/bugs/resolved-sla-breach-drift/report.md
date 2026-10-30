# Bug Fix Report: `resolved-sla-breach-drift`

- **Command Flow:** `/speckit-bug-assess` $\rightarrow$ `/speckit-bug-fix` $\rightarrow$ `/speckit-bug-test`
- **Symptom reported:** Un incidente `CriticalP1` abierto a las 12:00 UTC y resuelto a las 12:40 UTC (dentro de los 60 min de SLA) aparece a la mañana siguiente en `GET /api/incidents/{id}/sla` con `isBreached: true` y más de 1000 minutos consumidos.
- **Final Verdict:** `verified`

## 1. Root Cause Assessment (`/speckit-bug-assess`)
En `src/GuardiaCloud.Sla.Api/Services/SlaServices.cs`, el método `SlaCalculator.Evaluate(Incident incident)` calculaba siempre:
```csharp
var referenceEndUtc = timeProvider.GetUtcNow();
```
ignorando por completo `incident.ResolvedAtUtc` cuando `incident.Status == IncidentStatus.Resolved`. Como consecuencia, el tiempo activo seguía corriendo indefinidamente después del cierre del incidente.

## 2. Scoped Fix (`/speckit-bug-fix`)
1. En `SlaCalculator.Evaluate`, fijar el extremo superior del intervalo en `incident.ResolvedAtUtc.Value` siempre que `incident.Status == IncidentStatus.Resolved && incident.ResolvedAtUtc.HasValue`.
2. En `POST /api/incidents/{id:guid}/resolve`, si el incidente tenía una ventana de pausa activa al momento de resolverse, cerrarla automáticamente en `resolvedAt` (`system:auto-resume-on-resolve`) para mantener consistente el historial.

## 3. Verification (`/speckit-bug-test`)
- **Test de regresión agregado:** `SlaApiIntegrationTests.ResolvedIncident_FreezesSlaClock_AtResolvedAtUtc_RegressionTest`
- **Comando:** `dotnet test --filter FullyQualifiedName~ResolvedIncident_FreezesSlaClock` $\rightarrow$ **PASSED**.
