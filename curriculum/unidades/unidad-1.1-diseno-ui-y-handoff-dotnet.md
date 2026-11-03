# Guía Paso a Paso del Alumno — Unidad 1.1: Diseño de Producto e Interfaces con IA + Handoff a .NET 10

> **Módulo 1 · Unidad 1.1 (4 hs: 1h 30m encuadre + 2h 30m Workshop Práctico)**  
> **Herramientas:** Google Stitch (`stitch.withgoogle.com`), v0 (`v0.dev`), Lovable, Figma Make o Claude Artifacts + **VS Code / Cursor / Windsurf**  
> **Repositorio base:** `GuardiaCloud.Sla.sln` (`.NET 10`)

---

## 1. Objetivo del Taller
Diseñar un flujo interactivo de **3 pantallas** para la consola operativa **GuardiaCloud SLA**, extraer sus tokens visuales en un archivo estructurado (`ui/design-tokens.json`) y ejecutar el **Handoff técnico hacia `.NET 10`** sin inventar propiedades fuera del contrato DTO del backend.

---

## 2. Paso 1 (40 min): Generación de las 3 Pantallas Nucleares desde el Contrato C#

Abrí tu herramienta de diseño con IA y usá este prompt estructurado (acoplado exactamente al DTO de `GuardiaCloud.Sla.Api`):

```text
Actuá como Diseñador Senior de Producto B2B. Necesito diseñar la consola operativa "GuardiaCloud SLA" para ingenieros de guardia.
Restricción técnica obligatoria: Los componentes deben mapear exactamente a este contrato DTO de nuestro backend .NET 10 Minimal API:
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
3. Timeline de Auditoría de SLA + Banner de error estandarizado para respuestas HTTP 4xx en formato ProblemDetails RFC 9457 (mostrando title, detail, errorCode y traceId).
```

---

## 3. Paso 2 (35 min): Iteración de Estados de Borde y Extracción de `design-tokens.json`

1. Pedile a la herramienta que muestre explícitamente estos **3 estados de borde** sin cambiar la estructura del layout:
   - **Estado 1 (En riesgo):** `consumedRatio = 0.84`, `isBreached = false` (debe activar la alerta preventiva ámbar).
   - **Estado 2 (Rechazo regulatorio P1 — HTTP 422):** banner mostrando `errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED"`.
   - **Estado 3 (Sin pausas vs. múltiples pausas solapadas):** visualización clara del tiempo neto computable.
2. Exportá la paleta, tipografía y espaciados a `ui/design-tokens.json`:

```json
{
  "colors": {
    "surfacePrimary": "#0F172A",
    "surfaceCard": "#FFFFFF",
    "statusHealthy": "#0D9488",
    "statusWarning80": "#D97706",
    "statusBreached": "#DC2626"
  },
  "typography": {
    "fontFamilySans": "Inter, system-ui, sans-serif",
    "fontFamilyMono": "JetBrains Mono, Consolas, monospace"
  },
  "spacing": {
    "cardPadding": "16px",
    "borderRadius": "8px"
  }
}
```

---

## 4. Paso 3 (45 min): Handoff hacia `.NET 10` en VS Code, Cursor o Windsurf

Abrí el repositorio en **VS Code, Cursor o Windsurf** y usá el agente del IDE para convertir el marcado generado en un componente tipado (por ejemplo, `SlaStatusCard.razor` o el cliente tipado acoplado a `GuardiaCloud.Sla.Api`):

```razor
@* ui/Components/SlaStatusCard.razor *@
<article class="sla-card @(Item.IsBreached ? "sla-breached" : Item.ConsumedRatio >= 0.80 ? "sla-warning" : "sla-ok")">
    <header class="sla-header">
        <span class="badge-severity">@Item.Severity</span>
        <span class="badge-tier">@Item.ClientTier</span>
        <code>@Item.IncidentId</code>
    </header>

    <div class="sla-progress">
        <progress value="@Math.Min(Item.ConsumedRatio, 1.0)" max="1.0"></progress>
        <span>@($"{Item.ConsumedRatio:P0}") consumido</span>
    </div>

    @if (Item.ConsumedRatio >= 0.80 && !Item.IsBreached)
    {
        <p role="alert" class="alert-amber">
            Atención: SLA al >= 80%. Requiere escalamiento proactivo.
        </p>
    }
</article>

@code {
    [Parameter, EditorRequired]
    public required IncidentSlaCardDto Item { get; set; }
}
```

---

## 5. Paso 4 (30 min): Checklist de Verificación entre Pares

- [ ] Las 3 pantallas usan **únicamente** propiedades existentes en el DTO C# (cero campos inventados).
- [ ] `ui/design-tokens.json` está versionado en el repositorio.
- [ ] El estado de error muestra `errorCode` y `traceId` según RFC 9457 (`ProblemDetails`).
