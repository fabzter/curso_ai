# Catálogo Oficial de Errores RFC 9457 (`ProblemDetails`) — GuardiaCloud.Sla

Todo endpoint HTTP o contrato de validación en el ecosistema **`GuardiaCloud.Sla`** debe devolver errores estructurados según **RFC 9457 (`application/problem+json`)** usando `TypedResults.Problem(...)` o `Results.Problem(...)` en ASP.NET Core Minimal APIs.

## Campos Obligatorios en cada Respuesta de Error
1. `type`: URI estable del catálogo interno (`https://errors.guardiacloud.internal/sla/<codigo-kebab-case>`).
2. `title`: Resumen breve y legible en español rioplatense técnico.
3. `status`: Código HTTP exacto (`400`, `404`, `409`, `422`).
4. `detail`: Explicación accionable con el identificador del recurso afectado.
5. `extensions["errorCode"]`: Código canónico en mayúsculas (ver tabla inferior).
6. `extensions["traceId"]` (o `HttpContext.TraceIdentifier`): Identificador de correlación para Azure Application Insights.

## Tabla Canónica de Códigos (`errorCode`)

| `errorCode` | HTTP `status` | `type` URI | Cuándo se dispara |
|---|---:|---|---|
| `SLA-400-INVALID-CLIENT-TIER` | `400` | `https://errors.guardiacloud.internal/sla/invalid-client-tier` | El `clientTier` no pertenece a `{Bancario-Tier1, Aseguradora-Gold, Retail-Standard}`. |
| `SLA-400-INVALID-SEVERITY` | `400` | `https://errors.guardiacloud.internal/sla/invalid-severity` | La severidad no pertenece a `{P1, P2, P3}`. |
| `SLA-404-INCIDENT-NOT-FOUND` | `404` | `https://errors.guardiacloud.internal/sla/incident-not-found` | El `incidentId` consultado no existe en el almacén operativo. |
| `SLA-409-PAUSE-CONFLICT` | `409` | `https://errors.guardiacloud.internal/sla/pause-conflict` | Se intenta pausar un incidente ya pausado/resuelto, o reanudar uno sin pausa activa. |
| `SLA-422-P1-PAUSE-BUDGET-EXCEEDED` | `422` | `https://errors.guardiacloud.internal/sla/p1-pause-budget-exceeded` | Una pausa en incidente `P1` supera los 30 minutos acumulados sin `SupervisorOverrideCode` válido. |

## Antipatrón Prohibido en Code Reviews

```csharp
// ❌ PROHIBIDO: JSON ad-hoc sin RFC 9457 ni extensions["errorCode"]
return Results.BadRequest(new { error = "Severidad inválida" });
```

## Patrón Aprobado en GuardiaCloud (.NET 10)

```csharp
// ✅ CORRECTO: ProblemDetails RFC 9457 con errorCode tipado
return Results.Problem(
    title: "Severidad de incidente inválida",
    detail: $"La severidad '{severity}' no es válida. Valores permitidos: P1, P2, P3.",
    statusCode: StatusCodes.Status400BadRequest,
    type: "https://errors.guardiacloud.internal/sla/invalid-severity",
    extensions: new Dictionary<string, object?>
    {
        ["errorCode"] = "SLA-400-INVALID-SEVERITY"
    });
```
