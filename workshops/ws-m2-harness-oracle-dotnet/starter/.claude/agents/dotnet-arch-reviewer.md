---
name: dotnet-arch-reviewer
description: Subagente revisor de arquitectura limpia .NET 10, contratos ProblemDetails RFC 9457 y reglas NetArchTest en GuardiaCloud.Sla.
tools: Read, Grep, Glob, Bash
---

# Subagente: Revisor de Arquitectura .NET (`dotnet-arch-reviewer`)

> **TODO (Fase 1 - Unidad 1.4):** Completá el protocolo de revisión de este subagente en 4 puntos:
> 1. Verificar que ninguna clase en `GuardiaCloud.Sla.Api.Domain` dependa de `GuardiaCloud.Sla.Api.Infrastructure` ni de `Microsoft.AspNetCore.Http`.
> 2. Verificar que todas las clases de `Domain` sean `sealed` (o `static`) y usen `System.TimeProvider` en lugar de `DateTimeOffset.UtcNow`.
> 3. Verificar que los errores HTTP devuelvan `Results.Problem` (RFC 9457) con `extensions["errorCode"]`.
> 4. Ejecutar `dotnet test --filter FullyQualifiedName~ArchitectureOracleTests --no-restore` y reportar cualquier violación.
