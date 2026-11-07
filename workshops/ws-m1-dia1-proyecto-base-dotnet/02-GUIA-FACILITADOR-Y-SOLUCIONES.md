# Guía del Facilitador y Soluciones — Día 1 (Unidades 1.1 y 1.2)
## Proyecto Base `GuardiaCloud.Sla` (.NET 10)

---

## 1. Propósito Pedagógico de este Paquete Base

Este paquete (`ws-m1-dia1-proyecto-base-dotnet`) es el **Proyecto Base Semilla (`GuardiaCloud.Sla.sln`)** con el que arranca el curso en el Minuto 0 del Día 1 y sobre el cual se apoyan todos los slides de las **Unidades 1.1 y 1.2**.

Contiene tanto el estado inicial (`starter/`) con las trampas didácticas sembradas como la solución completa (`solution/`) lista para proyectar o comparar.

---

## 2. Verificación Rápida para el Instructor (Antes de Iniciar la Clase)

```bash
# 1. Verificar que starter/ compila y pasa sus 2 tests base:
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/starter/GuardiaCloud.Sla.sln
# -> Passed! - Failed: 0, Passed: 2, Total: 2

# 2. Verificar que solution/ compila con TreatWarningsAsErrors=true y pasa los 10 tests del Día 1:
dotnet test workshops/ws-m1-dia1-proyecto-base-dotnet/solution/GuardiaCloud.Sla.sln
# -> Passed! - Failed: 0, Passed: 10, Total: 10
```

---

## 3. Mapa de las Trampas Didácticas Sembradas en `starter/` (Unidad 1.2)

| Flujo de Unidad 1.2 | Archivo en `starter/` | Qué está sembrado | Qué debe hacer el alumno (`solution/`) |
|---|---|---|---|
| **Flujo 1: Arqueología de Legado** | `src/GuardiaCloud.Sla.Api/Services/SlaCalculator.cs` | Comentario engañoso: `// NOTA HISTÓRICA (2023): Convierte automáticamente a GMT-3 y suma 15 min de gracia en P1.` | Detectar con `@workspace` / `#codebase` que el comentario miente (el código usa UTC puro y no otorga gracia) y limpiarlo. |
| **Flujo 2: Refactoring C# 13** | `src/GuardiaCloud.Sla.Api/Services/SlaCalculator.cs` (`GetTargetResponseWindow`) | Método de 35 líneas con `if / else` anidados por severidad (`P1`, `P2`, `P3`) y tier (`Platinum`, `Gold`, `Silver`). | Refactorizar con Inline Edit a una *switch expression* de tuplas exhaustiva de C# 13 manteniendo `dotnet test` en verde. |
| **Flujo 3: Tests con `FakeTimeProvider`** | `tests/GuardiaCloud.Sla.Tests/` | Solo hay 2 tests de camino feliz. | Agregar tests parametrizados `[Theory]` y `[Fact]` con `FakeTimeProvider` (minuto 60.0, minuto 60.1, medianoche UTC e incidente resuelto). |
| **Flujo 4: Debugging `ResolvedAtUtc`** | `src/GuardiaCloud.Sla.Api/Services/SlaCalculator.cs` (`Evaluate`) | Usa `var referenceEndUtc = timeProvider.GetUtcNow();` ignorando `incident.ResolvedAtUtc`. | Diagnosticar el fallo del test de incidente cerrado y aplicar `var referenceEndUtc = incident.ResolvedAtUtc ?? timeProvider.GetUtcNow();`. |
| **Flujo 5: Code Review PR Contaminado** | `src/GuardiaCloud.Sla.Api/Endpoints/VibeCodedExportEndpoints.cs` | 4 defectos clásicos: (1) Secreto de Azure hardcodeado, (2) Falta de `CancellationToken` y paginación, (3) Consulta `N+1` en bucle, (4) `throw new Exception` (HTTP 500) en lugar de `ProblemDetails` RFC 9457. | Auditar con el IDE, corregir los 4 defectos y devolver HTTP 400 con `errorCode = "SLA-400-INVALID-EXPORT-FILTER"`. |
