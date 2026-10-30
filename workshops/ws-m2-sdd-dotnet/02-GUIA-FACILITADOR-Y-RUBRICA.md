# Guía del Facilitador y Rúbrica de Evaluación — Workshop M2 (`ws-m2-sdd-dotnet`)

> **Uso exclusivo del instructor / facilitador.** Contiene el guion minuto a minuto, la "hoja de respuestas" para el *role-play* como Gerente de Operaciones en la Fase 1, los errores típicos en el aula con sus soluciones rápidas y la rúbrica de calificación (100 puntos = 15% de la nota final del curso).

---

## 1. Cronograma y Dinámica de Facilitación (225 minutos)

| Bloque | Minutos | Qué hace el instructor | Qué hacen los participantes | Señal de que podemos avanzar |
|---|---:|---|---|---|
| **Fase 0: Kickoff** | 0–15 (15m) | Presenta el caso `GuardiaCloud.Sla.Api`, muestra `brief-cliente-ambiguo.md` en pantalla y pide correr `dotnet test` en `starter/`. | Corren `dotnet test` (2 verdes) y leen `AGENTS.md` + `brief-cliente-ambiguo.md`. | 100% de las máquinas compilan `.NET 10` sin errores. |
| **Fase 1: Auditoría Adversarial y EARS** | 15–60 (45m) | Explica en 5 min cómo usar el agente como *Analista Adversarial*. Durante 15 min actúa en vivo como **"Martín (Gerente de Operaciones)"** respondiendo solo lo que los equipos le preguntan. En los últimos 25 min guía la escritura EARS + GWT. | Corren el prompt adversarial, hacen preguntas a "Martín", descubren los 7 huecos y redactan los requerimientos EARS. | Cada dupla tiene escritas las 7 decisiones de clarificación y al menos 4 requerimientos EARS. |
| **Fase 2A: Spec Kit Bugfix** | 60–85 (25m) | Demuestra en 5 min cómo `/speckit-bug-assess` evita que el agente meta parches a ciegas. Circula viendo que usen `FakeTimeProvider` en el test de regresión. | Diagnostican el bug de `ResolvedAtUtc` en `SlaCalculator`, aplican el fix y agregan el test de regresión. | `dotnet test` muestra 3 tests pasando en verde. |
| **Fase 2B: Spec Kit Feature (`001-sla-pause-windows`)** | 85–135 (50m) | Muestra cómo `/speckit-constitution` ancla las reglas de `.NET` y enfatiza el **Checkpoint de revisión humana** entre `/speckit-tasks` y `/speckit-implement`. Al final muestra `/speckit-converge`. | Generan `constitution.md`, `spec.md`, `plan.md`, `tasks.md`, ejecutan la implementación y corren `/speckit-converge`. | Endpoints `/pause` y `/resume` andando, tests pasando y `tasks.md` en estado `Converged`. |
| **Fase 3: OpenSpec Brownfield Delta** | 135–195 (60m) | Introduce el "cambio de requisito 2 semanas después" (tope de 30 min en P1 salvo `SupervisorOverrideCode`). Contrasta Spec Kit (feature completo) vs. OpenSpec (deltas `MODIFIED`/`ADDED` sobre un sistema vivo). | Ejecutan `/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive` para `cap-p1-pause-budget`. | `openspec/specs/sla-tracking/spec.md` fusionada y test de presupuesto P1 en verde. |
| **Fase 4: Auditoría Cruzada y Debrief** | 195–225 (30m) | Empareja a las duplas para revisión cruzada (15 min) y lidera el cierre (15 min) comparando cuánto retrabajo se ahorró al atrapar las ambigüedades en el Markdown antes de compilar C#. | Auditan el repo de otra dupla con los 4 checks objetivos y aplican la rúbrica. | Todas las duplas con `dotnet test` 100% en verde y trazabilidad verificada. |

---

## 2. Hoja de Respuestas del Instructor para el Role-Play de la Fase 1 ("Martín — Gerente de Operaciones")

> **Regla de oro pedagógica:** Durante los 15 minutos de entrevista de la Fase 1, **no regales las 7 respuestas de entrada**. Respondé únicamente a las preguntas específicas que te hagan las duplas a partir del análisis de su agente adversarial. Si al minuto 12 alguna pregunta crítica no salió, hacé una pregunta disparadora al grupo (*"Che, ¿y qué pasa si un operador cierra el ticket mientras el reloj estaba pausado? ¿Nadie me lo va a preguntar?"*).

| # | Pregunta que deberían hacerte | Tu respuesta como "Martín (Operaciones)" | Código / Regla técnica resultante |
|---|---|---|---|
| **1** | *"¿Se puede pausar por cualquier motivo o hay una lista cerrada para el banco?"* | *"Buena pregunta. El banco solo nos acepta tres motivos: esperando logs del cliente, esperando acceso VPN del cliente, o esperando validación del cliente en su entorno."* | Enum `SlaPauseReason`: `WaitingForCustomerLogs = 1`, `WaitingForCustomerVpnAccess = 2`, `WaitingForCustomerValidation = 3`. |
| **2** | *"¿Qué datos nos pide la auditoría del banco en cada pausa y reanudación?"* | *"Sí o sí quién lo pidió (`RequestedBy`), el motivo y una nota de evidencia con el número de ticket o pedido (`EvidenceNote`). Y cuando se reanuda, quién lo reanudó (`ResumedBy`). Si mandan eso vacío, reboten el request."* | `400 Bad Request` (`ProblemDetails`) si `RequestedBy`, `EvidenceNote` o `ResumedBy` están vacíos/blancos. |
| **3** | *"¿Qué pasa si mandan dos veces seguidas `pause` o quieren pausar un incidente ya cerrado?"* | *"No tiene sentido pausar algo ya resuelto ni abrir dos pausas al mismo tiempo. Rebótenlo como conflicto de estado."* | `409 Conflict` (`ProblemDetails`) si `Status == Resolved` o si ya existe una ventana con `IsActive == true`. |
| **4** | *"¿Y si llaman a `resume` cuando el incidente NO estaba pausado?"* | *"También conflicto de estado (`409`)."* | `409 Conflict` (`ProblemDetails`) si no hay ventana activa. |
| **5** | *"¿Podemos recibir fechas `PausedAtUtc` o `ResumedAtUtc` por parámetro? ¿Qué pasa si son anteriores a la apertura o a la pausa?"* | *"Sí, a veces el integrador manda el timestamp del evento; si no lo manda, usen la hora actual del servidor. Pero si mandan una pausa anterior a `OpenedAtUtc` o una reanudación anterior a `PausedAtUtc`, rechácenlo por regla de negocio."* | `422 Unprocessable Entity` (`ProblemDetails`) si `PausedAtUtc < OpenedAtUtc` o `ResumedAtUtc < PausedAtUtc`. |
| **6** | *"¿Qué pasa si el cliente nos confirma que ya se arregló todo y llamamos directo a `/resolve` mientras el incidente estaba en `WaitingForCustomer`?"* | *"No hagan que el operador tenga que llamar a dos endpoints. Si se resuelve estando en pausa, cierren automáticamente la pausa en ese mismo instante de resolución y pásenlo a `Resolved`."* | En `POST /resolve`, si hay ventana activa, setear `ResumedAtUtc = resolvedAt` y `ResumedBy = "system:auto-resume-on-resolve"`. |
| **7** | *"¿Qué campos nuevos necesita ver el dashboard en `GET /api/incidents/{id}/sla`?"* | *"Además de lo que ya devuelve, necesito ver el total de minutos pausados (`TotalPausedMinutes`) y cuántas veces se pausó (`PauseCount`), y que `EffectiveDeadlineUtc` se corra hacia adelante sumando los minutos pausados."* | `SlaStatusResponse` suma `TotalPausedMinutes` y `PauseCount`; `EffectiveDeadlineUtc = OpenedAtUtc + Target + TotalPausedMinutes`. |

---

## 3. Fallas Frecuentes en el Aula y Cómo Destrabarlas Rápido

1. **El agente usa `DateTimeOffset.UtcNow` directo en `SlaPauseWindow` o en los endpoints y los tests con `FakeTimeProvider` fallan:**
   - *Causa:* El agente ignoró la regla de tiempo determinista o la Constitución no fue lo bastante explícita.
   - *Destrabe (1 min):* Mostrar cómo un simple `grep -rn "UtcNow" src/` lo detecta al instante y por qué esa regla debe estar en el Principio I de `.specify/memory/constitution.md` (y eventualmente en un hook o test de arquitectura).
2. **Desincronización de parámetros posicionales en el `record SlaStatusResponse` al agregar campos en Fase 2 y Fase 3:**
   - *Causa:* En C#, si `SlaStatusResponse` es un positional record y se insertan propiedades en el medio sin usar named arguments al instanciarlo en `SlaCalculator`, los valores `double` (`ElapsedActiveMinutes`, `TotalPausedMinutes`, `RemainingMinutes`) pueden intercambiarse silenciosamente sin error de compilación.
   - *Destrabe (1 min):* Señalar en `solution/src/GuardiaCloud.Sla.Api/Services/SlaServices.cs` el uso de **named arguments** (`ElapsedActiveMinutes: ...`, `TotalPausedMinutes: ...`) al construir `SlaStatusResponse`. ¡Excelente lección real de C# con agentes!
3. **El participante confunde cuándo usar GitHub Spec Kit vs. cuándo usar OpenSpec:**
   - *Regla mnemotécnica para el pizarrón:*
     - **GitHub Spec Kit (`v1.2.5`)** = *"Voy a construir un módulo o funcionalidad grande (o correr un flujo guiado de bugfix/assessment) y quiero el pipeline completo `constitution` $\rightarrow$ `specify` $\rightarrow$ `plan` $\rightarrow$ `tasks` $\rightarrow$ `implement` $\rightarrow$ `converge`."*
     - **OpenSpec (`v1.15.0`)** = *"Ya tengo un sistema en producción con especificaciones vivas (`openspec/specs/`) y necesito introducir un cambio iterativo (*brownfield delta*: `ADDED / MODIFIED / REMOVED Requirements`) viendo exactamente qué cambia antes de fusionarlo con `/opsx:archive`."*

---

## 4. Rúbrica de Evaluación del Workshop (100 Puntos = 15% de la Nota del Curso)

| Criterio | Peso | Excelente (100% del criterio) | Aceptable (70% del criterio) | Insuficiente (<50% del criterio) |
|---|---:|---|---|---|
| **1. Calidad de la Especificación EARS + GWT y Constitución (`specs/001-sla-pause-windows/spec.md` & `constitution.md`)** | **25 pts** | Captura las 7 decisiones de negocio sin ambigüedad usando sintaxis EARS (`WHEN/WHILE/IF... SHALL`) y escenarios Given/When/Then testeables. La Constitución define claramente las 4 invariantes `.NET`. | Captura la mayoría de las reglas pero omite 1–2 casos borde (ej. auto-cierre de pausa al resolver o códigos HTTP exactos). | Especificación vaga, copiada del prompt inicial sin resolver ambigüedades ni usar EARS/GWT. |
| **2. Descomposición Técnica y Convergencia en Spec Kit (`plan.md`, `tasks.md` y `/speckit-bug-*`)** | **20 pts** | Reporte de bug `resolved-sla-breach-drift` completo; `plan.md` y `tasks.md` mapean archivos `.cs` exactos e historias `[US1]`/`[US2]`; reporte `/speckit-converge` en estado `Converged`. | `plan.md` y `tasks.md` presentes pero con tareas demasiado gruesas o sin verificación explícita de convergencia. | Saltó directamente a generar código C# sin producir ni revisar `plan.md` / `tasks.md`. |
| **3. Flujo Delta Brownfield en OpenSpec (`openspec/changes/...` y `openspec/specs/sla-tracking/spec.md`)** | **20 pts** | Propuesta, diseño, tareas y Spec Delta (`MODIFIED` + `ADDED Requirements`) completos para el tope de 30 min en P1 + `SupervisorOverrideCode`, correctamente archivados y fusionados en `openspec/specs/sla-tracking/spec.md`. | El cambio fue implementado en código pero el Spec Delta no usa secciones `MODIFIED`/`ADDED` o no se fusionó en la especificación viva. | No utilizó estructura delta; editó el código directamente sin trazabilidad en `openspec/`. |
| **4. Calidad de Implementación C# (.NET 10) y Cumplimiento de Invariantes** | **20 pts** | Compila con `0 warnings` (`TreatWarningsAsErrors=true`), usa `TimeProvider` en todo el flujo, devuelve `ProblemDetails` RFC 9457 (`400`/`404`/`409`/`422`) y modela limpiamente el dominio. | Compila y funciona en el camino feliz, pero usa `DateTimeOffset.UtcNow` en algún punto o devuelve códigos HTTP genéricos. | No compila, desactiva `TreatWarningsAsErrors` o rompe endpoints existentes. |
| **5. Suite de Pruebas de Integración (`WebApplicationFactory` + `FakeTimeProvider`)** | **15 pts** | Todos los tests en `GuardiaCloud.Sla.Tests` pasan en verde, cubriendo: (a) regresión de `ResolvedAtUtc`, (b) pausa/reanudación P2, (c) rechazo `409` en doble pausa, y (d) tope de 30 min en P1 con y sin `SupervisorOverrideCode`. | Pasan los tests del camino feliz pero falta cubrir el caso de borde del presupuesto P1 o el test de regresión del bug. | Tests rotos, ausentes o acoplados a `Thread.Sleep`/reloj real en vez de `FakeTimeProvider`. |
| **TOTAL** | **100 pts** | **Equivale al 15% de la calificación final del curso.** | | |
