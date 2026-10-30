# GuardiaCloud.Sla Constitution

## Core Principles

### I. Tiempo Determinista (NO NEGOCIABLE)
Ningún modelo de dominio, servicio o endpoint puede invocar `DateTime.UtcNow` o `DateTimeOffset.UtcNow` directamente. Todo acceso al reloj del sistema debe pasar por `System.TimeProvider` inyectado vía contenedor de dependencias, garantizando que `FakeTimeProvider` pueda reproducir cualquier escenario horario en milisegundos.

### II. Contratos HTTP explícitos y ProblemDetails (RFC 9457)
Toda respuesta de error en ASP.NET Core Minimal APIs debe emitirse mediante `Results.Problem(...)` con códigos semánticos estrictos:
- `400 Bad Request` para campos obligatorios faltantes (`TenantId`, `RequestedBy`, `EvidenceNote`).
- `404 Not Found` para recursos inexistentes.
- `409 Conflict` para transiciones inválidas en la máquina de estados del incidente (doble pausa, reanudar sin pausa activa, pausar un incidente resuelto).
- `422 Unprocessable Entity` para invariantes temporales o topes de negocio (`PausedAtUtc < OpenedAtUtc`, `ResumedAtUtc < PausedAtUtc`, presupuesto de pausa agotado).

### III. Trazabilidad y Auditoría Bancaria
Toda modificación al cómputo de un SLA (apertura, pausa, reanudación, resolución o excepción de supervisor) es auditable: requiere actor (`RequestedBy` / `ResumedBy`), motivo tipado (`SlaPauseReason`), evidencia textual (`EvidenceNote`) y marcas de tiempo normalizadas en UTC (`.ToUniversalTime()`).

### IV. Test-First con `WebApplicationFactory` (NO NEGOCIABLE)
Ningún cambio en `SlaCalculator` o en las rutas `/api/incidents` se considera completo sin pruebas de integración automatizadas en `tests/GuardiaCloud.Sla.Tests` que ejerciten el pipeline HTTP completo en memoria.

## Restricciones Técnicas (.NET 10)
- Target Framework: `net10.0` con `Nullable=enable` y `TreatWarningsAsErrors=true`.
- Cero dependencias externas innecesarias: priorizar tipos nativos de la BCL de .NET 10.

## Gobernanza
Esta Constitución rige tanto las especificaciones de **GitHub Spec Kit** (`.specify/` y `specs/`) como las especificaciones delta de **OpenSpec** (`openspec/`). Todo `/speckit-plan` y `/speckit-converge` debe verificar el cumplimiento de estos 4 principios.
