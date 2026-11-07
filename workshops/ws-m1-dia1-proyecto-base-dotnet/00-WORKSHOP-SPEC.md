# Especificación de Workshop — Día 1 (Unidades 1.1 y 1.2)
## Proyecto Base `GuardiaCloud.Sla`: Diseño UI con IA, Handoff a .NET 10 y los 5 Flujos Diarios en VS Code, Cursor y Windsurf

- **Unidades cubiertas:**
  - **Unidad 1.1 (4 hs — Bloque Mañana):** Diseño de Producto e Interfaces con IA (`Google Stitch`, `v0`, `Lovable`, `Figma Make`, `Claude Artifacts`), extracción de `ui/design-tokens.json` y Handoff tipado hacia `.NET 10` (`IncidentSlaCardDto` + `SlaStatusCard.razor`).
  - **Unidad 1.2 (4 hs — Bloque Tarde):** Configuración profesional del IDE (**VS Code con GitHub Copilot, Cursor y Windsurf**), reglas unificadas de repositorio (`AGENTS.md`, `.github/copilot-instructions.md`, `.cursor/rules/dotnet10.mdc`, `.windsurfrules`) y ejecución de los **5 flujos diarios de ingeniería** sobre código C# brownfield.
- **Stack técnico:** `.NET 10` (`net10.0`, C# 13, ASP.NET Core Minimal APIs, `ProblemDetails` RFC 9457, `System.TimeProvider`, xUnit, `WebApplicationFactory<Program>`).

---

## Estructura del Paquete (`ws-m1-dia1-proyecto-base-dotnet`)

```text
ws-m1-dia1-proyecto-base-dotnet/
├── 00-WORKSHOP-SPEC.md                  # Esta especificación y mapa de correspondencia con los slides
├── 01-GUIA-PASO-A-PASO.md               # Guía práctica paso a paso para los alumnos (U1.1 + U1.2)
├── 02-GUIA-FACILITADOR-Y-SOLUCIONES.md  # Guion docente, trampas sembradas y soluciones esperadas
├── starter/                             # Repositorio semilla inicial (Minuto 0 del Día 1 · 2/2 tests en verde)
│   ├── GuardiaCloud.Sla.sln
│   ├── AGENTS.md                        # Plantilla inicial de reglas del workspace
│   ├── .github/copilot-instructions.md  # Reglas para VS Code + GitHub Copilot
│   ├── .cursor/rules/dotnet10.mdc       # Reglas para Cursor
│   ├── .windsurfrules                   # Reglas para Windsurf
│   ├── ui/
│   │   ├── README-UI-HANDOFF.md         # Prompt de 5 capas y guía de handoff (Unidad 1.1)
│   │   ├── design-tokens.starter.json   # Esqueleto de tokens para completar en Unidad 1.1
│   │   └── Components/
│   │       └── SlaStatusCard.razor      # Esqueleto Blazor para conectar al DTO C#
│   ├── src/GuardiaCloud.Sla.Api/
│   │   ├── Program.cs                   # Endpoints Minimal API de GuardiaCloud.Sla
│   │   ├── Domain/IncidentModels.cs     # Entidades, enums (P1/P2/P3) y DTOs (IncidentSlaCardDto)
│   │   ├── Services/SlaCalculator.cs    # Contiene: comentario engañoso (Flujo 1), if/else legado (Flujo 2) y bug ResolvedAtUtc (Flujo 4)
│   │   └── Endpoints/VibeCodedExportEndpoints.cs # Rama/archivo contaminado con 4 defectos para Code Review (Flujo 5)
│   └── tests/GuardiaCloud.Sla.Tests/
│       └── SlaApiIntegrationTests.cs    # 2 tests base pasando al clonar el repositorio
└── solution/                            # Solución de referencia completa al cierre del Día 1 (10/10 tests en verde)
    ├── GuardiaCloud.Sla.sln
    ├── AGENTS.md                        # Reglas de arquitectura .NET 10 curadas (<55 líneas)
    ├── .github/copilot-instructions.md
    ├── .cursor/rules/dotnet10.mdc
    ├── .windsurfrules
    ├── ui/
    │   ├── design-tokens.json           # Tokens visuales congelados (Unidad 1.1 Paso 2)
    │   ├── prototype-3-screens.html     # Prototipo interactivo de las 3 pantallas + estados de borde
    │   └── Components/
    │       └── SlaStatusCard.razor      # Componente Blazor tipado acoplado a IncidentSlaCardDto
    ├── src/GuardiaCloud.Sla.Api/
    │   ├── Program.cs
    │   ├── Domain/IncidentModels.cs
    │   ├── Services/SlaCalculator.cs    # Refactorizado a C# 13 switch expressions + fix ResolvedAtUtc
    │   └── Endpoints/VibeCodedExportEndpoints.cs # Los 4 defectos de seguridad/performance corregidos
    └── tests/GuardiaCloud.Sla.Tests/
        ├── SlaApiIntegrationTests.cs
        └── SlaCalculatorDay1FlowsTests.cs # Suite completa con FakeTimeProvider para los Flujos 2, 3, 4 y 5
```

---

## Mapa 1:1 entre los Slides del Curso y los Archivos de este Proyecto Base

| Slide (`dia-1-paso-a-paso.pptx` / `00-Modulo-1-Completo.pptx`) | Actividad | Archivo Exacto en este Paquete |
|---|---|---|
| **Slide 3** (Onboarding Minuto 0) | Clonar repo semilla y correr `dotnet test` (`Passed: 2`) | `starter/GuardiaCloud.Sla.sln` + `starter/tests/GuardiaCloud.Sla.Tests/SlaApiIntegrationTests.cs` |
| **Slides 4 y 5** (Unidad 1.1 — Pasos 1 y 2) | Prompt estructurado de 5 capas, 3 pantallas, estados de borde y extracción de tokens | `starter/ui/README-UI-HANDOFF.md`, `solution/ui/prototype-3-screens.html` y `solution/ui/design-tokens.json` |
| **Slide 6** (Unidad 1.1 — Paso 3: Handoff `.NET 10`) | Acoplar la UI al DTO `IncidentSlaCardDto` en `SlaStatusCard.razor` | `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs` y `ui/Components/SlaStatusCard.razor` |
| **Slide 8** (Unidad 1.2 — Reglas del IDE) | Configurar `AGENTS.md`, `.github/copilot-instructions.md`, `.cursor/rules/dotnet10.mdc` y `.windsurfrules` | Archivos homónimos en la raíz de `starter/` y `solution/` |
| **Slide 9** (Unidad 1.2 — Flujos 1 y 2) | **Flujo 1:** Detectar comentario obsoleto engañoso. **Flujo 2:** Refactorizar `if/else` anidados a C# 13 *switch expression* | `src/GuardiaCloud.Sla.Api/Services/SlaCalculator.cs` (`GetTargetResponseWindow`) |
| **Slide 10** (Unidad 1.2 — Flujos 3 y 4) | **Flujo 3:** Tests `[Theory]` de borde con `FakeTimeProvider`. **Flujo 4:** Diagnosticar y reparar bug de `ResolvedAtUtc` | `tests/GuardiaCloud.Sla.Tests/SlaCalculatorDay1FlowsTests.cs` y `Services/SlaCalculator.cs` |
| **Slide 11** (Unidad 1.2 — Flujo 5) | **Flujo 5:** Code Review de seguridad/performance sobre el PR contaminado (`pr/vibe-coded-export`) | `src/GuardiaCloud.Sla.Api/Endpoints/VibeCodedExportEndpoints.cs` |
