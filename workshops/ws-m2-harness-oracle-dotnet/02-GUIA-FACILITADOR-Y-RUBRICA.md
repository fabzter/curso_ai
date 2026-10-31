# Guía del Facilitador y Rúbrica de Evaluación (`ws-m2-harness-oracle-dotnet`)

- **Unidades cubiertas:** **Unidad 1.4** (*Harness Engineering: Claude Code, Codex y Devin*) + **Unidad 2.3** (*Modos de Implementación: Full AI vs. Human-in-the-Loop*)
- **Duración total:** 225 minutos (3 hs 45 min)
- **Evaluación:** Rúbrica sobre 100 puntos (parte de las Prácticas Guiadas Evaluables y habilitante directo del Proyecto Integrador del Módulo 3).

---

## 1. Notas de Facilitación y Puntos Clave de Enseñanza

### Minuto 0:00 – 0:15 (Fase 0: La ilusión de los "Tests en Verde" sin Oráculo de Arquitectura)
- **Momento "¡Ajá!" del inicio:** Cuando las duplas corren `dotnet test` sobre `starter/`, ven `Passed: 2, Failed: 0`. Inmediatamente pediles que abran `src/GuardiaCloud.Sla.Api/Domain/LegacyVibeCodedHelper.cs`.
- **Pregunta disparadora:** *"Si un agente autónomo corre en CI o en background y su única condición de éxito es `dotnet test`, ¿quién le impide meter un `using GuardiaCloud.Sla.Api.Infrastructure;` adentro de `Domain` o llamar a `DateTimeOffset.UtcNow`?"*
- **Lección central:** Las pruebas funcionales de camino feliz **no alcanzan** como oráculo para agentes autónomos. Sin **fitness functions arquitectónicas (`NetArchTest.Rules`)** y sin un **hook de ciclo de vida (`PostToolUse`)**, el modo Full AI acumula deuda técnica silenciosa a velocidad de máquina.

### Minuto 0:15 – 1:05 (Fase 1: El estudio de ETH Zurich y la dieta de `AGENTS.md`)
- **Dato empírico clave para citar en pizarrón:** Gloaguen et al. (ETH Zurich, `arXiv:2602.11988`, feb. 2026) midieron que los archivos `AGENTS.md` / `CLAUDE.md` autogenerados por LLMs (como el comando `/init` sin curación) **bajan la tasa de resolución entre 0,5% y 2% y suben el costo en tokens entre 20% y 23%**, mientras que los archivos breves escritos por ingenieros humanos con comandos exactos de build/test y reglas no obvias **suben el éxito +4%**.
- **Regla práctica para la consultora:** Si una regla ya la sabe cualquier modelo entrenado en C# (*"usá async/await, seguí PascalCase"*), **borrala de `AGENTS.md`**. Dejá solo lo específico de este repositorio (`--filter FullyQualifiedName~...`, invariantes de `NetArchTest`, catálogo RFC 9457) y mantenelo por debajo de 100 líneas (idealmente 40–60 líneas).
- **El puente `@AGENTS.md`:** Recordá mostrar en vivo que Codex, GitHub Copilot y Cursor leen `AGENTS.md` de forma nativa, pero **Claude Code (`v2.1+`) exige `CLAUDE.md`** (`anthropics/claude-code#34235`). Una sola línea `@AGENTS.md` dentro de `CLAUDE.md` elimina la duplicación en equipos mixtos.

### Minuto 1:05 – 1:55 (Fase 2: `NetArchTest.Rules` como Oráculo Determinista)
- Verificá que las duplas corran `dotnet test` **antes** de borrar `LegacyVibeCodedHelper.cs` para que experimenten en primera persona cómo `NetArchTest` falla e imprime el nombre exacto de la clase infractora (`GuardiaCloud.Sla.Api.Domain.LegacyVibeCodedHelper`).

### Minuto 1:55 – 3:15 (Fase 3: HITL vs. Full AI y la trampa de los conflictos de merge)
- **Conexión con la Unidad 2.2 (AgenticFlict — 27,67% de conflictos de merge en PRs agénticos):**
  - En este laboratorio, tanto la Tarea A (HITL) como la Tarea B (Full AI en `git worktree`) tocan `SlaRuleEngine.cs` y `Program.cs`.
  - Mostrales cómo aislar dónde agrega métodos cada tarea (o separar endpoints en archivos de extensión por *Vertical Slice*) evita que dos agentes corriendo en paralelo en distintos `git worktrees` generen conflictos de merge al integrar.

---

## 2. Solución de Problemas Frecuentes (Troubleshooting)

| Síntoma | Causa raíz | Solución rápida |
|---|---|---|
| `./scripts/post-edit-dotnet-hook.sh` dice `AGENTS.md tiene >100 líneas` | El participante dejó texto del borrador viejo o pegó documentación extensa en `AGENTS.md`. | Podar `AGENTS.md` a <60 líneas dejando solo comandos e invariantes arquitectónicas. |
| `Domain_Classes_Should_Be_Sealed` sigue fallando tras borrar `LegacyVibeCodedHelper.cs` | El agente creó una clase auxiliar o de cálculo en `Domain` olvidando el modificador `sealed`. | Agregar `sealed` a la clase reportada en `result.FailingTypeNames`. |
| `ExportSummary_ReturnsDeterministicCountsBySeverity` falla en `BreachedIncidents` | `InMemoryIncidentStore` en `starter/` tiene 4 incidentes; en la especificación de referencia se evalúan los 5 incidentes (incluyendo `INC-2026-1005`) o los 4 del store inicial. | Verificar que el test y `InMemoryIncidentStore` usen el mismo conjunto de incidentes semilla y el mismo `FixedTimeProvider(2026-10-30T14:00:00Z)`. |
| `git worktree add` falla porque `starter/` está dentro del repo general del curso | El participante corrió `git worktree add` sin estar en una rama dedicada o con árbol sucio. | Hacer `git init && git add -A && git commit -m "baseline"` dentro de una copia independiente de `starter/` en `/tmp/lab-harness` para practicar `git worktree` con total libertad. |

---

## 3. Rúbrica de Evaluación del Workshop (100 Puntos)

| Criterio | Peso | Excelente (100%) | Aceptable (70%) | Insuficiente (0–40%) |
|---|---:|---|---|---|
| **1. Ingeniería de Contexto (`AGENTS.md` + `CLAUDE.md`)** | **20 pts** | `AGENTS.md` curado (<100 líneas, sin relleno genérico), con comandos exactos de filtro xUnit y las 4 invariantes arquitectónicas; `CLAUDE.md` con `@AGENTS.md`. | `AGENTS.md` pasa el hook pero conserva texto genérico innecesario o le faltan filtros `--filter`. | Conserva el `AGENTS.md` autogenerado del starter o falta `CLAUDE.md`. |
| **2. Automatización del Harness (`.claude/settings.json` + Subagente)** | **20 pts** | `.claude/settings.json` configurado con hook `PostToolUse` ejecutando `./scripts/post-edit-dotnet-hook.sh` y subagente `.claude/agents/dotnet-arch-reviewer.md` completo. | Hook configurado pero el subagente `dotnet-arch-reviewer.md` sigue incompleto. | Sin hook configurado o el script `post-edit-dotnet-hook.sh` falla. |
| **3. Oráculo de Arquitectura con `NetArchTest.Rules` (`v1.3.2`)** | **25 pts** | `ArchitectureOracleTests.cs` verifica que `Domain` no dependa de `Infrastructure` ni de `Microsoft.AspNetCore.Http` y que todas las clases de `Domain` sean `sealed`; `LegacyVibeCodedHelper.cs` eliminado/remediado. | Reglas de `NetArchTest` implementadas parcialmente (solo 1 de las 2 invariantes). | `ArchitectureOracleTests.cs` sigue con `TODO` o `LegacyVibeCodedHelper.cs` sigue en `Domain`. |
| **4. Implementación HITL (Tarea A) y Full AI (Tarea B) + Integración** | **25 pts** | `POST /api/sla/credits/calculate` (tope 30%/20%, `MidpointRounding.ToEven`, errores RFC 9457) y `GET /api/sla/incidents/export-summary` implementados y pasando los 4 tests de `WebApplicationFactory<Program>`. | Ambos endpoints funcionan en el camino feliz pero falta validación RFC 9457 para facturas negativas o tiers inválidos. | Alguno de los dos endpoints lanza `NotImplementedException` o fallan tests de integración. |
| **5. Debrief Empírico (`comparativa-hitl-vs-full-ai.md`)** | **10 pts** | Cuadro comparativo completo con métricas reales de la dupla (tiempos de oráculo/generación/revisión, intervenciones del hook y justificación de riesgo). | Cuadro completado de forma superficial sin desglosar tiempos de revisión vs. generación. | No entregaron el análisis comparativo. |

### Comando de Corrección Rápida para el Docente
```bash
./scripts/post-edit-dotnet-hook.sh
```
*(Verifica en un solo paso: `CLAUDE.md`, longitud y curación de `AGENTS.md`, compilación con `TreatWarningsAsErrors=true` y los 7 tests de `NetArchTest` + `WebApplicationFactory`).*
