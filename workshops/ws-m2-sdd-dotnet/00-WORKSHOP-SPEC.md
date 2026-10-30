# Especificación del Workshop: Spec-Driven Development sobre .NET con GitHub Spec Kit y OpenSpec

- **ID del Workshop:** `ws-m2-sdd-dotnet`
- **Unidades del Temario v2 cubiertas:** **Unidad 2.1** (*Especificaciones Ejecutables por Agentes*) + **Unidad 2.4** (*Herramientas y Frameworks para SDD*)
- **Duración total:** **3 horas 45 minutos (225 min)** de práctica guiada intensiva *(puede dictarse en un bloque continuo de media jornada o dividido en Parte 1 [1h 45m] en la Unidad 2.1 y Parte 2 [2h 00m] en la Unidad 2.4)*.
- **Stack técnico:** **.NET 10 (C# 13, ASP.NET Core Minimal APIs, `ProblemDetails` RFC 9457, `System.TimeProvider`, xUnit + `WebApplicationFactory`)**, **GitHub Spec Kit (`v1.2.5`)** y **OpenSpec (`v1.15.0`)**.
- **Peso en la evaluación del curso:** **15% de la nota final** (Entregable Evaluable #2 del curso).

---

## 1. Propósito y Contexto de Negocio

En el trabajo diario de una consultora de software, el 80% del retrabajo con agentes de IA no ocurre porque el modelo "no sepa programar en C#", sino porque **resuelve el problema equivocado** a partir de un pedido ambiguo o incompleto (como demostró la evidencia empírica de Larbi et al. y SWE-EVO).

En este workshop vas a tomar el rol del equipo de ingeniería `.NET` a cargo de **`GuardiaCloud.Sla.Api`**, el microservicio que audita el cumplimiento de acuerdos de nivel de servicio (SLA) de incidentes críticos para clientes bancarios y aseguradoras. Partiendo de un mensaje real y ambiguo del Gerente de Operaciones (`starter/brief-cliente-ambiguo.md`), vas a:
1. Descubrir los huecos ocultos del pedido usando un agente con rol de **Analista Adversarial** y redactar una especificación sin ambigüedades con notación **EARS** y escenarios **Given/When/Then**.
2. Diagnosticar y reparar un bug productivo en el cálculo de SLA usando la extensión de bugs de **GitHub Spec Kit (`v1.2.5`)** (`/speckit-bug-assess` $\rightarrow$ `/speckit-bug-fix` $\rightarrow$ `/speckit-bug-test`).
3. Desarrollar de punta a punta las **Ventanas de Pausa Auditable de SLA** usando el flujo completo de **GitHub Spec Kit** (`/speckit-constitution` $\rightarrow$ `/speckit-specify` $\rightarrow$ `/speckit-plan` $\rightarrow$ `/speckit-tasks` $\rightarrow$ `/speckit-implement` $\rightarrow$ **`/speckit-converge`**).
4. Evolucionar el sistema ya en producción (*brownfield*) dos semanas después aplicando un cambio de regla regulatoria mediante **Especificaciones Delta en OpenSpec (`v1.15.0`)** (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`).

---

## 2. Objetivos de Aprendizaje Medibles

Al finalizar el workshop, cada participante/dupla será capaz de:
1. **Detectar ambigüedades antes de tocar código:** Utilizar un agente como crítico adversarial para identificar estados faltantes, invariantes temporales y códigos de error HTTP omitidos en un pedido de negocio.
2. **Escribir especificaciones ejecutables (EARS + GWT):** Redactar requerimientos con sintaxis **EARS** (`WHEN... WHILE... THE SYSTEM SHALL...`) y criterios de aceptación **Given/When/Then** directamente traducibles a tests de integración con `WebApplicationFactory<Program>`.
3. **Operar GitHub Spec Kit (`v1.2.5`) sobre .NET:** Gobernar al agente mediante `.specify/memory/constitution.md`, generar el encadenamiento `spec.md` $\rightarrow$ `plan.md` $\rightarrow$ `tasks.md`, ejecutar la implementación y auditar la convergencia con `/speckit-converge`.
4. **Operar OpenSpec (`v1.15.0`) en escenarios Brownfield:** Modelar un cambio sobre funcionalidad existente separando la verdad actual (`openspec/specs/`) del delta propuesto (`openspec/changes/` con bloques `MODIFIED` y `ADDED Requirements`) y fusionarlo limpiamente tras verificar los tests.

---

## 3. Agenda y Cronograma (225 minutos)

| Fase | Tiempo | Minutos | Actividad práctica | Artefacto producido |
|---|---:|---:|---|---|
| **Fase 0** | 0:00 – 0:15 | 15 min | Clonado/apertura de `starter/`, ejecución de `dotnet test` base y lectura de `brief-cliente-ambiguo.md`. | Entorno `.NET 10` compilando y pasando los 2 tests base en <1 seg. |
| **Fase 1** | 0:15 – 1:00 | 45 min | **Auditoría Adversarial y EARS (Unidad 2.1):** Entrevista al "cliente" (instructor), destrabe de las 7 ambigüedades y redacción de requerimientos EARS + escenarios GWT. | Matriz de clarificación + borrador de Spec Funcional validada. |
| **Fase 2A** | 1:00 – 1:25 | 25 min | **Spec Kit Bugfix Workflow:** Diagnóstico y corrección del bug de incidentes resueltos (`ResolvedAtUtc`) con `/speckit-bug-assess`, `/speckit-bug-fix` y `/speckit-bug-test`. | `.specify/bugs/resolved-sla-breach-drift/` + test de regresión en verde. |
| **Fase 2B** | 1:25 – 2:15 | 50 min | **Spec Kit Feature Workflow (`v1.2.5`):** Constitución `.NET`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` y `/speckit-converge` para `001-sla-pause-windows`. | `specs/001-sla-pause-windows/*` + endpoints `/pause` y `/resume` + tests xUnit en verde. |
| **Fase 3** | 2:15 – 3:15 | 60 min | **OpenSpec Brownfield Delta (`v1.15.0`):** Nuevo cambio regulatorio (tope de 30 min en P1 salvo `SupervisorOverrideCode`) con `/opsx:explore`, `/opsx:propose`, `/opsx:apply` y `/opsx:archive`. | `openspec/changes/archive/...` + `openspec/specs/sla-tracking/spec.md` actualizada + test P1 en verde. |
| **Fase 4** | 3:15 – 3:45 | 30 min | **Auditoría Cruzada y Cierre:** Cada dupla revisa el repo de otra dupla corriendo `dotnet test` y verificando trazabilidad Spec $\leftrightarrow$ Test. | Entrega final calificada con la rúbrica de 100 puntos. |

---

## 4. Requisitos Previos verificables

Antes de iniciar el reloj del taller, verificá en tu terminal:
```bash
dotnet --version          # Debe ser 10.0.x (o 9.0.x ajustando TargetFramework)
uv --version              # Para GitHub Spec Kit (uv tool install specify-cli)
node --version            # v22+ para OpenSpec (npm install -g @fission-ai/openspec@latest)
```
> **Nota resiliente para el aula:** Si algún participante tiene restricciones de red corporativa para instalar `specify-cli` u `openspec` globalmente, la guía paso a paso incluye las plantillas y estructura exacta de directorios (`.specify/`, `specs/`, `openspec/`) para ejecutar el flujo idéntico desde cualquier *harness* (Claude Code, GitHub Copilot Chat/Agent o Codex).

---

## 5.Estructura del Paquete del Workshop

```text
workshops/ws-m2-sdd-dotnet/
├── 00-WORKSHOP-SPEC.md                 # Este documento (especificación y agenda)
├── 01-GUIA-PASO-A-PASO.md              # Guía práctica para el participante (en voseo rioplatense)
├── 02-GUIA-FACILITADOR-Y-RUBRICA.md    # Guía docente, hoja de respuestas del role-play y rúbrica
├── starter/                            # Solución .NET 10 inicial ("Antes" del workshop, 2 tests verdes)
│   ├── AGENTS.md / CLAUDE.md
│   ├── brief-cliente-ambiguo.md
│   ├── GuardiaCloud.Sla.sln
│   ├── openspec/specs/sla-tracking/spec.md
│   ├── src/GuardiaCloud.Sla.Api/
│   └── tests/GuardiaCloud.Sla.Tests/
└── solution/                           # Solución .NET 10 de referencia ("Después" del workshop, 4 suites verdes)
    ├── AGENTS.md / CLAUDE.md
    ├── GuardiaCloud.Sla.sln
    ├── .specify/memory/constitution.md
    ├── .specify/bugs/resolved-sla-breach-drift/report.md
    ├── specs/001-sla-pause-windows/{spec.md, plan.md, tasks.md}
    ├── openspec/specs/sla-tracking/spec.md
    ├── openspec/changes/archive/2026-10-30-cap-p1-pause-budget/{proposal.md, design.md, tasks.md, specs/sla-tracking/spec.md}
    ├── src/GuardiaCloud.Sla.Api/
    └── tests/GuardiaCloud.Sla.Tests/
```
