# Matriz Comparativa de Ejecución: Modo Human-in-the-Loop (HITL) vs. Modo Full AI Autónomo (`git worktrees`)

- **Proyecto:** `GuardiaCloud.Sla.HarnessLab` (.NET 10)
- **Oráculo de contención activo:** `NetArchTest.Rules v1.3.2` (`ArchitectureOracleTests`) + `WebApplicationFactory<Program>` (`SlaHarnessEndpointsTests`) + `TreatWarningsAsErrors=true` + Hook `post-edit-dotnet-hook.sh`.

## Resultados Medidos en el Laboratorio

| Dimensión | Tarea A — Motor de Créditos Financieros (`POST /api/sla/credits/calculate`) | Tarea B — Exportador de Resumen de Guardia (`GET /api/sla/incidents/export-summary`) |
|---|---|---|
| **Modo de ejecución elegido** | **Human-in-the-Loop (HITL)** con aprobación de Plan y revisión de casos borde | **Full AI Autónomo** en `git worktree` aislado (`../worktree-full-ai`) |
| **Por qué corresponde este modo** | Regla financiera crítica (redondeo bancario `MidpointRounding.ToEven`, topes diferenciados 30% vs. 20%, penalidades acumuladas). | Operación de solo lectura (`GET`), contrato cerrado (`ShiftExportSummaryDto`) y oráculo determinista 100% especificado de antemano. |
| **Tiempo de especificación / preparación del oráculo** | 8 min (co-diseño de reglas e invariantes con el agente en *Plan Mode*) | 6 min (escritura previa del test de contrato `ExportSummary_ReturnsDeterministicCountsBySeverity`) |
| **Tiempo de generación / iteración del agente** | 6 min (guiado paso a paso) | 3 min (ejecución autónoma validada por `post-edit-dotnet-hook.sh`) |
| **Tiempo de revisión humana del diff** | 4 min (diff ya conocido durante la sesión HITL) | 5 min (auditoría guiada por `dotnet-arch-reviewer` + lectura focalizada) |
| **Intervenciones humanas durante la codificación** | 2 intervenciones (ajustar validación de `IncidentIds` inexistentes y redondeo bancario) | 0 intervenciones durante el bucle (el hook frenó 1 intento de usar `DateTimeOffset.UtcNow`) |
| **Conflictos de merge al integrar ambos `worktrees`** | 0 conflictos en `SlaModels.cs` / `SlaRuleEngine.cs` (métodos separados) · 1 merge limpio en `Program.cs` | Integrado vía `git merge worktree-full-ai` con los 7 tests pasando en verde |

## Conclusiones de Ingeniería para la Consultora
1. **El modo Full AI sin un Oráculo (`NetArchTest` + tests de integración + hook) produce deuda oculta** (como demostró `LegacyVibeCodedHelper.cs` en la Fase 2).
2. **Con el Oráculo activo, delegar tareas acotadas (Tarea B) en un `git worktree` paralelo libera al ingeniero senior** para concentrar su atención cognitiva en las reglas financieras de alto riesgo (Tarea A).
