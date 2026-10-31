# AGENTS.md — GuardiaCloud.CommandCenter (.NET 10 Capstone Seed)

## Propósito del Repositorio
Repositorio semilla del **Proyecto Integrador (Módulo 3 — 14 hs)**: centro de comando operativo y financiero de SLA para clientes bancarios y aseguradoras (`GuardiaCloud.CommandCenter.Api`).

## Comandos de Compilación y Oráculo de Verificación
- **Compilar sin warnings:** `dotnet build GuardiaCloud.CommandCenter.sln --nologo`
- **Correr todos los tests:** `dotnet test GuardiaCloud.CommandCenter.sln --no-build --nologo`
- **Correr solo el Oráculo de Arquitectura (`NetArchTest`):** `dotnet test GuardiaCloud.CommandCenter.sln --filter FullyQualifiedName~ArchitectureOracle --no-build --nologo`

## Reglas de Arquitectura y Paralelización en Equipo (3–5 personas)
1. **Aislamiento de `Domain` (`NetArchTest`):** Ningún tipo en `GuardiaCloud.CommandCenter.Api.Domain` puede depender de `Infrastructure` ni de `Microsoft.AspNetCore.Http`. Toda clase en `Domain` debe ser `sealed`.
2. **Abstracción del tiempo:** Usar siempre `System.TimeProvider` inyectado (`timeProvider.GetUtcNow()`); prohibido usar `DateTime.UtcNow` o `DateTimeOffset.UtcNow` directo.
3. **Errores RFC 9457 (`ProblemDetails`):** Todo error 4xx debe devolver `Results.Problem(...)` incluyendo `type`, `title`, `statusCode`, `detail` y `extensions["errorCode"]`.
4. **Fronteras de archivos para `git worktrees` paralelos:** Cada Vertical Slice (`BUG-301`, `FEAT-301`, `FEAT-302`, `FEAT-303`) debe mantener su lógica aislada para evitar colisiones de merge entre integrantes del equipo.
