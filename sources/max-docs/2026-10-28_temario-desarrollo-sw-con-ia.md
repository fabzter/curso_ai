# Temario: Desarrollo de Software con IA

Oct 20, 2026 · @Max

## Resumen del curso

Curso de 52 horas que lleva a equipos de desarrollo de usar la IA como asistente a trabajar con agentes de forma metodológica, cerrando con un proyecto real construido de punta a punta.

**Perfil:** desarrolladores, tech leads y arquitectos con experiencia en Git, un lenguaje de backend o frontend y trabajo en equipo ágil.

**Enfoque:** cada unidad combina 30–40% de teoría y 60–70% de práctica guiada. Todo el material práctico se encadena hacia el proyecto del Módulo 3.

| Módulo | Unidades | Horas |
|----|----|----|
| 1\. Herramientas de IA | Diseño · Herramientas de desarrollo · Agentes y Skills · Harness Engineering · MCPs | 20 |
| 2\. Metodologías adaptadas a la IA | Spec · Estimación, impacto y planning · Implementation · Herramientas para SDD | 18 |
| 3\. Ejecución de proyecto | Presentación · Specs · Planificación · Implementación | 14 |
| **Total** |  | **52** |

## Módulo 1 – Herramientas de IA (20 hs)

Objetivo: conocer el ecosistema actual de herramientas, entender cómo funciona un agente por dentro y saber configurarlo para un equipo real.

### 1.1 Diseño (4 hs)

Uso de IA para pasar de una idea a prototipos navegables y a un design system que luego consume el desarrollo.

| Bloque | Duración | Contenido |
|----|----|----|
| Panorama de IA en diseño | 0:45 | Generación de UI desde prompt, de boceto a pantalla, de captura a código. Herramientas: Figma AI / Figma Make, v0, Lovable, Google Stitch, Claude (artifacts y diseño). Límites actuales. |
| Prompting para UI | 0:45 | Cómo describir pantallas: usuario, tarea, estados, jerarquía, restricciones de marca. Uso de referencias visuales y capturas como input. |
| Design systems para IA | 0:45 | Tokens (color, tipografía, espaciado), componentes y reglas documentadas para que el modelo las respete. Cómo exportar el sistema a código (Tailwind, librería de componentes). |
| Práctica: prototipo | 1:15 | Diseñar 3–4 pantallas de un flujo, iterar con feedback y generar el handoff a desarrollo. |
| Cierre y criterios de calidad | 0:30 | Accesibilidad, consistencia, revisión humana. Qué entregar al equipo de desarrollo. |

### 1.2 Herramientas de desarrollo (4 hs)

Recorrido por los asistentes integrados al IDE y al flujo diario, con criterios para elegir y combinar.

| Bloque | Duración | Contenido |
|----|----|----|
| Mapa del ecosistema | 0:45 | Autocompletado, chat en el IDE, agentes en IDE, agentes en terminal y agentes en la nube. Cursor, Windsurf, GitHub Copilot, JetBrains AI, Claude Code, Codex. Modelos y costos. |
| Flujo de trabajo en el IDE | 1:00 | Autocompletado, edición multiarchivo, modo agente, reglas de proyecto, contexto con @archivos y documentación. |
| Casos de uso diarios | 1:00 | Entender código ajeno, refactorizar, generar tests, depurar, escribir docs, revisar PRs. Ejercicios cortos sobre un repo de ejemplo. |
| Calidad y seguridad | 0:45 | Alucinaciones, dependencias inventadas, secretos, licencias, revisión de código generado, políticas de empresa. |
| Comparativa y elección | 0:30 | Matriz de criterios: lenguaje, tamaño del repo, privacidad, costo, integración con el stack. |

### 1.3 Agentes y Skills (4 hs)

Qué es un agente, cómo funciona su bucle y cómo se le enseñan capacidades reutilizables.

| Bloque | Duración | Contenido |
|----|----|----|
| Anatomía de un agente | 0:45 | Bucle percibir–razonar–actuar, tool use, ventana de contexto, memoria, condiciones de parada. Diferencia entre chat, workflow y agente. |
| Patrones agénticos | 0:45 | Prompt chaining, routing, orquestador–subagentes, evaluador–optimizador, ejecución en paralelo. Cuándo conviene cada uno. |
| Skills | 1:00 | Qué es una skill (instrucciones + scripts + recursos en una carpeta con SKILL.md), carga bajo demanda, diferencia con prompts de sistema y con MCP. Diseño de buenas descripciones. |
| Práctica: crear una skill | 1:00 | Construir una skill del equipo (por ejemplo, convenciones de API o checklist de code review) y probarla. |
| SDKs de agentes | 0:30 | Introducción a Claude Agent SDK y OpenAI Agents SDK para agentes propios. Evaluación básica de agentes. |

### 1.4 Harness Engineering (6 hs)

El modelo es solo una parte: el harness (contexto, herramientas, permisos, hooks, entorno) define qué tan bien trabaja el agente. Se comparan tres harness representativos.

| Bloque | Duración | Contenido |
|----|----|----|
| Conceptos de harness | 0:45 | Context engineering, archivos de instrucciones (CLAUDE.md, AGENTS.md), herramientas, permisos, sandbox, compactación de contexto, verificación automática. |
| Claude Code | 2:00 | Instalación y modos (terminal, IDE, web, desktop). CLAUDE.md y memoria, slash commands, subagentes, skills, hooks, permisos, plan mode, modo headless y uso en CI/GitHub Actions. Práctica sobre un repo real. |
| Devin | 1:15 | Agente autónomo en la nube: sesiones, Knowledge, Playbooks, integración con Slack, Jira y GitHub, DeepWiki. Cuándo delegar tareas completas. Demo de una tarea de punta a punta. |
| Codex | 1:15 | Codex CLI y Codex en la nube, AGENTS.md, tareas en paralelo, revisión de código en GitHub, sandbox y niveles de aprobación. Práctica comparada. |
| Comparativa y buenas prácticas | 0:45 | Matriz: autonomía, control, costo, privacidad, integración. Configuración compartida de equipo, versionado de instrucciones, métricas de uso. |

### 1.5 MCPs (2 hs)

Model Context Protocol como estándar para conectar agentes con sistemas externos.

| Bloque | Duración | Contenido |
|----|----|----|
| Fundamentos | 0:30 | Arquitectura cliente–servidor, tools, resources y prompts, transportes (stdio, HTTP), autenticación. |
| Uso de servidores existentes | 0:30 | Configurar MCPs de GitHub, base de datos, Jira o navegador en Claude Code, Cursor o Codex. |
| Práctica: construir un MCP | 0:45 | Crear un servidor MCP simple que exponga una API interna, con el SDK de TypeScript o Python. |
| Seguridad | 0:15 | Prompt injection, permisos mínimos, secretos, servidores de terceros confiables. |

## Módulo 2 – Metodologías adaptadas a la IA (18 hs)

Objetivo: adoptar Spec-Driven Development (SDD) como forma de trabajo, donde la especificación es el artefacto principal y el código se genera, verifica y mantiene a partir de ella.

### 2.1 Spec (4 hs)

Cómo escribir especificaciones que un agente pueda ejecutar sin ambigüedad y que un humano pueda revisar.

| Bloque | Duración | Contenido |
|----|----|----|
| De requerimiento a spec | 0:45 | Por qué el prompt suelto no escala. Spec como contrato entre negocio, equipo y agente. Niveles: visión, spec funcional, spec técnica, tareas. |
| Anatomía de una buena spec | 1:00 | Contexto, objetivos y no-objetivos, historias de usuario, criterios de aceptación (Given/When/Then, EARS), restricciones, modelo de datos, contratos de API, casos borde. |
| Spec técnica y de arquitectura | 0:45 | Decisiones (ADRs), stack, patrones, constitución o principios del proyecto, requisitos no funcionales. |
| Práctica: escribir y refinar | 1:00 | Redactar una spec con ayuda de IA, pedirle al modelo que detecte ambigüedades y huecos, iterar. |
| Revisión y versionado | 0:30 | Specs en el repo, revisión por PR, trazabilidad spec → tarea → código → test. |

### 2.2 Estimación, Análisis de impacto y Planning (4 hs)

Cómo cambian la estimación y la planificación cuando parte del trabajo lo ejecutan agentes.

| Bloque | Duración | Contenido |
|----|----|----|
| Análisis de impacto con IA | 1:00 | Usar agentes para mapear el código afectado, dependencias, contratos, datos y tests. Generar un informe de impacto y riesgos a partir de la spec. |
| Estimación en la era de agentes | 1:00 | Qué se acelera y qué no (revisión, integración, validación). Estimar por tipo de tarea y nivel de autonomía. Costos de tokens y tiempo de revisión como variables. |
| Planning y descomposición | 1:00 | Dividir la spec en tareas pequeñas, independientes y verificables. Dependencias, paralelización entre agentes, definición de done. |
| Práctica | 0:45 | Tomar la spec de 2.1, generar análisis de impacto, plan de tareas y estimación; contrastar con estimación tradicional. |
| Métricas | 0:15 | Lead time, tasa de retrabajo, porcentaje de código aceptado, costo por tarea. |

### 2.3 Implementation (4 hs)

Dos modos de implementación y cuándo usar cada uno.

| Bloque | Duración | Contenido |
|----|----|----|
| Espectro de autonomía | 0:30 | Desde autocompletado hasta agente autónomo. Criterios: riesgo, reversibilidad, cobertura de tests, criticidad del dominio. |
| Full AI | 1:15 | Agente que ejecuta tareas de punta a punta: entorno aislado, tests como oráculo, CI que valida, PR automático. Agentes en paralelo y en background. Cuándo funciona y cuándo falla. |
| Human in the loop | 1:15 | Puntos de control: aprobación del plan, revisión por paso, pair programming con el agente, permisos por acción. Técnicas de revisión eficiente de código generado. |
| Práctica comparada | 0:45 | Implementar la misma tarea en ambos modos y comparar tiempo, calidad y esfuerzo de revisión. |
| Calidad | 0:15 | Tests primero, linters, análisis estático y seguridad en el pipeline como red de contención. |

### 2.4 Herramientas para SDD (6 hs)

Herramientas y frameworks que estructuran el ciclo spec → plan → tareas → código.

| Bloque | Duración | Contenido |
|----|----|----|
| Panorama de SDD | 0:45 | Spec-first, spec-anchored y spec-as-source. Comparación de enfoques y madurez de las herramientas. |
| GitHub Spec Kit | 1:30 | Constitución del proyecto, comandos specify, plan, tasks e implement, uso con Claude Code, Copilot o Codex. Práctica guiada. |
| Kiro | 1:00 | IDE orientado a specs: requirements, design y tasks, hooks de agente, steering. Demo y práctica. |
| Otros frameworks | 1:00 | BMAD Method (roles de agentes), OpenSpec (cambios sobre specs existentes), Tessl. Cuándo conviene cada uno. |
| Flujo propio del equipo | 1:15 | Armar un flujo SDD a medida con skills, comandos y plantillas en el harness elegido. |
| Cierre | 0:30 | Elección de herramienta para el proyecto del Módulo 3. |

## Módulo 3 – Ejecución de Proyecto de Desarrollo (14 hs)

Objetivo: aplicar todo lo visto en un proyecto práctico en equipos de 3–5 personas, con un entregable funcionando al final.

### 3.1 Presentación de proyecto y entendimiento funcional (2 hs)

| Bloque | Duración | Contenido |
|----|----|----|
| Presentación del caso | 0:30 | Contexto de negocio, usuarios, problema a resolver, alcance y restricciones del proyecto. |
| Exploración funcional con IA | 0:45 | Usar IA para entrevistar al "cliente" (el instructor), detectar supuestos, mapear flujos y preguntas abiertas. |
| Armado de equipos y roles | 0:30 | Roles: product owner, arquitecto, desarrolladores, QA. Elección de harness y herramienta SDD. Setup del repo. |
| Cierre | 0:15 | Documento de entendimiento funcional validado con el instructor. |

### 3.2 Specs del ejercicio práctico (4 hs)

| Bloque | Duración | Contenido |
|----|----|----|
| Constitución y contexto | 0:45 | Principios del proyecto, stack, convenciones y archivo de instrucciones del agente (CLAUDE.md / AGENTS.md). |
| Spec funcional | 1:15 | Historias, criterios de aceptación y casos borde, redactados y refinados con IA. |
| Spec técnica | 1:15 | Arquitectura, modelo de datos, contratos de API, prototipo de UI generado con las herramientas de diseño. |
| Revisión cruzada | 0:45 | Cada equipo revisa la spec de otro buscando ambigüedades. Ajustes y aprobación. |

### 3.3 Planificación (2 hs)

| Bloque | Duración | Contenido |
|----|----|----|
| Análisis de impacto y riesgos | 0:30 | Riesgos técnicos y de dependencias, generados con agentes y validados por el equipo. |
| Descomposición en tareas | 0:45 | Tareas pequeñas y verificables, dependencias, qué se hace Full AI y qué con human in the loop. |
| Estimación y asignación | 0:30 | Estimación por tarea, reparto entre personas y agentes, plan de las 6 hs de implementación. |
| Validación del plan | 0:15 | Revisión con el instructor. |

### 3.4 Implementación (6 hs)

| Bloque | Duración | Contenido |
|----|----|----|
| Sprint 1 | 2:00 | Base del proyecto, primeras tareas, configuración de CI, tests y MCPs necesarios. |
| Checkpoint | 0:30 | Avance, bloqueos y ajustes de spec o plan. |
| Sprint 2 | 2:00 | Funcionalidades principales, agentes en paralelo, revisión de PRs. |
| Integración y QA | 0:45 | Pruebas de aceptación contra la spec, corrección de errores. |
| Demo y retrospectiva | 0:45 | Demo por equipo, métricas (tiempo, % de código generado, retrabajo) y lecciones aprendidas. |

## Evaluación y entregables

La nota final se basa en el proyecto, con entregables parciales en los Módulos 1 y 2.

| Entregable                       | Momento                    | Peso |
|----------------------------------|----------------------------|------|
| Skill propia y servidor MCP      | Fin del Módulo 1           | 15%  |
| Spec y plan de una funcionalidad | Fin del Módulo 2           | 15%  |
| Specs y plan del proyecto        | Módulo 3, unidades 3.2–3.3 | 25%  |
| Proyecto funcionando y demo      | Módulo 3, unidad 3.4       | 35%  |
| Retrospectiva con métricas       | Cierre del curso           | 10%  |

Requisitos previos de entorno: cuenta de GitHub, IDE instalado y acceso a al menos un harness (Claude Code o Codex). Devin y Kiro se cubren con demo si no hay licencias para todos.
