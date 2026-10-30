# Guía del Facilitador y Rúbrica de Evaluación (`ws-m1-skills-mcp-dotnet`)

- **Unidades cubiertas:** **Unidad 1.3** (*Agentes, Patrones Agénticos y Skills Reutilizables*) + **Unidad 1.5** (*Model Context Protocol (MCP) en .NET y Azure*)
- **Duración total:** 225 minutos (3 hs 45 min)
- **Entregable Evaluable #1:** **15% de la nota final del curso** (Rúbrica sobre 100 puntos)

---

## 1. Notas de Facilitación y Gestión de Tiempos en el Aula

### Minuto 0:00 – 0:15 (Fase 0: Diagnóstico)
- **Objetivo docente:** Asegurar que todas las duplas tengan los paquetes NuGet (`ModelContextProtocol v2.3.0` y `Microsoft.Extensions.AI v10.11.0`) restaurados y que vean pasar los 2 tests base antes de escribir una sola línea.
- **Tip clave:** Pediles que abran `src/GuardiaCloud.Sla.McpServer/Infrastructure/InMemorySlaCatalogStore.cs` y lean en voz alta el resumen de `INC-2026-1002`. Preguntá al grupo: *"¿Qué pasa si un agente lee ese ticket desde Jira o ServiceNow y tiene conectada una tool MCP que puede cerrar incidentes o enviar emails sin confirmación?"* Esto introduce de forma visceral la necesidad de `ReadOnlyHint`, listas blancas y sanitización contra **Prompt Injection Indirecto**.

### Minuto 0:15 – 1:15 (Fase 1: Ingeniería de Agent Skills — Unidad 1.3A)
- **Error común #1 — Copiar el catálogo entero dentro de `SKILL.md`:** Muchas duplas van a querer pegar toda la tabla de `references/rfc9457-catalogo-errores.md` adentro de `SKILL.md` o incluso en `AGENTS.md`.
  - **Intervención del facilitador:** Recordá los 3 niveles de *progressive disclosure* del estándar `agentskills.io` y el estudio de ETH Zurich (`arXiv:2602.11988`): `SKILL.md` debe mantenerse conciso (<80 líneas) y apuntar explícitamente a `references/rfc9457-catalogo-errores.md` para que el catálogo detallado solo consuma tokens cuando la tarea involucra contratos de error HTTP.
- **Error común #2 — `description` vaga en el frontmatter YAML:** Si escriben `description: "Skill para Minimal APIs"`, el agente no sabrá cuándo activarla frente a un problema de `ProblemDetails` o `TimeProvider`, o la activará innecesariamente al editar estilos CSS. Exigí **disparadores positivos + anti-disparadores (`NO activar para...`)**.

### Minuto 1:15 – 2:30 (Fase 2: Servidor MCP en C# — Unidad 1.5)
- **Error común #3 — Usar `Console.WriteLine` para depurar un servidor MCP `stdio`:**
  - **Intervención del facilitador:** Si un participante pone `Console.WriteLine("Debug...")` dentro de `SlaMcpTools.cs`, el cliente MCP (Claude Code / VS Code) va a fallar al parsear JSON-RPC porque `stdout` es el canal de transporte del protocolo. Mostrá por qué en `Program.cs` configuramos:
    ```csharp
    builder.Logging.AddConsole(options =>
    {
        options.LogToStandardErrorThreshold = LogLevel.Trace;
    });
    ```
    Cualquier log diagnóstico en un servidor MCP `stdio` debe ir a `stderr` (`ILogger` o `Console.Error.WriteLine`).
- **Pregunta frecuente de arquitectos .NET — *"¿Cuándo usamos `stdio` vs. `ModelContextProtocol.AspNetCore` (Streamable HTTP)?"*:**
  - **`stdio` (`ModelContextProtocol`):** Ideal para herramientas locales de desarrollo que corren en la máquina del ingeniero como subproceso del IDE/CLI (baja latencia, sin puertos abiertos).
  - **Streamable HTTP (`ModelContextProtocol.AspNetCore`):** Ideal para servidores MCP corporativos desplegados en **Azure Container Apps** o **Azure App Service** compartidos por toda la consultora, donde se requiere autenticación centralizada (**Microsoft Entra ID / OAuth 2.1**) y acceso controlado a bases de datos o Azure Monitor sin distribuir credenciales locales a cada laptop.

### Minuto 2:30 – 3:20 (Fase 3: Agente con `Microsoft.Extensions.AI` — Unidad 1.3B)
- **Por qué enseñamos `IChatClient` + `FunctionInvokingChatClient`:**
  - Mostrales a los participantes cómo las mismas funciones de `SlaMcpTools` sirven tanto para ser expuestas por MCP a agentes externos (`[McpServerTool]`) como para ser invocadas en proceso por un agente propio de backend en .NET mediante `AIFunctionFactory.Create`.
  - Destacá las 3 propiedades de seguridad de `FunctionInvokingChatClient`:
    - `MaximumIterationsPerRequest = 4` (evita bucles infinitos que drenen presupuesto de tokens en Azure AI Foundry).
    - `MaximumConsecutiveErrorsPerRequest = 2` (corta la ejecución si una herramienta falla repetidamente).
    - `TerminateOnUnknownCalls = true` (frena al agente si alucina el nombre de una herramienta inexistente).

---

## 2. Solución de Problemas Frecuentes (Troubleshooting)

| Síntoma | Causa raíz | Solución rápida |
|---|---|---|
| `verify-minimal-api.sh: Permission denied` | El script perdió el bit de ejecución al copiarse. | Ejecutar `chmod +x ./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh`. |
| `dotnet build` falla por warnings (`CS1591` o variables sin usar) | El proyecto tiene `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`. | Eliminar variables no usadas o completar la implementación de los métodos `TODO`. |
| El test `InspectIncidentSlaStatus` da un `EffectiveElapsedMinutes` distinto de `80.0` | Se usó `DateTimeOffset.UtcNow` directo en vez de `_timeProvider.GetUtcNow()`. | Reemplazar `DateTimeOffset.UtcNow` por `_timeProvider.GetUtcNow()` en `SlaMcpTools.cs`. |
| El servidor MCP en `.mcp.json` tarda en responder la primera vez o falla por salida de compilación | `dotnet run` compila en `stdout` antes de iniciar el proceso. | Compilar primero con `dotnet build` y pasar `"--no-build"` en `args` dentro de `.mcp.json` con `"DOTNET_NOLOGO": "1"`. |

---

## 3. Rúbrica de Evaluación del Entregable #1 (100 Puntos = 15% Nota Final)

| Criterio | Peso | Excelente (100%) | Aceptable (70%) | Insuficiente (0–40%) |
|---|---:|---|---|---|
| **1. Diseño de la Agent Skill (`SKILL.md` + *Progressive Disclosure*)** | **25 pts** | Frontmatter YAML con `name` y `description` precisos (disparadores + anti-disparadores). Cuerpo estructurado que referencia bajo demanda `references/rfc9457-catalogo-errores.md` y pasa `./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh` con código `0`. | Pasa el script verificador pero la descripción del frontmatter no define anti-disparadores o duplica parte del catálogo en `SKILL.md`. | `SKILL.md` conserva marcadores `TODO`, no referencia el catálogo o falla `verify-minimal-api.sh`. |
| **2. Servidor MCP en C# (`ModelContextProtocol` v2.3.0)** | **25 pts** | Las 3 herramientas (`get_client_sla_policy`, `inspect_incident_sla_status`, `validate_rfc9457_contract`) están decoradas con `[McpServerTool]`, `[Description]` en métodos y parámetros, y anotaciones completas (`ReadOnly = true`, `Idempotent = true`, `Destructive = false`, `OpenWorld = false`). | Las 3 herramientas funcionan pero omiten `[Description]` en parámetros o alguna anotación de seguridad (`ReadOnly`/`Destructive`). | Menos de 3 herramientas registradas en DI o uso de `DateTimeOffset.UtcNow` en lugar de `TimeProvider`. |
| **3. Seguridad MCP y Defensa contra Prompt Injection Indirecto** | **20 pts** | Validación estricta por lista blanca para `clientTier` y `severity` con códigos RFC 9457 (`SLA-400-*`), y sanitización efectiva de `incident.Summary` con `SanitizeUntrustedNotes` neutralizando el `SYSTEM OVERRIDE` de `INC-2026-1002`. | Sanitiza el resumen pero no valida entradas con códigos canónicos, o viceversa. | Devuelve `incident.Summary` crudo permitiendo que la instrucción maliciosa llegue intacta al contexto del agente. |
| **4. Agente en C# con `Microsoft.Extensions.AI` (`v10.11.0`)** | **20 pts** | `SlaTriageAgent` registra las 3 herramientas con `AIFunctionFactory.Create` y configura `FunctionInvokingChatClient` con `MaximumIterationsPerRequest = 4`, `MaximumConsecutiveErrorsPerRequest = 2` y `TerminateOnUnknownCalls = true`. | El pipeline `UseFunctionInvocation` funciona pero omite las condiciones explícitas de parada (`MaximumIterationsPerRequest`). | `RunTriageAsync` lanza `NotImplementedException` o invoca las herramientas manualmente sin pasar por `IChatClient`. |
| **5. Suite de Verificación Automatizada (`dotnet test` sin warnings)** | **10 pts** | Compila con 0 warnings (`TreatWarningsAsErrors=true`) y pasan los 6 tests xUnit en `GuardiaCloud.Sla.McpTests` verificando políticas, rechazo de inputs inválidos, sanitización anti-inyección, contratos RFC 9457, registro DI y bucle multi-tool. | Compila y pasan al menos 4 tests cubriendo MCP y agente. | No compila o fallan tests en `dotnet test`. |

### Comando de Corrección Rápida para el Docente
Para evaluar la entrega de una dupla en menos de 5 segundos:
```bash
./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh && dotnet test GuardiaCloud.Sla.McpWorkshop.sln --nologo
```
