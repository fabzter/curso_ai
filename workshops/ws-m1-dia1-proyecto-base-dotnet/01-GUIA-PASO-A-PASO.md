# Guía Paso a Paso del Alumno — Día 1 (Unidades 1.1 y 1.2)
## Proyecto Base `GuardiaCloud.Sla` (.NET 10): Diseño con IA, Handoff y los 5 Flujos Diarios en el IDE

> **Duración total:** 8 horas (Bloque 1 Mañana: Unidad 1.1 = 4 hs · Bloque 2 Tarde: Unidad 1.2 = 4 hs)  
> **IDEs estándar (`D-024`):** **VS Code (con GitHub Copilot), Cursor y Windsurf** *(o tu IDE habitual)*  
> **Carpeta de inicio:** `workshops/ws-m1-dia1-proyecto-base-dotnet/starter/`

---

## Paso 0 (20 min): Verificación del Entorno y Clonado del Proyecto Base

1. Abrí una terminal en la carpeta `starter/` de este workshop y verificá que tenés `.NET 10` instalado y que los 2 tests iniciales pasan en verde:
   ```bash
   cd workshops/ws-m1-dia1-proyecto-base-dotnet/starter
   dotnet --version
   dotnet test GuardiaCloud.Sla.sln
   ```
   **Salida esperada:**
   ```text
   Passed!  - Failed:     0, Passed:     2, Skipped:     0, Total:     2
   ```
2. Abrí la carpeta `starter/` en **VS Code**, **Cursor** o **Windsurf**.

---

# PARTE 1 (Mañana · Unidad 1.1): Diseño de Producto con IA y Handoff a .NET 10 (2h 30m de Práctica)

## Ejercicio 1.1 — Paso 1 (40 min): Generación de las 3 Pantallas desde el Contrato C#

1. Inspeccioná el contrato DTO real en `src/GuardiaCloud.Sla.Api/Domain/IncidentModels.cs` (`IncidentSlaCardDto` y `PauseWindowDto`).
2. Abrí **Google Stitch**, **v0**, **Lovable**, **Figma Make** o **Claude Artifacts** y ejecutá el prompt de 5 capas incluido en `ui/README-UI-HANDOFF.md`:
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

## Ejercicio 1.1 — Paso 2 (35 min): Estados de Borde y Congelamiento de `ui/design-tokens.json`

1. Pedile a la herramienta de diseño que renderice simultáneamente los **3 estados de borde**:
   - **En Riesgo Preventivo (`>= 80%`):** `consumedRatio = 0.84`, `isBreached = false` (borde y alerta ámbar `#D97706`).
   - **Rechazo Regulatorio P1 (`HTTP 422`):** banner RFC 9457 mostrando `errorCode: "SLA-422-P1-PAUSE-CAP-EXCEEDED"`.
   - **Incidente Vencido (`Breached`):** `consumedRatio = 1.18`, `isBreached = true` (borde y badge rojo `#DC2626`).
2. Completá y guardá `ui/design-tokens.json` con la paleta semántica, tipografías y radios de borde para que los agentes de código mantengan consistencia visual. *(Podés comparar contra `solution/ui/design-tokens.json` y abrir `solution/ui/prototype-3-screens.html` en tu navegador).*

## Ejercicio 1.1 — Paso 3 (45 min): Handoff Limpio hacia `.NET 10` (`SlaStatusCard.razor`)

1. Abrí `ui/Components/SlaStatusCard.razor` en VS Code, Cursor o Windsurf.
2. Usá el asistente del IDE para completar el componente Blazor conectándolo estrictamente a las propiedades de `IncidentSlaCardDto` (definido en `Domain/IncidentModels.cs`), incluyendo la alerta preventiva cuando `Item.ConsumedRatio >= 0.80 && !Item.IsBreached`.

---

# PARTE 2 (Tarde · Unidad 1.2): Los 5 Flujos Diarios en VS Code, Cursor y Windsurf sobre Código C# Legado (2h 30m de Práctica)

## Ejercicio Preliminar (15 min): Reglas Unificadas del Workspace

Revisá y completá los archivos de reglas en la raíz de `starter/`:
- `AGENTS.md`
- `.github/copilot-instructions.md` (VS Code + GitHub Copilot)
- `.cursor/rules/dotnet10.mdc` (Cursor)
- `.windsurfrules` (Windsurf)

Asegurate de que prohíban explícitamente `DateTime.Now` / `DateTime.UtcNow` directo en dominio (exigiendo `System.TimeProvider`), exijan `CancellationToken` en endpoints asíncronos, obliguen a devolver `ProblemDetails` RFC 9457 y ordenen correr `dotnet test` tras cada edición.

---

## Flujo 1 (25 min): Comprensión y Arqueología de Código Legado

1. En el chat de tu IDE (`@workspace` en VS Code Copilot, `@Codebase` en Cursor o Cascade en Windsurf), ejecutá:
   ```text
   Trazá el flujo completo desde el endpoint GET /api/incidents/{id}/sla en Program.cs hasta SlaCalculator.Evaluate en Services/SlaCalculator.cs.
   Citá archivo y línea exacta. Además, verificá si existe algún comentario en SlaCalculator.cs que contradiga lo que realmente hace el código C#.
   ```
2. **Meta del ejercicio:** Descubrir que el comentario legado en `SlaCalculator.cs` afirma que *"convierte a GMT-3 y otorga 15 minutos de gracia en P1"*, mientras que el código real opera en UTC y no suma ningún minuto de gracia.

---

## Flujo 2 (30 min): Refactoring Seguro a C# 13 con Red de Pruebas

1. Abrí `src/GuardiaCloud.Sla.Api/Services/SlaCalculator.cs` y localizá el método `GetTargetResponseWindow(SeverityTier tier, ClientTier clientTier)`.
2. Observá que está escrito con condicionales `if / else` anidados y repetitivos.
3. Seleccionalo y usá **Inline Edit (`Cmd+I` / `Ctrl+I`)** para transformarlo en una **switch expression pura y exhaustiva de C# 13** (lanzando `ArgumentOutOfRangeException` ante valores fuera del enum).
4. Corré `dotnet test` para confirmar que no rompiste nada.

---

## Flujo 3 (35 min): Generación de Tests de Casos Borde con `FakeTimeProvider`

1. En `tests/GuardiaCloud.Sla.Tests/`, pedile al agente que cree una clase de pruebas unitarias `SlaCalculatorDay1FlowsTests.cs` usando `FakeTimeProvider` (sin `Thread.Sleep` ni `DateTimeOffset.UtcNow` real).
2. Exigí explícitamente estos **4 casos de borde** para un incidente `CriticalP1` (objetivo = 60 min):
   - **Caso A:** Exactamente en el minuto `60.0` (`ElapsedActiveMinutes == 60`, `IsBreached == false`).
   - **Caso B:** En el minuto `60.1` (`IsBreached == true` por 6 segundos).
   - **Caso C:** Cruce de medianoche UTC (abierto `23:30Z`, evaluado `00:15Z` del día siguiente $\rightarrow$ `45 min`, `IsBreached == false`).
   - **Caso D (Incidente ya cerrado):** Abierto a las `10:00Z`, **resuelto a las `10:45Z`** (`ResolvedAtUtc` seteado), pero consultado en el tablero a las `18:00Z` (8 horas después).

---

## Flujo 4 (30 min): Debugging Asistido del Bug `ResolvedAtUtc`

1. Ejecutá `dotnet test`. Vas a ver que el **Caso D** del Flujo 3 **falla** (`Assert.False(status.IsBreached)` falla porque calcula 480 minutos transcurridos en vez de 45 minutos).
2. Pegá el mensaje de fallo en el chat de tu IDE y pedile la causa raíz en `SlaCalculator.cs`.
3. Aplicá la corrección mínima en `SlaCalculator.Evaluate`:
   ```csharp
   var referenceEndUtc = incident.ResolvedAtUtc ?? timeProvider.GetUtcNow();
   ```
4. Volvé a correr `dotnet test` y confirmá que los 4 casos de borde pasen en verde.

---

## Flujo 5 (30 min): Code Review Asistido de Seguridad y Performance (`VibeCodedExportEndpoints.cs`)

1. Abrí `src/GuardiaCloud.Sla.Api/Endpoints/VibeCodedExportEndpoints.cs` (que simula un Pull Request generado con "vibe coding" sin supervisión).
2. Pedile a tu IDE que haga un **Code Review de Seguridad, Concurrencia y Performance** contra las reglas de `AGENTS.md`.
3. Encontrá y corregí los **4 defectos sembrados**:
   - **Defecto 1 (Seguridad):** Cadena de conexión con `AccountKey` hardcodeada en el código fuente.
   - **Defecto 2 (Asincronía y DoS):** Endpoint asíncrono sin `CancellationToken` ni tope de paginación (`pageSize`).
   - **Defecto 3 (Performance `N+1`):** Bucle `foreach` que ejecuta una consulta/búsqueda separada por cada incidente.
   - **Defecto 4 (Contrato HTTP):** Lanza `throw new Exception(...)` devolviendo HTTP 500 crudo cuando el filtro `priority` es inválido, en lugar de devolver `Results.Problem` (RFC 9457 `400 Bad Request` con `extensions["errorCode"] = "SLA-400-INVALID-EXPORT-FILTER"`).
4. Corré `dotnet test` y verificá que toda la suite quede en verde.
