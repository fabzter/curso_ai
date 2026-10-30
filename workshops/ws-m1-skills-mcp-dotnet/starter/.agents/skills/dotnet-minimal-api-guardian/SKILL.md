---
name: dotnet-minimal-api-guardian
description: TODO (Fase 1 - Unidad 1.3): Escribí acá una descripción rica en palabras clave de activación (Minimal APIs, ProblemDetails RFC 9457, TimeProvider, CancellationToken, GuardiaCloud.Sla) y sus anti-disparadores.
---

# Skill: Guardián de Convenciones .NET Minimal API & RFC 9457 (`GuardiaCloud.Sla`)

> **TODO (Fase 1 - Unidad 1.3):** Completá las instrucciones paso a paso de esta Skill siguiendo el estándar abierto `agentskills.io` (carga progresiva de contexto):
> 1. **Cuándo activar esta Skill y cuándo NO activarla.**
> 2. **Flujo obligatorio en 4 pasos:**
>    - Paso 1: Leer bajo demanda `references/rfc9457-catalogo-errores.md`.
>    - Paso 2: Validar las 4 invariantes C# (uso de `Results.Problem` con `extensions["errorCode"]`, inyección de `System.TimeProvider`, propagación de `CancellationToken`, y llamada a `validate_rfc9457_contract` en el servidor MCP `guardiacloud-sla`).
>    - Paso 3: Ejecutar el script determinista `./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh`.
>    - Paso 4: Ejecutar `dotnet test` antes de dar la tarea por terminada.
