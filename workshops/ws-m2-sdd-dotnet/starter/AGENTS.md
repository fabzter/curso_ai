# AGENTS.md — GuardiaCloud.Sla (.NET 10)

Servicio de seguimiento de acuerdos de nivel de servicio (SLA) para incidentes operativos de clientes enterprise.

## Comandos de verificación (ejecutá siempre antes de dar una tarea por cerrada)

- Compilar sin warnings: `dotnet build GuardiaCloud.Sla.sln --no-restore` (`TreatWarningsAsErrors=true` está activo)
- Correr todos los tests (xUnit + `WebApplicationFactory`): `dotnet test GuardiaCloud.Sla.sln --no-build`
- Filtrar un test puntual: `dotnet test --filter FullyQualifiedName~NombreDelTest`

## Invariantes de arquitectura (.NET 10 / ASP.NET Core Minimal APIs)

1. **Tiempo determinista:** NUNCA uses `DateTime.UtcNow` ni `DateTimeOffset.UtcNow` directo en dominio o servicios. Inyectá siempre `TimeProvider` (`TimeProvider.GetUtcNow()`) para que los tests de integración controlen el reloj con `FakeTimeProvider`.
2. **Errores HTTP estandarizados:** Todo error de validación o de regla de negocio debe responder `application/problem+json` (RFC 9457) mediante `Results.Problem(...)`:
   - `400 Bad Request` para datos faltantes o formato inválido.
   - `404 Not Found` cuando el `IncidentId` no existe.
   - `409 Conflict` para transiciones de estado inválidas (ej. pausar un incidente ya pausado o ya resuelto).
   - `422 Unprocessable Entity` para violaciones de reglas de dominio (ej. fechas inconsistentes o presupuesto de pausa excedido sin autorización).
3. **Timestamps en UTC:** Toda fecha persistida o calculada debe normalizarse con `.ToUniversalTime()`.
4. **Tests de integración obligatorios:** Toda ruta nueva o cambio de regla en `SlaCalculator` requiere al menos un test de integración en `tests/GuardiaCloud.Sla.Tests` usando `WebApplicationFactory<Program>` y `FakeTimeProvider`.
