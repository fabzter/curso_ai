# AGENTS.md — GuardiaCloud.Sla.HarnessLab (.NET 10)

## Propósito
Microservicio `GuardiaCloud.Sla.Api` para cálculo de créditos financieros por SLA y exportación operativa de guardia, gobernado por **Oráculos de Arquitectura (`NetArchTest.Rules` v1.3.2)** y **Pruebas de Integración (`WebApplicationFactory`)**.

## Comandos Exactos de Verificación
- **Hook completo del Harness:** `./scripts/post-edit-dotnet-hook.sh`
- **Compilar (0 warnings):** `dotnet build GuardiaCloud.Sla.HarnessLab.sln --nologo`
- **Oráculo de Arquitectura (`NetArchTest`):** `dotnet test GuardiaCloud.Sla.HarnessLab.sln --filter FullyQualifiedName~ArchitectureOracleTests --no-build --nologo`
- **Tests de Integración HTTP:** `dotnet test GuardiaCloud.Sla.HarnessLab.sln --filter FullyQualifiedName~SlaHarnessEndpointsTests --no-build --nologo`

## Invariantes Arquitectónicas Verificadas por Máquina (`NetArchTest`)
1. **Aislamiento estricto de `Domain`:** Ningún tipo en `GuardiaCloud.Sla.Api.Domain` puede depender de `GuardiaCloud.Sla.Api.Infrastructure` ni de `Microsoft.AspNetCore.Http`.
2. **Inmutabilidad y sellado:** Toda clase en `GuardiaCloud.Sla.Api.Domain` debe ser `sealed` (o `static`).
3. **Abstracción del tiempo:** Prohibido usar `DateTime.UtcNow` / `DateTimeOffset.UtcNow` en `Domain`; inyectar siempre `System.TimeProvider`.
4. **Contratos de error RFC 9457:** Todo error HTTP debe usar `Results.Problem(...)` incluyendo `type`, `title`, `statusCode`, `detail` y `extensions["errorCode"]`.
