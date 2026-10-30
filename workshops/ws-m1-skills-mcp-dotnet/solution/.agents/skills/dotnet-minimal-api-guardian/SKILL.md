---
name: dotnet-minimal-api-guardian
description: Estándar de equipo para diseñar, implementar y auditar endpoints ASP.NET Core Minimal APIs y contratos de error ProblemDetails RFC 9457 en GuardiaCloud.Sla (.NET 10). Activar cuando el usuario pida crear o modificar endpoints HTTP, validar códigos de error SLA-4xx, auditar uso de System.TimeProvider o verificar contratos RFC 9457. NO activar para migraciones SQL puras ni estilos CSS/Blazor sin cambios de contrato HTTP.
---

# Skill: Guardián de Convenciones .NET Minimal API & RFC 9457 (`GuardiaCloud.Sla`)

Seguí este protocolo determinista cada vez que diseñes, modifiques o audites un endpoint o contrato de error en la plataforma **`GuardiaCloud.Sla`**.

## 1. Carga Progresiva de Contexto (*Progressive Disclosure*)
1. **No adivines códigos ni URIs de error.** Antes de escribir código C# de manejo de errores, leé bajo demanda [`references/rfc9457-catalogo-errores.md`](references/rfc9457-catalogo-errores.md).
2. Si tenés conectado el servidor MCP `guardiacloud-sla`, invocá la herramienta `validate_rfc9457_contract` pasando `(errorCode, httpStatus, typeUri)` para confirmar que el contrato coincide con el catálogo oficial.

## 2. Las 4 Invariantes Obligatorias en C# (.NET 10)
1. **Errores tipados con RFC 9457 (`ProblemDetails`):**
   - Prohibido devolver `Results.BadRequest(new { error = "..." })` o strings planos.
   - Usá siempre `Results.Problem(...)` o `TypedResults.Problem(...)` incluyendo `type`, `title`, `statusCode`, `detail` y `extensions["errorCode"]`.
2. **Abstracción determinista del tiempo (`System.TimeProvider`):**
   - Prohibido invocar `DateTime.UtcNow` o `DateTimeOffset.UtcNow` directamente en servicios de dominio o endpoints.
   - Inyectá `TimeProvider` por constructor o parámetro de endpoint y usá `timeProvider.GetUtcNow()`.
3. **Cancelación cooperativa y metadatos OpenAPI:**
   - Todo endpoint asíncrono debe recibir `CancellationToken cancellationToken` y declarar `.WithName(...)` y `.ProducesProblem(...)`.
4. **Sanitización de texto no confiable en telemetría/auditoría:**
   - Al exponer resúmenes de incidentes hacia herramientas de IA o logs de triage, sanitizá patrones de *prompt injection* con `InMemorySlaCatalogStore.SanitizeUntrustedNotes(...)`.

## 3. Verificación Determinista antes de Cerrar la Tarea
1. Ejecutá el verificador de la Skill:
   ```bash
   ./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh
   ```
2. Ejecutá la suite de pruebas del proyecto sin warnings:
   ```bash
   dotnet test GuardiaCloud.Sla.McpWorkshop.sln --nologo
   ```
