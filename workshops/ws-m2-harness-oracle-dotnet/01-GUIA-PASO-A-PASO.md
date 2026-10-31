# Guía Práctica Paso a Paso: Harness Engineering, Oráculos con `NetArchTest` y Laboratorio HITL vs. Full AI (`git worktrees`)

> **Duración:** 3 hs 45 min · **Modalidad:** En duplas · **Unidades 1.4 + 2.3**

En este laboratorio vas a transformar un repositorio `.NET 10` vulnerable a *"workslop"* en un entorno de ingeniería blindado con un **Harness interoperable** (Unidad 1.4) y un **Oráculo de Verificación Determinista** (Unidad 2.3), para después poner a prueba dos modos de trabajo en paralelo: **Human-in-the-Loop (HITL)** frente a **Full AI Autónomo en `git worktrees`**.

---

## Fase 0 — Diagnóstico del Repositorio Inicial (15 min)

### Paso 0.1: Ejecutá los tests base y el hook del Harness
Entrá en tu copia de trabajo de `starter/` y corré primero `dotnet test` y luego `./scripts/post-edit-dotnet-hook.sh`:

```bash
cd workshops/ws-m2-harness-oracle-dotnet/starter
dotnet test GuardiaCloud.Sla.HarnessLab.sln --nologo
./scripts/post-edit-dotnet-hook.sh
```

Vas a notar una paradoja muy común en proyectos reales:
1. `dotnet test` dice **`Passed: 2, Failed: 0`**, dando una falsa sensación de seguridad.
2. Pero `./scripts/post-edit-dotnet-hook.sh` **falla inmediatamente** porque falta `CLAUDE.md` y porque [`AGENTS.md`](starter/AGENTS.md) contiene un borrador autogenerado inútil.
3. Peor aún: si abrís [`src/GuardiaCloud.Sla.Api/Domain/LegacyVibeCodedHelper.cs`](starter/src/GuardiaCloud.Sla.Api/Domain/LegacyVibeCodedHelper.cs), vas a encontrar una clase en la capa `Domain` que referencia directamente `GuardiaCloud.Sla.Api.Infrastructure.InMemoryIncidentStore`, no es `sealed` y usa `DateTimeOffset.UtcNow`. Los tests actuales ni siquiera se enteran.

---

## Fase 1 — Unidad 1.4: Ingeniería de Harness (`AGENTS.md`, `CLAUDE.md`, Hooks y Subagentes) (50 min)

### ¿Por qué el `AGENTS.md` de `starter/` es un antipatrón?
El estudio empírico de ETH Zurich (`arXiv:2602.11988`, feb. 2026) demostró que los archivos `AGENTS.md` / `CLAUDE.md` generados automáticamente con obviedades del lenguaje (*"use async/await, follow SOLID, write clean code"*) **reducen la tasa de éxito de los agentes entre 0,5% y 2% e inflan el costo de tokens entre 20% y 23%**, mientras que un archivo breve curado por humanos con comandos exactos e invariantes no obvias **mejora el éxito en +4%**.

### Paso 1.1: Reescribí `AGENTS.md` (<100 líneas) y creá el puente `CLAUDE.md`
1. Reemplazá el contenido de `AGENTS.md` por una guía curada de menos de 60 líneas que incluya únicamente:
   - Propósito del microservicio `GuardiaCloud.Sla.HarnessLab`.
   - Los 4 comandos exactos de verificación (incluyendo los filtros `--filter FullyQualifiedName~ArchitectureOracleTests` y `--filter FullyQualifiedName~SlaHarnessEndpointsTests`).
   - Las 4 invariantes arquitectónicas no obvias:
     1. `GuardiaCloud.Sla.Api.Domain` no puede depender de `Infrastructure` ni de `Microsoft.AspNetCore.Http`.
     2. Toda clase en `Domain` debe ser `sealed` (o `static`).
     3. Prohibido usar `DateTime.UtcNow` / `DateTimeOffset.UtcNow` en `Domain`; inyectar siempre `System.TimeProvider`.
     4. Todo error HTTP debe usar `Results.Problem(...)` (RFC 9457) con `extensions["errorCode"]`.
2. Creá `CLAUDE.md` en la raíz con una única línea para garantizar interoperabilidad entre Codex/Copilot/Cursor (que leen `AGENTS.md`) y Claude Code (que lee `CLAUDE.md`):
   ```markdown
   @AGENTS.md
   ```

### Paso 1.2: Activá el hook `PostToolUse` y el subagente revisor
1. Copiá `.claude/settings.json.example` a `.claude/settings.json`:
   ```bash
   cp .claude/settings.json.example .claude/settings.json
   ```
   A partir de este momento, cada vez que Claude Code edite un archivo (`Edit|Write|MultiEdit`), ejecutará automáticamente `./scripts/post-edit-dotnet-hook.sh`.
2. Completá [`.claude/agents/dotnet-arch-reviewer.md`](starter/.claude/agents/dotnet-arch-reviewer.md) definiendo el checklist de 4 puntos para auditar aislamiento de `Domain`, clases `sealed`, `ProblemDetails` RFC 9457 y corrida del hook.

Corré `./scripts/post-edit-dotnet-hook.sh` y verificá que el **Paso 1/3** ahora pasa en verde.

---

## Fase 2 — Unidad 2.3A: Construcción del Oráculo de Arquitectura con `NetArchTest.Rules` (50 min)

Un agente autónomo no puede respetar fronteras arquitectónicas que no estén expresadas como código ejecutable. Vamos a convertir nuestras reglas de `AGENTS.md` en un **oráculo determinista** usando **`NetArchTest.Rules` (`v1.3.2`)**.

### Paso 2.1: Escribí las 2 reglas de arquitectura en `ArchitectureOracleTests.cs`
Abrí [`tests/GuardiaCloud.Sla.Tests/ArchitectureOracleTests.cs`](starter/tests/GuardiaCloud.Sla.Tests/ArchitectureOracleTests.cs) y agregá los dos tests marcados en el `TODO`:

```csharp
[Fact]
public void Domain_Should_Not_Depend_On_Infrastructure_Or_AspNetCoreHttp()
{
    var result = Types.InAssembly(typeof(SlaRuleEngine).Assembly)
        .That()
        .ResideInNamespace("GuardiaCloud.Sla.Api.Domain")
        .ShouldNot()
        .HaveDependencyOnAny(
            "GuardiaCloud.Sla.Api.Infrastructure",
            "Microsoft.AspNetCore.Http")
        .GetResult();

    Assert.True(
        result.IsSuccessful,
        $"Violación de arquitectura limpia en Domain: {string.Join(", ", result.FailingTypeNames ?? [])}");
}

[Fact]
public void Domain_Classes_Should_Be_Sealed()
{
    var result = Types.InAssembly(typeof(SlaRuleEngine).Assembly)
        .That()
        .ResideInNamespace("GuardiaCloud.Sla.Api.Domain")
        .And()
        .AreClasses()
        .Should()
        .BeSealed()
        .GetResult();

    Assert.True(
        result.IsSuccessful,
        $"Las siguientes clases de Domain no son sealed: {string.Join(", ", result.FailingTypeNames ?? [])}");
}
```

### Paso 2.2: Ejecutá el Oráculo, observá cómo atrapa a `LegacyVibeCodedHelper` y reparalo
Corré en tu terminal:

```bash
dotnet test GuardiaCloud.Sla.HarnessLab.sln --filter FullyQualifiedName~ArchitectureOracleTests --nologo
```

Vas a ver que **ambos tests nuevos fallan** reportando exactamente el culpable:
`GuardiaCloud.Sla.Api.Domain.LegacyVibeCodedHelper`.

Eliminá `src/GuardiaCloud.Sla.Api/Domain/LegacyVibeCodedHelper.cs` y volvé a correr `./scripts/post-edit-dotnet-hook.sh`. Ahora los **3 tests de arquitectura (`NetArchTest`)** pasan en verde en menos de 200 ms. ¡Tu red de contención arquitectónica ya está activa!

---

## Fase 3 — Unidad 2.3B: Laboratorio Comparado HITL vs. Full AI en `git worktrees` (80 min)

Ahora tenés dos requerimientos nuevos para entregar en este sprint sobre `GuardiaCloud.Sla.Api`:

| Tarea | Endpoint | Nivel de Riesgo | Modo Asignado |
|---|---|---|---|
| **Tarea A** | `POST /api/sla/credits/calculate` | **Alto (Financiero):** Calcula bonificaciones en USD sobre la factura mensual (`P1=10%`, `P2=5%`, `P3=2%`), aplica tope contractual (`30%` en `Bancario-Tier1`, `20%` en el resto) con redondeo bancario `MidpointRounding.ToEven` y errores RFC 9457 (`SLA-400-INVALID-INVOICE-AMOUNT`, `SLA-400-INVALID-CLIENT-TIER`, `SLA-404-INCIDENT-NOT-FOUND`). | **Human-in-the-Loop (HITL)** (Plan Mode + co-diseño paso a paso). |
| **Tarea B** | `GET /api/sla/incidents/export-summary` | **Bajo (Lectura Operativa):** Devuelve `ShiftExportSummaryDto` con fecha de corte vía `TimeProvider`, total de incidentes, abiertos, vencidos y conteo por severidad (`P1`, `P2`, `P3`). | **Full AI Autónomo** en un `git worktree` paralelo con test-first oracle. |

### Paso 3.1: Prepará el Oráculo de Integración antes de delegar (TDD Agéntico)
En [`tests/GuardiaCloud.Sla.Tests/SlaHarnessEndpointsTests.cs`](starter/tests/GuardiaCloud.Sla.Tests/SlaHarnessEndpointsTests.cs), configurá un `FixedTimeProvider(2026-10-30T14:00:00Z)` en `WebApplicationFactory<Program>` y agregá los 3 tests de contrato que actuarán como oráculo de aceptación:
1. `CalculateCredits_AppliesTier1CapAtThirtyPercent` (verifica que 35% bruto sobre USD 10.000 se topea en USD 3.000 para `Bancario-Tier1`).
2. `CalculateCredits_ReturnsRfc9457ProblemDetailsOnNegativeInvoice` (verifica HTTP 400 + `errorCode = "SLA-400-INVALID-INVOICE-AMOUNT"`).
3. `ExportSummary_ReturnsDeterministicCountsBySeverity` (verifica los totales del resumen de guardia).

### Paso 3.2: Ejecutá la Tarea A en modo Human-in-the-Loop (HITL)
En tu directorio principal (integrante 1 de la dupla):
1. Iniciá tu agente en **Plan Mode** (`/plan` en Claude Code) pidiendo diseñar `SlaRuleEngine.CalculateMonthlyCredit` y el endpoint `POST /api/sla/credits/calculate`.
2. Revisá que el plan contemple explícitamente `MidpointRounding.ToEven`, la validación de `MonthlyInvoiceUsd <= 0` y la verificación de que todos los `IncidentIds` existan antes de liquidar.
3. Aprobá el plan paso a paso y verificá con:
   ```bash
   dotnet test --filter FullyQualifiedName~CalculateCredits
   ```

### Paso 3.3: Ejecutá la Tarea B en paralelo en modo Full AI Autónomo (`git worktree`)
Para ejecutar un segundo agente en paralelo sin que pise los archivos que estás editando en la Tarea A, creá un `git worktree` aislado (o una copia aislada de trabajo si estás fuera de una rama dedicada):

```bash
# Desde un repositorio git con commit limpio:
git worktree add ../worktree-full-ai -b feat/shift-export-summary
```

En la terminal de `../worktree-full-ai` (integrante 2 de la dupla), dale al agente una única instrucción autónoma cerrada por el oráculo:

> *"Implementá `SlaRuleEngine.BuildShiftExportSummary` y el endpoint `GET /api/sla/incidents/export-summary` siguiendo las invariantes de `AGENTS.md`. No te detengas hasta que `./scripts/post-edit-dotnet-hook.sh` y el test `ExportSummary_ReturnsDeterministicCountsBySeverity` pasen en verde."*

Observá cómo el agente itera solo contra el compilador y el hook sin intervención humana.

### Paso 3.4: Integración y verificación completa
Integrá los cambios de ambas tareas y ejecutá el hook completo:

```bash
./scripts/post-edit-dotnet-hook.sh
```

Resultado esperado: **Build succeeded (0 Warnings, 0 Errors)** y **7/7 tests en verde** (3 de `NetArchTest` + 4 de `WebApplicationFactory`).

---

## Fase 4 — Auditoría con Subagente y Debrief Comparativo (30 min)

1. Invocá al subagente `dotnet-arch-reviewer` para que audite el diff final contra las 4 reglas de arquitectura.
2. Completá tu cuadro comparativo en `comparativa-hitl-vs-full-ai.md` registrando para Tarea A (HITL) vs. Tarea B (Full AI):
   - Tiempo de preparación del oráculo vs. tiempo de generación vs. tiempo de revisión humana.
   - Cuántas veces el hook o `NetArchTest` frenaron un desvío del agente.
   - Qué hubiera pasado si delegabas la Tarea A (regla financiera con topes y redondeo bancario) en Full AI sin revisar los casos borde.
