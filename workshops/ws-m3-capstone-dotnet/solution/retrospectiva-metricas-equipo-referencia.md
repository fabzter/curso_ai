# Retrospectiva de Ingeniería Basada en Métricas (Entregable #5 — Referencia)

- **Equipo:** Equipo Alfa (`GuardiaCloud Command Center v2.0`)
- **Integrantes y Roles:**
  - *Product & Spec Lead:* Integrante 1
  - *Architect & Harness Lead:* Integrante 2
  - *Backend & MCP Lead:* Integrante 3
  - *QA, Oracle & Integration Lead:* Integrante 4

---

## 1. Tabla de Ejecución Real vs. Estimada por Tarea (`tasks.md`)

| ID Tarea | Módulo / Slice | Modo Elegido (`HITL` / `Full AI`) | Tiempo Estimado (min) | Tiempo Real Generación (min) | Tiempo Real Revisión/QA (min) | Iteraciones del Agente | ¿Contuvo errores el Oráculo? |
|---|---|---|---:|---:|---:|---:|---|
| `BUG-301` | Idempotencia de Webhooks | **Full AI** | 25 min | 4 min | 5 min | 1 | Sí (test de duplicado validó `ProcessedWebhookEventIds`). |
| `FEAT-301` | Escalamiento Proactivo (80% + Cooldown 15m) | **Full AI** | 45 min | 7 min | 8 min | 2 | Sí (corrigió comparación `>= 80.0` vs `> 80.0`). |
| `FEAT-302` | Exención Fuerza Mayor (Doble firma + RFC 9457) | **HITL** | 50 min | 12 min | 6 min | 2 | Sí (validó comparación case-insensitive de emails). |
| `FEAT-303` | Tablero Ejecutivo por Tier | **Full AI** | 40 min | 6 min | 7 min | 1 | Sí (verificó exclusión de incidentes con exención activa). |

---

## 2. Métricas Consolidadas del Equipo
- **Porcentaje de tareas ejecutadas en Full AI vs. HITL:** `75% Full AI (3/4 slices) / 25% HITL (1/4 slice + diseño de oráculo)`
- **Conflictos de merge ocurridos entre `git worktrees`:** `0 conflictos en lógica de dominio` (1 unión trivial de rutas en `Program.cs`).
- **Defectos atrapados por `NetArchTest` o tests de contrato antes de abrir PR:** `3 defectos` (borde `>= 80%`, case-insensitivity en aprobadores y orden de descuento de exención).
- **Defectos encontrados en el QA cruzado contra la Spec (Unidad 3.4 Parte 3):** `0 defectos escapados`.

---

## 3. Tres Decisiones Concretas para Transferir a los Proyectos de la Consultora el Lunes
1. **Qué adoptaremos de inmediato en nuestros repositorios `.NET`:** Un `AGENTS.md` de menos de 80 líneas + `CLAUDE.md` (`@AGENTS.md`) + suite base `NetArchTest.Rules` en todos los proyectos nuevos y legados.
2. **Qué dejaremos de hacer al usar agentes de IA:** Prohibido pedir código a un agente a partir de un ticket ambiguo de Jira sin antes redactar los criterios EARS/GWT y el test de contrato HTTP (`WebApplicationFactory`).
3. **Cómo ajustaremos nuestras estimaciones y revisiones de PR:** Separar el tiempo de especificación/oráculo (que aumenta y requiere ingenieros senior en HITL) del tiempo de codificación de slices acotadas (que se comprime un 70% con Full AI en `git worktrees`).
