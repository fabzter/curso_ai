# AGENTS.md — GuardiaCloud.CommandCenter (.NET 10 Capstone Reference)

## Propósito del Repositorio
Centro de comando operativo y financiero de SLA para clientes bancarios y aseguradoras (`GuardiaCloud.CommandCenter.Api`), gobernado con **Spec-Driven Development (`specs/command-center-v2/`)**, **`NetArchTest.Rules` (`v1.3.2`)** y **`WebApplicationFactory<Program>`**.

## Comandos de Compilación y Oráculo de Verificación
- **Compilar sin warnings:** `dotnet build GuardiaCloud.CommandCenter.sln --nologo`
- **Correr todos los tests (8 suites):** `dotnet test GuardiaCloud.CommandCenter.sln --no-build --nologo`
- **Correr solo el Oráculo de Arquitectura (`NetArchTest`):** `dotnet test GuardiaCloud.CommandCenter.sln --filter FullyQualifiedName~ArchitectureOracle --no-build --nologo`

## Reglas de Arquitectura y Paralelización en Equipo (3–5 personas)
1. **Aislamiento de `Domain` (`NetArchTest`):** Ningún tipo en `GuardiaCloud.CommandCenter.Api.Domain` puede depender de `Infrastructure` ni de `Microsoft.AspNetCore.Http`. Toda clase en `Domain` debe ser `sealed`.
2. **Abstracción del tiempo:** Usar siempre `System.TimeProvider` inyectado (`timeProvider.GetUtcNow()`); prohibido usar `DateTime.UtcNow` o `DateTimeOffset.UtcNow` directo.
3. **Errores RFC 9457 (`ProblemDetails`):** Todo error 4xx debe devolver `Results.Problem(...)` incluyendo `type`, `title`, `statusCode`, `detail` y `extensions["errorCode"]` (`CC-404-INCIDENT-NOT-FOUND`, `CC-400-SAME-APPROVER`, `CC-422-INVALID-DUAL-TOKEN`, `CC-400-INVALID-CLIENT-TIER`).
4. **Trazabilidad Spec $\leftrightarrow$ Test:** Ningún PR se fusiona sin pasar los 8 tests de `CommandCenterTests`.
