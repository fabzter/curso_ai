# Especificación del Proyecto Integrador (Capstone): GuardiaCloud Command Center v2.0

- **ID del Workshop / Capstone:** `ws-m3-capstone-dotnet`
- **Módulo y Unidades del Temario v2 cubiertas:** **Módulo 3 Completo (14 horas)**:
  - **Unidad 3.1 (2 hs):** *Presentación del Caso y Entendimiento Funcional*
  - **Unidad 3.2 (4 hs):** *Especificaciones y Diseño del Proyecto (EARS/GWT + Técnica .NET + Prototipo UI + Revisión Cruzada)*
  - **Unidad 3.3 (2 hs):** *Planificación, Análisis de Impacto y Grafo de Tareas Paralelizable (`tasks.md`)*
  - **Unidad 3.4 (6 hs):** *Implementación Agéntica en Sprints, Checkpoint de Convergencia, QA Cruzado, Demo en Vivo y Retrospectiva con Métricas*
- **Stack técnico:** **.NET 10 (C# 13, ASP.NET Core Minimal APIs, `System.TimeProvider`, `ProblemDetails` RFC 9457)**, **`NetArchTest.Rules` (`v1.3.2`)**, **xUnit + `WebApplicationFactory<Program>`**, **GitHub Spec Kit (`v1.2.5`) / OpenSpec (`v1.15.0`)**, **Skills (`SKILL.md`) + Servidor MCP C# (`ModelContextProtocol` `v2.3.0`)** y **`git worktrees`**.
- **Peso en la evaluación del curso:** **70% de la nota final del curso**, distribuido en 3 entregables evaluables:
  - **Entregable #3 (25%):** Constitución (`AGENTS.md`), Specs (EARS/GWT + Técnica .NET), Prototipo UI y Plan Paralelizable (`tasks.md`).
  - **Entregable #4 (35%):** Proyecto .NET funcionando en vivo, suite de pruebas oráculo (`NetArchTest` + `WebApplicationFactory`) y Demo.
  - **Entregable #5 (10%):** Retrospectiva de ingeniería basada en métricas y plan de transferencia a la consultora.

---

## 1. Propósito y Diseño Anti-Fricción para las 14 Horas

En muchos cursos, el proyecto final fracasa porque los equipos pierden la mitad del tiempo configurando un proyecto vacío o discutiendo qué construir.
En **`ws-m3-capstone-dotnet`**, cada equipo de **3 a 5 integrantes** recibe el repositorio semilla **`GuardiaCloud.CommandCenter.sln`** (`starter/`) ya compilando en `.NET 10` con 3 tests base en verde, junto con un pliego de negocio realista (`pliego-licitacion-cliente.md`) que requiere:
1. Diagnosticar y reparar un **defecto crítico de producción (`BUG-301`)**: duplicación de minutos pausados y penalidades ante reintentos de webhooks.
2. Especificar, planificar e implementar **3 Vertical Slices de negocio (`FEAT-301`, `FEAT-302`, `FEAT-303`)** en paralelo sin pisarse entre compañeros ni entre agentes:
   - **`FEAT-301`:** Motor de Escalamiento Proactivo al **80% del SLA** con ventana de enfriamiento (*cooldown*) de **15 minutos**.
   - **`FEAT-302`:** Registro de **Exenciones por Fuerza Mayor** (caídas de BCRA/Coelsa/Nube) con validación de **control dual de aprobadores** y token criptográfico `FM-DUAL-*`.
   - **`FEAT-303`:** **Tablero Ejecutivo Consolidado por Tier** (`GET /api/command-center/dashboard/{clientTier}`) que calcula la exposición financiera en USD excluyendo incidentes exentos, listo para conectar al prototipo UI generado en la Unidad 3.2.

---

## 2. Topología del Equipo (3 a 5 Personas)

Para evitar el **27,67% de conflictos de merge** documentado en equipos que corren agentes en paralelo sin fronteras claras, cada equipo asigna 4 roles explícitos desde la Unidad 3.1:

| Rol en el Equipo | Responsabilidad Principal durante las 14 hs | Slice Asignada en Unidad 3.4 |
|---|---|---|
| **1. Product & Spec Lead** | Lidera el cuestionario de entrevista al cliente (U3.1), consolida la Spec Funcional EARS/GWT (U3.2) y el prototipo UI. | `FEAT-301` (Escalamiento Proactivo 80% + Cooldown 15m) en `wt-feat301`. |
| **2. Architect & Harness Lead** | Gobierna `AGENTS.md`/`CLAUDE.md`, configura la Skill de equipo y los hooks (U3.2), y lidera la revisión de arquitectura. | `FEAT-302` (Exención por Fuerza Mayor con control dual) en `wt-feat302` (modo HITL). |
| **3. Backend & MCP Lead** | Conecta el servidor MCP C# del Módulo 1, ejecuta el análisis de impacto (U3.3) y coordina la integración de ramas. | `BUG-301` (Idempotencia de Webhooks con `ProcessedWebhookEventIds`) en `wt-bug301`. |
| **4. QA, Oracle & Integration Lead** *(1 o 2 personas)* | Escribe primero los tests de contrato `WebApplicationFactory` y `NetArchTest` en el arranque del Sprint 1 (TDD Agéntico) y lidera el QA cruzado. | `FEAT-303` (Tablero Ejecutivo por Tier + conexión UI) en `wt-feat303`. |

---

## 3. Cronograma Completo de las 14 Horas (Unidades 3.1 a 3.4)

| Unidad | Duración | Actividad Práctica del Equipo | Entregable Verificable |
|---|---:|---|---|
| **Unidad 3.1** | **2:00 hs** | Lectura de `pliego-licitacion-cliente.md`, auditoría del repo semilla con agente explorador y **2 rondas de entrevista al cliente (instructor)** para destrabar las 8 reglas ocultas. | Matriz de Clarificación y Alcance validada. |
| **Unidad 3.2** | **4:00 hs** | Configuración del Harness (`AGENTS.md`, Skill RFC 9457, MCP C#), redacción de `specs/command-center-v2/spec.md` (EARS/GWT) + `plan.md` (.NET 10), prototipo de UI del Dashboard y **Auditoría Adversarial Cruzada** con otro equipo. | **Entregable #3 Parte A** aprobado con *sign-off* del instructor. |
| **Unidad 3.3** | **2:00 hs** | Análisis de impacto automatizado, descomposición en el DAG `specs/command-center-v2/tasks.md` (definiendo modo `HITL` vs. `Full AI`, `git worktrees` y comando oráculo por tarea) y estimación. | **Entregable #3 Parte B** (`tasks.md` + estimación comparada). |
| **Unidad 3.4 – Sprint 1** | **2:00 hs** | **TDD Agéntico:** escritura de los 5 tests de aceptación HTTP en `CommandCenterTests.cs` primero, seguida de la implementación de `BUG-301` y `FEAT-301` en worktrees aislados. | Tests de `BUG-301` y `FEAT-301` pasando en verde. |
| **Unidad 3.4 – Checkpoint** | **0:30 hs** | Ejecución de `/speckit-converge` (verificación de deriva Spec $\leftrightarrow$ Código), resolución de bloqueos de integración y merge intermedio a `main`. | `main` compilando con 0 warnings y 5/8 tests en verde. |
| **Unidad 3.4 – Sprint 2** | **2:00 hs** | Implementación paralela de `FEAT-302` (HITL) y `FEAT-303` (Full AI + UI), code review cruzado asistido por el subagente `dotnet-arch-reviewer` y merge final. | **8/8 tests en verde** (2 `NetArchTest` + 6 `WebApplicationFactory`). |
| **Unidad 3.4 – QA y Demo** | **1:30 hs** | **0:45 hs:** QA de aceptación cruzado contra los escenarios GWT de otro equipo. **0:45 hs:** Demo funcional en vivo (10 min por equipo) + presentación de `retrospectiva-metricas.md`. | **Entregable #4 (35%)** y **Entregable #5 (10%)** calificados en vivo. |

---

## 4. Estructura del Paquete del Proyecto Integrador

```text
workshops/ws-m3-capstone-dotnet/
├── 00-WORKSHOP-SPEC.md                 # Este documento (especificación de las 14 hs y topología de equipos)
├── 01-PLIEGO-CASO-Y-GUIA-EQUIPOS.md    # Guía paso a paso por unidad (3.1 a 3.4) para los equipos participantes
├── 02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md# Hoja de respuestas del cliente (U3.1) y las 3 rúbricas oficiales (70% nota)
├── starter/                            # Repositorio Semilla .NET 10 ("Antes" del Módulo 3, 3 tests base en verde)
│   ├── AGENTS.md / CLAUDE.md
│   ├── pliego-licitacion-cliente.md    # Pedido de negocio con BUG-301, FEAT-301..303 y 8 ambigüedades
│   ├── plantilla-retrospectiva-metricas.md
│   ├── GuardiaCloud.CommandCenter.sln
│   ├── src/GuardiaCloud.CommandCenter.Api/
│   └── tests/GuardiaCloud.CommandCenter.Tests/
└── solution/                           # Solución de Referencia .NET 10 ("Después" del Módulo 3, 8 tests en verde)
    ├── AGENTS.md / CLAUDE.md
    ├── specs/command-center-v2/{spec.md, plan.md, tasks.md}
    ├── retrospectiva-metricas-equipo-referencia.md
    ├── GuardiaCloud.CommandCenter.sln
    ├── src/GuardiaCloud.CommandCenter.Api/
    └── tests/GuardiaCloud.CommandCenter.Tests/
```
