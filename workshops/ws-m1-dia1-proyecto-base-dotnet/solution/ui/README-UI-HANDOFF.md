# Guía de Diseño UI y Handoff a .NET 10 (Unidad 1.1)

## Prompt Estructurado de 5 Capas (Pegar en Google Stitch, v0, Lovable, Figma Make o Claude Artifacts)

```text
Actuá como Diseñador Senior de Producto B2B. Necesito diseñar la consola operativa "GuardiaCloud SLA" para ingenieros de guardia.
Restricción técnica obligatoria: Los componentes deben mapear exactamente a este contrato DTO de nuestro backend .NET 10 Minimal API (IncidentSlaCardDto):
- incidentId (string, ej. "INC-2026-1001")
- clientTier (enum: "Platinum" | "Gold" | "Silver")
- severity (enum: "P1" | "P2" | "P3")
- consumedRatio (double entre 0.0 y 1.5)
- isBreached (bool)
- deadlineUtc (ISO-8601 UTC timestamp)
- pauseWindows (array de { reason: "WaitingForCustomer" | "MaintenanceWindow", startsAtUtc, endsAtUtc })

Generá 3 vistas conectadas:
1. Tablero Principal de Guardia SLA con filtro por severity y barra de progreso (verde <0.80, ámbar >=0.80, rojo si isBreached == true).
2. Modal "Registrar Ventana de Pausa" con selector de reason y aviso visible cuando severity == "P1": "En incidentes P1 la pausa máxima acumulada es de 30 minutos".
3. Timeline de Auditoría de SLA + Banner de error estandarizado para respuestas HTTP 4xx en formato ProblemDetails RFC 9457 (mostrando title, detail, errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED" y traceId).
```
