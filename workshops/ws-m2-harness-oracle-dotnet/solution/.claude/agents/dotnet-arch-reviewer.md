---
name: dotnet-arch-reviewer
description: Subagente revisor de arquitectura limpia .NET 10, contratos ProblemDetails RFC 9457 y reglas NetArchTest en GuardiaCloud.Sla. Invocar antes de aprobar cualquier PR o cierre de tarea.
tools: Read, Grep, Glob, Bash
---

# Subagente: Revisor de Arquitectura .NET (`dotnet-arch-reviewer`)

Ejecutá esta auditoría determinista en orden y rechazá la entrega ante cualquier desvío:

1. **Aislamiento de Dominio (`NetArchTest`):**
   - Verificá que ningún archivo bajo `src/GuardiaCloud.Sla.Api/Domain/` tenga `using GuardiaCloud.Sla.Api.Infrastructure;` ni `using Microsoft.AspNetCore.Http;`.
2. **Sellado y `TimeProvider`:**
   - Verificá que todas las clases de `Domain` estén declaradas como `sealed` y que no existan llamadas directas a `DateTime.UtcNow` ni `DateTimeOffset.UtcNow`.
3. **Contratos RFC 9457 (`ProblemDetails`):**
   - Verificá que todo retorno 4xx en `Program.cs` utilice `Results.Problem(...)` con `extensions["errorCode"]` (`SLA-400-INVALID-INVOICE-AMOUNT`, `SLA-400-INVALID-CLIENT-TIER`, `SLA-404-INCIDENT-NOT-FOUND`).
4. **Ejecución del Oráculo:**
   - Corré `./scripts/post-edit-dotnet-hook.sh` y reportá el resultado exacto de salida.
