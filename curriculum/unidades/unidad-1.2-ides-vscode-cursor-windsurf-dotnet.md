# Guía Paso a Paso del Alumno — Unidad 1.2: Herramientas de Desarrollo (VS Code, Cursor y Windsurf) en .NET 10

> **Módulo 1 · Unidad 1.2 (4 hs: 1h 30m encuadre + 2h 30m Workshop Práctico)**  
> **IDEs estándar (`D-024`):** **VS Code (con GitHub Copilot), Cursor y Windsurf** *(o tu IDE habitual)*  
> **Repositorio base:** `GuardiaCloud.Sla.sln` (`.NET 10`)

---

## 1. Configuración Inicial de Reglas del Workspace (15 min)

Antes de ejecutar los 5 flujos prácticos, verificá que tu repositorio tenga configuradas las instrucciones de arquitectura en la raíz (`AGENTS.md` y `.github/copilot-instructions.md` o `.cursor/rules/dotnet10.mdc` / `.windsurfrules`):

```markdown
# Reglas de Ingeniería .NET 10 — GuardiaCloud.Sla
- Target Framework: `net10.0`, `LangVersion` C# 13, `Nullable=enable`, `TreatWarningsAsErrors=true`.
- Prohibido usar `DateTime.Now` o `DateTime.UtcNow` directamente en lógica de negocio; inyectá siempre `System.TimeProvider`.
- Todo endpoint ASP.NET Core Minimal API debe recibir `CancellationToken` y devolver `TypedResults.Problem` (RFC 9457) ante errores 4xx/5xx.
- Después de cualquier cambio en archivos `.cs`, ejecutá `dotnet test` para validar que no haya regresiones.
```

---

## 2. Los 5 Flujos Diarios de Ingeniería sobre Código .NET Legado (150 min)

### Flujo 1 (25 min) — Comprensión y Arqueología de Código Legado
1. Usá `@workspace` / `#codebase` en VS Code, Cursor o Windsurf para trazar el camino completo desde el endpoint HTTP en `Program.cs` hasta `SlaCalculator.cs`.
2. Pedile al asistente que identifique:
   - Qué método calcula el vencimiento del SLA.
   - Qué comentario del código contradice el comportamiento real del método (trampa de documentación obsoleta).
3. Verificá cada línea citada abriendo el archivo C# correspondiente.

### Flujo 2 (30 min) — Refactoring Seguro a C# 13
1. Seleccioná la lógica condicional de ventanas de SLA por severidad (`P1`, `P2`, `P3`).
2. Usá *Inline Edit* (`Cmd+I` / `Ctrl+I`) para transformarla en una *switch expression* pura y exhaustiva de C# 13.
3. Ejecutá `dotnet test` inmediatamente para confirmar que el refactoring preserva el comportamiento.

### Flujo 3 (35 min) — Generación de Tests de Casos Borde con `FakeTimeProvider`
1. Evitá pedir *"escribí tests para SlaCalculator"* sin contexto (eso genera tests tautológicos).
2. Pedile al agente una suite `[Theory]` en xUnit usando `FakeTimeProvider` que pruebe explícitamente:
   - Exactamente el minuto límite (`60.0` min en P1).
   - `60.1` min (incumplimiento por 6 segundos).
   - Cruce de medianoche UTC.
   - Un incidente **ya cerrado** (`ResolvedAtUtc != null`) consultado 8 horas más tarde.

### Flujo 4 (30 min) — Debugging Asistido del Bug `ResolvedAtUtc`
1. Al correr `dotnet test`, el cuarto caso del Flujo 3 falla porque `SlaCalculator` seguía comparando contra `nowUtc` aun cuando el incidente ya estaba resuelto.
2. Pegá el fallo de `dotnet test` en el chat del IDE, pedile la causa raíz y aplicá la corrección mínima:
   ```csharp
   var effectiveEndUtc = incident.ResolvedAtUtc ?? nowUtc;
   ```
3. Volvé a correr `dotnet test` y verificá que todos los casos pasen en verde.

### Flujo 5 (30 min) — Code Review Asistido de Seguridad y Performance
Auditar el diff de ejemplo buscando y corrigiendo los **4 defectos clásicos de código generado sin supervisión**:
1. Credencial hardcodeada en configuración $\rightarrow$ mover a variables de entorno / `UserSecrets`.
2. Falta de `CancellationToken` en endpoint asíncrono $\rightarrow$ propagar `CancellationToken ct`.
3. Consulta `N+1` al iterar colecciones $\rightarrow$ proyectar en una sola consulta o diccionario indexado.
4. Excepción cruda 500 ante input inválido $\rightarrow$ devolver `ProblemDetails` RFC 9457 (`400 Bad Request`).
