# AGENTS.md — GuardiaCloud.Sla.McpWorkshop (.NET 10)

## Propósito del Repositorio
Servidor **MCP en C# (`ModelContextProtocol` v2.3.0)**, **Skill de equipo (`SKILL.md`)** y **Agente de Triage (`Microsoft.Extensions.AI` v10.11.0)** para auditar políticas de SLA y contratos de error RFC 9457 en la plataforma `GuardiaCloud.Sla`.

## Comandos de Compilación, Test y Verificación
- **Compilar sin warnings:** `dotnet build GuardiaCloud.Sla.McpWorkshop.sln --nologo`
- **Correr todos los tests:** `dotnet test GuardiaCloud.Sla.McpWorkshop.sln --no-build --nologo`
- **Verificar la Skill de equipo:** `./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh`
- **Ejecutar el servidor MCP (`stdio`):** `dotnet run --project src/GuardiaCloud.Sla.McpServer/GuardiaCloud.Sla.McpServer.csproj`

## Invariantes de Arquitectura (.NET 10 + MCP + Agent SDK)
1. **Cero logs en `stdout` cuando corre el servidor MCP `stdio`:** Todo log de `ILogger` debe ir a `stderr` (`ConsoleLogOptions.LogToStandardErrorThreshold = LogLevel.Trace`) para no corromper los frames JSON-RPC de `stdio`.
2. **Anotaciones y descripciones explícitas en MCP Tools:** Todo método `[McpServerTool]` en `SlaMcpTools` debe declarar `Name`, `ReadOnly = true`, `Idempotent = true`, `Destructive = false`, `OpenWorld = false` y `[Description("...")]` tanto en el método como en cada parámetro.
3. **Defensa contra Prompt Injection Indirecto y Entradas Inválidas:** Nunca interpolar texto libre de un incidente sin sanitizar patrones de secuestro de instrucciones (`SYSTEM OVERRIDE`, `IGNORE PREVIOUS INSTRUCTIONS`), y validar `clientTier` y `severity` contra listas blancas explícitas.
4. **Abstracción del tiempo y límites del bucle agéntico:** Usar siempre `System.TimeProvider` inyectado (nunca `DateTimeOffset.UtcNow` directo) y configurar `MaximumIterationsPerRequest = 4`, `MaximumConsecutiveErrorsPerRequest = 2` y `TerminateOnUnknownCalls = true` en `FunctionInvokingChatClient`.
