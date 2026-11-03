#!/usr/bin/env python3
"""
Generate all detailed, minute-by-minute Day-by-Day Step-by-Step PPTX decks
for the 52-hour course "Desarrollo de Software con IA (.NET 10 + Azure)",
plus the unified 62-slide Master Course Deck:

Outputs:
  - curriculum/2026-11-03_dia-1-paso-a-paso.pptx (11 slides)
  - curriculum/slides/dia-1-unidades-1.1-y-1.2-paso-a-paso.pptx (11 slides)
  - curriculum/slides/dia-2-unidades-1.3-y-1.4-paso-a-paso.pptx (11 slides)
  - curriculum/slides/dia-3-unidades-1.5-y-2.1-paso-a-paso.pptx (10 slides)
  - curriculum/slides/dia-4-unidades-2.2-y-2.3-paso-a-paso.pptx (10 slides)
  - curriculum/slides/dia-5-unidad-2.4-sdd-tools-paso-a-paso.pptx (9 slides)
  - curriculum/slides/dia-6-y-7-modulo-3-capstone-paso-a-paso.pptx (11 slides)
  - curriculum/2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx (62 slides, Master Deck)
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Palette
NAVY = RGBColor(15, 23, 42)        # #0F172A
DARK_BLUE = RGBColor(30, 58, 138)  # #1E3A8A
BLUE = RGBColor(37, 99, 235)       # #2563EB
TEAL = RGBColor(13, 148, 136)      # #0D9488
AMBER = RGBColor(217, 119, 6)      # #D97706
PURPLE = RGBColor(124, 58, 237)    # #7C3AED
SLATE = RGBColor(51, 65, 85)       # #334155
MUTED = RGBColor(100, 116, 139)    # #64748B
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)  # #FFFFFF
CODE_BG = RGBColor(15, 23, 42)     # #0F172A
CODE_FG = RGBColor(226, 232, 240)  # #E2E8F0
BORDER = RGBColor(203, 213, 225)   # #CBD5E1
WHITE = RGBColor(255, 255, 255)


def new_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, tag_text: str, title_text: str, subtitle_text: str = "", tag_color=BLUE, footer_note: str = ""):
    set_bg(slide, LIGHT_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.10))
    bar.fill.solid()
    bar.fill.fore_color.rgb = tag_color
    bar.line.fill.background()

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.32), Inches(4.6), Inches(0.34))
    badge.fill.solid()
    badge.fill.fore_color.rgb = tag_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = tag_text.upper()
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.72), Inches(12.1), Inches(0.55))
    tf2 = tb.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(23.5)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.font.name = "Calibri"

    if subtitle_text:
        tb3 = slide.shapes.add_textbox(Inches(0.6), Inches(1.26), Inches(12.1), Inches(0.38))
        tf3 = tb3.text_frame
        tf3.word_wrap = True
        p3 = tf3.paragraphs[0]
        p3.text = subtitle_text
        p3.font.size = Pt(12.5)
        p3.font.color.rgb = MUTED
        p3.font.name = "Calibri"

    footer = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(12.1), Inches(0.3))
    ftf = footer.text_frame
    fp = ftf.paragraphs[0]
    fp.text = footer_note or "Desarrollo de Software con IA · Programa 52 hs (.NET 10 + Azure) · VS Code / Cursor / Windsurf"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = MUTED
    fp.font.name = "Calibri"


def add_card(slide, left, top, width, height, title: str, bullets: list[str], accent=BLUE, title_size=14.5, body_size=11.8):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER
    card.line.width = Pt(1)

    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.08))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.16), Inches(width - 0.4), Inches(height - 0.26))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(title_size)
    p0.font.bold = True
    p0.font.color.rgb = NAVY
    p0.font.name = "Calibri"
    p0.space_after = Pt(6)

    for b in bullets:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(body_size)
        p.font.color.rgb = SLATE
        p.font.name = "Calibri"
        p.space_after = Pt(4)


def add_code_card(slide, left, top, width, height, title: str, code_lines: list[str], accent=TEAL):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CODE_BG
    card.line.color.rgb = accent
    card.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.14), Inches(width - 0.4), Inches(height - 0.24))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(56, 189, 248)
    p0.font.name = "Calibri"
    p0.space_after = Pt(6)

    for line in code_lines:
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(11)
        p.font.color.rgb = CODE_FG
        p.font.name = "Consolas"
        p.space_after = Pt(2)


def add_cover(prs: Presentation, badge: str, title: str, subtitle: str, pills: list[tuple[str, str]], accent=TEAL, notes: str = ""):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    set_bg(s, NAVY)

    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.95), Inches(5.8), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = DARK_BLUE
    pill.line.fill.background()
    ptf = pill.text_frame
    pp = ptf.paragraphs[0]
    pp.text = badge
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = WHITE
    pp.font.name = "Calibri"

    tb = s.shapes.add_textbox(Inches(0.9), Inches(1.65), Inches(11.5), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(37)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.font.name = "Calibri"
    p2.space_before = Pt(12)

    for idx, (k, v) in enumerate(pills):
        left = 0.9 + idx * 2.95
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(4.55), Inches(2.75), Inches(1.45))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(30, 41, 59)
        box.line.color.rgb = accent
        box.line.width = Pt(1.2)
        btf = box.text_frame
        btf.word_wrap = True
        bp1 = btf.paragraphs[0]
        bp1.text = k
        bp1.font.size = Pt(20)
        bp1.font.bold = True
        bp1.font.color.rgb = RGBColor(56, 189, 248)
        bp1.font.name = "Calibri"
        bp2 = btf.add_paragraph()
        bp2.text = v
        bp2.font.size = Pt(11.5)
        bp2.font.color.rgb = WHITE
        bp2.font.name = "Calibri"
        bp2.space_before = Pt(4)

    foot = s.shapes.add_textbox(Inches(0.9), Inches(6.55), Inches(11.5), Inches(0.5))
    ftf = foot.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "Desarrollo de Software con IA · Repositorio Semilla: GuardiaCloud.Sla (.NET 10) · VS Code, Cursor y Windsurf"
    fp.font.size = Pt(12)
    fp.font.color.rgb = RGBColor(148, 163, 184)
    fp.font.name = "Calibri"

    if notes:
        s.notes_slide.notes_text_frame.text = notes


def add_step_slide(prs: Presentation, tag: str, title: str, subtitle: str,
                   left_title: str, left_bullets: list[str],
                   right_title: str, right_items: list[str], right_is_code: bool,
                   bottom_title: str, bottom_bullets: list[str],
                   accent=BLUE, notes: str = ""):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    add_header(s, tag, title, subtitle, accent)
    add_card(s, 0.6, 1.75, 5.95, 3.35, left_title, left_bullets, accent=accent, title_size=14.5, body_size=11.8)
    if right_is_code:
        add_code_card(s, 6.78, 1.75, 5.95, 3.35, right_title, right_items, accent=TEAL)
    else:
        add_card(s, 6.78, 1.75, 5.95, 3.35, right_title, right_items, accent=TEAL, title_size=14.5, body_size=11.8)
    add_card(s, 0.6, 5.25, 12.13, 1.68, bottom_title, bottom_bullets, accent=AMBER, title_size=13.8, body_size=11.3)
    if notes:
        s.notes_slide.notes_text_frame.text = notes


# ==============================================================================
# DAY 1 (8 hs): Unidades 1.1 y 1.2 (11 slides)
# ==============================================================================
def append_day1(prs: Presentation):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_day1_helper import populate_day1
    populate_day1(prs, add_cover, add_step_slide)


# ==============================================================================
# DAY 2 (10 hs): Unidades 1.3 (Agentes/Skills) y 1.4 (Harness Engineering)
# ==============================================================================
def append_day2(prs: Presentation):
    add_cover(
        prs,
        "DÍA 2 · GUÍA PASO A PASO (10 HORAS · UNIDADES 1.3 Y 1.4)",
        "Día 2: Agentes, Agent Skills (SKILL.md)\ny Harness Engineering en .NET 10",
        "Construcción de Skills verificables, agentes en C# con Microsoft.Extensions.AI y endurecimiento de Claude Code, Codex y Devin.",
        [
            ("Bloque 1 (4 hs)", "Unidad 1.3: Loop Agéntico,\nSKILL.md y Extensions.AI"),
            ("Bloque 2 (6 hs)", "Unidad 1.4: Harness, Hooks,\nClaude Code, Codex y Devin"),
            ("6.25 hs Práctica", "2h 30m en Unidad 1.3 +\n3h 45m en Unidad 1.4"),
            ("Repositorios", "ws-m1-skills-mcp-dotnet &\nws-m2-harness-oracle-dotnet"),
        ],
        accent=BLUE,
        notes="Guion Presentador Día 2: Hoy pasamos del uso manual del IDE a empaquetar conocimiento del equipo en Skills reutilizables y a configurar el arnés (AGENTS.md + hooks deterministas).",
    )

    add_step_slide(
        prs,
        "Día 2 · Agenda Minuto a Minuto (10 hs)",
        "Estructura Completa del Día 2: Unidades 1.3 (4 hs) y 1.4 (6 hs)",
        "Cada bloque combina encuadre arquitectónico con laboratorios guiados sobre soluciones .NET 10 reales.",
        "Bloque 1 (4 hs) — Unidad 1.3: Agentes y SKILL.md",
        [
            "00:00 – 00:40 (40m) · Anatomía del loop agéntico y los 4 patrones (Chaining, Routing, Orchestrator-Workers, Evaluator-Optimizer).",
            "00:40 – 01:10 (30m) · Estándar abierto `SKILL.md` (`agentskills.io`) y *progressive disclosure*.",
            "01:10 – 01:30 (20m) · SDKs en .NET 10: `Microsoft.Extensions.AI` (`v10.11.0`) y `Microsoft.Agents.AI` (`v1.27.0`).",
            "01:30 – 03:05 (95m) · WORKSHOP 1.3A: Creación de la Skill `dotnet-minimal-api-guardian` + `verify-minimal-api.sh`.",
            "03:05 – 04:00 (55m) · WORKSHOP 1.3B: Agente `SlaTriageAgent.cs` con `FunctionInvokingChatClient`.",
        ],
        "Bloque 2 (6 hs) — Unidad 1.4: Harness Engineering",
        [
            "00:00 – 00:45 (45m) · ¿Qué es el Harness? Interoperabilidad `AGENTS.md`/`CLAUDE.md` y estudio ETH Zurich (`arXiv:2602.11988`).",
            "00:45 – 01:30 (45m) · Deep-dive en Claude Code (`v2.1.314`): `/plan`, permisos, subagentes, hooks y modo headless `claude -p`.",
            "01:30 – 02:15 (45m) · Deep-dive en OpenAI Codex (`rust-v0.166.0`) y Devin (Knowledge, Playbooks, DeepWiki).",
            "02:15 – 06:00 (3h 45m) · WORKSHOP 1.4: Poda de `AGENTS.md` (<60 líneas), Hook `PostToolUse` `.NET`, subagente revisor y duelo Claude Code vs. Codex.",
        ],
        False,
        "Salidas Concretas al Terminar el Día 2",
        [
            "1) Skill `SKILL.md` validada por script determinista + `SlaTriageAgent.cs` corriendo en xUnit (2/3 del Entregable Evaluable #1).",
            "2) Harness `.NET 10` endurecido con `AGENTS.md` curado, hook `post-edit-dotnet-hook.sh` y subagente en modo lectura.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 1.3 · 00:00 a 01:30 (90 min) · Teoría y Arquitectura",
        "Del Workflow Fijo al Agente con Herramientas y Skills Reutilizables",
        "Regla de ingeniería: usá la abstracción más simple que resuelva el problema y acotá siempre el número de iteraciones.",
        "Los 4 Patrones de Orquestación (00:00 – 00:40)",
        [
            "1. Prompt Chaining: secuencia fija de pasos con validación intermedia en código C#.",
            "2. Routing: clasificador inicial que deriva el ticket al flujo o modelo especializado.",
            "3. Orchestrator-Workers: agente coordinador que divide subtareas en subagentes con contexto limpio.",
            "4. Evaluator-Optimizer: un agente genera el artefacto y un segundo agente (u oráculo determinista) lo audita en loop.",
        ],
        "Anatomía de una Agent Skill (agentskills.io)",
        (
            ".agents/skills/dotnet-minimal-api-guardian/\n"
            "├── SKILL.md                  # <80 líneas (YAML + reglas)\n"
            "├── references/\n"
            "│   └── rfc9457-catalogo.md   # Cargado solo bajo demanda\n"
            "└── scripts/\n"
            "    └── verify-minimal-api.sh # Oráculo ejecutable (exit 0/1)"
        ).splitlines(),
        True,
        "Por qué el Progressive Disclosure ahorra Miles de Tokens",
        [
            "El agente lee al inicio únicamente el `name` y `description` del frontmatter YAML (~50 tokens). Solo cuando el usuario pide crear o auditar un endpoint Minimal API, el agente abre `SKILL.md` y ejecuta `verify-minimal-api.sh`.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 1.3 · Workshop Paso a Paso · 01:30 a 03:05 (95 min)",
        "Workshop 1.3 (Fase 1): Construcción de la Skill `dotnet-minimal-api-guardian`",
        "Trabajamos sobre `workshops/ws-m1-skills-mcp-dotnet/starter/`.",
        "Pasos Guiados para las Duplas (95 min)",
        [
            "Paso 1 (20m): Correr `./.agents/skills/dotnet-minimal-api-guardian/scripts/verify-minimal-api.sh` en `starter/` y observar por qué falla la Skill incompleta.",
            "Paso 2 (35m): Completar el frontmatter YAML (`name`, `description` accionable) y las 4 reglas obligatorias de arquitectura en `SKILL.md` (`ProblemDetails` RFC 9457, `TimeProvider`, `CancellationToken`, enlace a `references/rfc9457-catalogo-errores.md`).",
            "Paso 3 (25m): Hacer que el agente en VS Code / Cursor / Claude Code aplique la Skill sobre un endpoint nuevo y verifique con el script.",
            "Paso 4 (15m): Confirmar salida `[OK] Skill verificada` con código de retorno `0`.",
        ],
        "Fragmento Clave de SKILL.md Completado",
        [
            "---",
            "name: dotnet-minimal-api-guardian",
            "description: >-",
            "  Aplica y verifica estándares de arquitectura para",
            "  ASP.NET Core Minimal APIs en .NET 10 (RFC 9457,",
            "  TimeProvider y CancellationToken).",
            "---",
            "## Reglas Obligatorias",
            "1. Errores 4xx/5xx usan TypedResults.Problem (RFC 9457)",
            "   con extensions['errorCode'] del catálogo oficial.",
            "2. Prohibido DateTime.Now/UtcNow; inyectar TimeProvider.",
            "3. Ejecutar siempre ./scripts/verify-minimal-api.sh",
        ],
        True,
        "Criterio de Verificación (30 puntos de la Rúbrica del Módulo 1)",
        [
            "El script `./scripts/verify-minimal-api.sh` y el test `SkillManifestTests` en `dotnet test` deben pasar en verde.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 1.3 · Workshop Paso a Paso · 03:05 a 04:00 (55 min)",
        "Workshop 1.3 (Fase 3): Agente Programático en C# con `Microsoft.Extensions.AI`",
        "Implementación de `SlaTriageAgent.cs` conectando herramientas C# tipadas mediante `IChatClient`.",
        "Pasos Guiados para las Duplas (55 min)",
        [
            "Paso 1 (15m): Inspeccionar `src/GuardiaCloud.Sla.McpServer/Agent/SlaTriageAgent.cs` y el pipeline `ChatClientBuilder` de `Microsoft.Extensions.AI` (`v10.11.0`).",
            "Paso 2 (25m): Configurar `.UseFunctionInvocation(c => { c.MaximumIterationsPerRequest = 4; })` y registrar las herramientas con `AIFunctionFactory.Create`.",
            "Paso 3 (15m): Ejecutar `dotnet test --filter SlaTriageAgent` y verificar cómo el agente invoca primero `get_client_sla_policy`, luego `inspect_incident_sla_status` y sintetiza el diagnóstico.",
        ],
        "Implementación en SlaTriageAgent.cs (.NET 10)",
        [
            "public static IChatClient CreateAgent(IChatClient innerClient) =>",
            "    new ChatClientBuilder(innerClient)",
            "        .UseFunctionInvocation(options => {",
            "            options.MaximumIterationsPerRequest = 4;",
            "            options.AllowConcurrentInvocation = false;",
            "        })",
            "        .Build();",
            "",
            "var chatOptions = new ChatOptions {",
            "    Tools = [",
            "        AIFunctionFactory.Create(SlaMcpTools.GetClientSlaPolicy),",
            "        AIFunctionFactory.Create(SlaMcpTools.InspectIncidentSlaStatus)",
            "    ]",
            "};",
        ],
        True,
        "Aprendizaje Clave de Ingeniería .NET",
        [
            "Con `Microsoft.Extensions.AI`, la lógica de tus herramientas vive en métodos C# estáticos o servicios DI fuertemente tipados que podés exponer simultáneamente como `AIFunction` en proceso y como `[McpServerTool]` por protocolo MCP.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 1.4 · 00:00 a 01:30 (90 min) · Harness Engineering & Claude Code",
        "Ingeniería del Arnés: `AGENTS.md`, Evidencia ETH Zurich y Claude Code",
        "Cómo diseñar el entorno que envuelve al modelo para maximizar aciertos y minimizar tokens desperdiciados.",
        "Hallazgos Empíricos (ETH Zurich `arXiv:2602.11988`)",
        [
            "Los archivos `AGENTS.md` largos o autogenerados por `/init` reducen la tasa de resolución entre 0.5% y 2% y aumentan el consumo de tokens un 20–23%.",
            "¿Por qué? Porque llenan la ventana de atención con descripciones obvias de carpetas que el agente puede descubrir con `glob`/`grep`.",
            "Qué SÍ debe ir en `AGENTS.md` (<60–80 líneas): comandos exactos de compilación/test, invariantes de arquitectura no obvias y prohibiciones explícitas.",
            "Puente universal: `AGENTS.md` en la raíz + `CLAUDE.md` con `@AGENTS.md`.",
        ],
        "Dominio Operativo de Claude Code (v2.1.314)",
        [
            "1. Modo `/plan` (`Shift+Tab`): explorar y acordar diseño antes de tocar archivos.",
            "2. Gestión de higiene de contexto: `/compact` con foco explícito al terminar una subtarea y `/clear` entre tickets independientes.",
            "3. Subagentes (`.claude/agents/*.md`): aislar búsquedas ruidosas o auditorías de código en una ventana de contexto separada.",
            "4. Hooks (`PreToolUse`, `PostToolUse`, `Stop`): validación determinista automática con scripts de shell.",
        ],
        False,
        "Regla Práctica para Equipos .NET",
        [
            "Si una regla puede verificarse con el compilador C#, un analizador Roslyn, `NetArchTest` o un hook `PostToolUse`, automatizala en el arnés en lugar de pedirle 'por favor' al LLM en un párrafo de texto.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 1.4 · 01:30 a 02:15 (45 min) · OpenAI Codex y Devin",
        "Comparativa de Harnesses: Claude Code vs. OpenAI Codex vs. Devin",
        "Criterios de selección en una consultora de software según el tipo de tarea, privacidad y paralelismo.",
        "OpenAI Codex (`rust-v0.166.0` · CLI + Cloud)",
        [
            "CLI nativa en Rust de altísima velocidad + ejecución asíncrona de tareas en contenedores cloud.",
            "Tres niveles de sandbox explícitos:",
            "  • `read-only`: auditorías, análisis de impacto y Q&A.",
            "  • `workspace-write`: desarrollo estándar dentro del repo sin red externa.",
            "  • `danger-full-access`: solo para entornos efímeros aislados.",
            "Lee nativamente `AGENTS.md` en cascada desde la raíz hasta subdirectorios.",
        ],
        "Devin (Cognition · Agente Cloud Orientado a Tickets)",
        [
            "Sesiones cloud completas con navegador, terminal y editor propios, integradas con Jira / Linear / GitHub / Azure DevOps.",
            "Tres primitivas clave para consultoría:",
            "  • *Knowledge*: lecciones aprendidas activadas por contexto.",
            "  • *Playbooks*: recetas paso a paso para tareas repetitivas (ej. actualizar paquetes NuGet o migrar endpoints a RFC 9457).",
            "  • *DeepWiki*: indexación arquitectónica automática del repositorio.",
        ],
        False,
        "Matriz de Selección Rápida",
        [
            "Diseño interactivo / Refactoring complejo en vivo → IDE (VS Code / Cursor / Windsurf) o Claude Code en `/plan` · Tareas acotadas con buen oráculo de tests → Codex / Worktrees · Tickets repetitivos bien especificados → Devin con Playbook.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 1.4 · Workshop Paso a Paso · 02:15 a 04:20 (125 min)",
        "Workshop 1.4 (Fases 1 y 2): Poda de `AGENTS.md` y Hook Determinista `.NET`",
        "Trabajamos sobre `workshops/ws-m2-harness-oracle-dotnet/starter/` (`GuardiaCloud.Sla.HarnessLab.sln`).",
        "Fase 1 (60m): Curación Quirúrgica de `AGENTS.md`",
        [
            "En `starter/AGENTS.md` hay un archivo inflado de >150 líneas con historia irrelevante y reglas ambiguas.",
            "Las duplas lo podan a **menos de 55 líneas** conservando solo: comandos exactos (`dotnet build --no-restore`, `dotnet test`), invariantes de capas (`Domain` sin dependencias externas), contrato RFC 9457 y uso de `TimeProvider`.",
            "Verifican que `CLAUDE.md` importe `@AGENTS.md`.",
        ],
        "Fase 2 (65m): Hook PostToolUse en .claude/settings.json",
        [
            "# scripts/post-edit-dotnet-hook.sh",
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "echo \"[Hook .NET] Verificando compilación y oráculo...\"",
            "dotnet build GuardiaCloud.Sla.HarnessLab.sln \\",
            "  --no-restore -v quiet /p:TreatWarningsAsErrors=true",
            "dotnet test GuardiaCloud.Sla.HarnessLab.sln \\",
            "  --no-build -v minimal",
            "echo \"[Hook .NET] OK: Compilación y tests en verde.\"",
        ],
        True,
        "Demostración del Bucle de Autocorrección",
        [
            "Los alumnos le piden al agente un cambio que rompe un tipo en C#; el hook `PostToolUse` devuelve código de salida != 0 con el error exacto de MSBuild y el agente lo corrige automáticamente antes de devolver el turno.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 1.4 · Workshop Paso a Paso · 04:20 a 06:00 (100 min)",
        "Workshop 1.4 (Fases 3 y 4): Subagente Revisor y Duelo Claude Code vs. Codex",
        "Aislamiento de contexto mediante subagentes de solo lectura y evaluación comparativa entre harnesses.",
        "Fase 3 (50m): Subagente Revisor en `.claude/agents/`",
        [
            "Configurar `.claude/agents/dotnet-arch-reviewer.md` restringiendo sus herramientas a `Read, Grep, Glob`.",
            "Su misión es auditar cualquier diff contra las reglas de `AGENTS.md` devolviendo hallazgos con `archivo:línea` y severidad (`BLOCKER`, `WARNING`).",
            "Probar al subagente sobre `LegacyVibeCodedHelper.cs` y confirmar que detecta la violación de capas sin tocar archivos.",
        ],
        "Definición del Subagente (.claude/agents/dotnet-arch-reviewer.md)",
        [
            "---",
            "name: dotnet-arch-reviewer",
            "description: Audita cambios C# contra AGENTS.md en modo lectura.",
            "tools: Read, Grep, Glob",
            "---",
            "Sos un Arquitecto .NET 10 Senior.",
            "Revisá los archivos modificados verificando:",
            "1. Cero referencias de Domain hacia Infrastructure/AspNetCore.",
            "2. Uso de TimeProvider y CancellationToken.",
            "3. Errores HTTP devueltos como ProblemDetails RFC 9457.",
        ],
        True,
        "Fase 4 (50m): Duelo Práctico Claude Code vs. OpenAI Codex",
        [
            "Cada integrante de la dupla resuelve el mismo requerimiento sobre el repositorio endurecido usando un harness distinto y registran tiempo total, tokens consumidos y calidad del diff.",
        ],
        accent=PURPLE,
    )


# ==============================================================================
# DAY 3 (6 hs): Unidades 1.5 (MCP en C#) y 2.1 (Spec EARS/GWT)
# ==============================================================================
def append_day3(prs: Presentation):
    add_cover(
        prs,
        "DÍA 3 · GUÍA PASO A PASO (6 HORAS · UNIDADES 1.5 Y 2.1)",
        "Día 3: Servidores MCP en C# (.NET 10)\ny Especificaciones Ejecutables (SDD)",
        "Cerramos el Módulo 1 con el Servidor MCP en C# (15% nota) y abrimos el Módulo 2 con Especificaciones EARS y Given/When/Then.",
        [
            ("Bloque 1 (2 hs)", "Unidad 1.5: MCP Server C#\n(ModelContextProtocol v2.3)"),
            ("Entregable #1", "Cierre Módulo 1 (15% nota):\nSkill + MCP + Agente C#"),
            ("Bloque 2 (4 hs)", "Unidad 2.1: Specs EARS,\nGWT y Spec Critic"),
            ("Repositorios", "ws-m1-skills-mcp-dotnet &\nws-m2-sdd-dotnet"),
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 1.5 · 00:00 a 00:45 (45 min) · Arquitectura y Seguridad MCP en .NET",
        "Model Context Protocol (MCP) con el SDK Oficial de C# (`v2.3.0`)",
        "Cómo exponer lógica de dominio y telemetría .NET a cualquier agente sin abrir brechas de inyección de prompts.",
        "Conceptos Clave y Configuración en C# (45 min)",
        [
            "Paquete NuGet oficial: `ModelContextProtocol` (`v2.3.0`) con soporte nativo para `.NET 10` e inyección de dependencias (`Microsoft.Extensions.Hosting`).",
            "Trampa número 1 en transporte `stdio`: cualquier `Console.WriteLine` corrompe el stream JSON-RPC. Configurar siempre `LogToStandardErrorThreshold = LogLevel.Trace`.",
            "Seguridad defensiva ante *Indirect Prompt Injection*: nunca devolver textos libres ingresados por usuarios externos sin sanitizar directivas de secuestro (`IGNORE PREVIOUS INSTRUCTIONS`, `SYSTEM OVERRIDE`).",
        ],
        "Host MCP en Program.cs (.NET 10 + stdio)",
        [
            "var builder = Host.CreateApplicationBuilder(args);",
            "builder.Logging.AddConsole(opts => {",
            "    opts.LogToStandardErrorThreshold = LogLevel.Trace;",
            "});",
            "builder.Services.AddSingleton<SlaRepository>();",
            "builder.Services",
            "    .AddMcpServer()",
            "    .WithStdioServerTransport()",
            "    .WithToolsFromAssembly();",
            "await builder.Build().RunAsync();",
        ],
        True,
        "Servidores MCP Listos para Usar en Consultoría .NET + Azure",
        [
            "Azure MCP Server (`microsoft/mcp`), GitHub MCP / Azure DevOps MCP y PostgreSQL / SQL Server MCP en modo solo lectura para diagnóstico seguro.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 1.5 · Workshop Evaluable #1 · 00:45 a 02:00 (75 min)",
        "Taller 1.5: Implementación de `SlaMcpTools.cs` y Entrega del Módulo 1 (15%)",
        "Fase 2 y cierre del paquete `workshops/ws-m1-skills-mcp-dotnet`.",
        "Pasos Guiados del Taller MCP (75 min)",
        [
            "Paso 1 (25m): Implementar `inspect_incident_sla_status` en `SlaMcpTools.cs`, calculando el ratio de SLA y aplicando `SanitizeUntrustedNotes` para neutralizar el ataque sembrado en `INC-2026-1002`.",
            "Paso 2 (20m): Implementar `validate_rfc9457_contract` verificando que todo payload de error cumpla RFC 9457 y use códigos oficiales (`SLA-400-*`, `SLA-404-*`, `SLA-409-*`, `SLA-422-*`).",
            "Paso 3 (15m): Ejecutar `dotnet test` y confirmar los **6 tests del workshop en verde**.",
            "Paso 4 (15m): Conectar el servidor mediante `.mcp.json` en VS Code / Cursor / Claude Code y hacer la demo cruzada.",
        ],
        "Sanitización Anti-Inyección en SlaMcpTools.cs",
        [
            "public static string SanitizeUntrustedNotes(string raw) {",
            "    if (string.IsNullOrWhiteSpace(raw)) return string.Empty;",
            "    string[] patterns = [",
            '        "IGNORE PREVIOUS INSTRUCTIONS",',
            '        "SYSTEM OVERRIDE",',
            '        "APPROVE FULL CREDIT"',
            "    ];",
            "    foreach (var p in patterns) {",
            "        if (raw.Contains(p, StringComparison.OrdinalIgnoreCase))",
            '            return "[REDACTED: POTENTIAL PROMPT INJECTION]";',
            "    }",
            "    return raw;",
            "}",
        ],
        True,
        "Hito de Evaluación: Entrega Calificada #1 (15% de la Nota Final del Curso)",
        [
            "Al finalizar la hora 2 del Día 3, cada dupla entrega su repositorio `ws-m1-skills-mcp-dotnet` con `./scripts/verify-minimal-api.sh` OK y `dotnet test` (6/6 passed).",
        ],
        accent=PURPLE,
    )

    add_step_slide(
        prs,
        "Unidad 2.1 · 00:00 a 01:30 (90 min) · El Arte de Especificar (SDD)",
        "Por Qué Falla el 'Vibe Coding' y Cómo Escribir Specs Ejecutables (EARS + GWT)",
        "La especificación es el código fuente de más alto nivel cuando trabajamos con agentes.",
        "Evidencia Científica y Jerarquía SDD (00:00 – 00:45)",
        [
            "Larbi et al. (`arXiv:2507.20439`): las ambigüedades en el prompt/spec derrumban Pass@1 entre 20 y 40 puntos porcentuales.",
            "SWE-EVO (`arXiv:2512.18470`): >60% de los fallos en evolución de sistemas reales se deben a requisitos implícitos no especificados.",
            "Pirámide SDD:",
            "  1. `constitution.md` / `AGENTS.md` (Invariantes globales).",
            "  2. `spec.md` (Requisitos funcionales EARS + escenarios Given/When/Then).",
            "  3. `plan.md` (Contratos HTTP, DTOs C#, códigos RFC 9457, estrategia de pruebas).",
        ],
        "Los 5 Patrones de Sintaxis EARS (00:45 – 01:30)",
        [
            "1. Ubiquitous: THE SYSTEM SHALL registrar toda marca de tiempo en UTC.",
            "2. Event-Driven: WHEN se registra una pausa, THE SYSTEM SHALL recalcular el tiempo neto.",
            "3. State-Driven: WHILE un incidente esté en estado Resolved, THE SYSTEM SHALL usar ResolvedAtUtc como fin.",
            "4. Unwanted Behavior: IF `EndsAtUtc <= StartsAtUtc`, THEN THE SYSTEM SHALL devolver HTTP 400 (`SLA-400-INVALID-PAUSE-WINDOW`).",
            "5. Complex (WHEN + WHILE + IF): combina evento, estado y condición de borde sin ambigüedad.",
        ],
        False,
        "Técnica Clave: El Agente como Crítico Adversarial (*Spec Critic*)",
        [
            "Antes de diseñar la solución, le damos al agente el pedido crudo del cliente y le pedimos que actúe como un ingeniero QA adversarial buscando contradicciones, huecos de huso horario y límites no definidos.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 2.1 · Workshop Paso a Paso · 01:30 a 02:35 (65 min)",
        "Taller 2.1 (Parte A): Auditoría Adversarial (*Spec Critic*) y Role-Play con Cliente",
        "Primera parte del paquete `workshops/ws-m2-sdd-dotnet` sobre `GuardiaCloud.Sla.sln`.",
        "Paso 1 (35m): Prompt Spec Critic sobre el Brief Ambiguo",
        [
            "Las duplas abren `starter/brief-cliente-ambiguo.md` (*'Queremos pausar el reloj de SLA cuando esperamos al cliente'*).",
            "Le piden al agente que actúe como un **QA / Arquitecto Adversarial** buscando huecos de huso horario, solapamientos y límites no definidos.",
            "Resultado esperado: lista priorizada de las **7 ambigüedades críticas** sin escribir una sola línea de código C#.",
        ],
        "Las 7 Ambigüedades que Deben Descubrir las Duplas",
        [
            "1. ¿Qué pasa si dos pausas se solapan parcialmente?",
            "   -> Se fusionan (unión matemática), nunca se suman doble.",
            "2. ¿Qué pasa con una pausa que empieza antes de OpenedAtUtc?",
            "   -> Se recorta al intervalo [OpenedAtUtc, EffectiveEndUtc].",
            "3. ¿Cuáles son los motivos válidos (enum cerrado)?",
            "   -> Solo WaitingForCustomer y MaintenanceWindow.",
            "4. ¿Hay tope de pausa en incidentes críticos P1?",
            "   -> Máximo 30 min acumulados (SLA-422-P1-PAUSE-CAP-EXCEEDED).",
        ],
        True,
        "Paso 2 (30m): Entrevista en Vivo al 'Gerente de Operaciones'",
        [
            "El presentador responde únicamente las preguntas específicas que formulan las duplas usando la hoja oficial de `02-GUIA-FACILITADOR-Y-RUBRICA.md`.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 2.1 · Workshop Paso a Paso · 02:35 a 04:00 (85 min)",
        "Taller 2.1 (Parte B): Redacción de `spec.md` (EARS/GWT) y `plan.md` (.NET 10)",
        "Transformación de las respuestas del negocio en contratos formales verificables por máquinas y pares.",
        "Paso 3 (50m): Redacción de `spec.md` y `plan.md`",
        [
            "Escribir `specs/001-sla-pause-windows/spec.md` con los requisitos en notación EARS y los escenarios de aceptación Given/When/Then con marcas de tiempo UTC exactas.",
            "Escribir `specs/001-sla-pause-windows/plan.md` especificando el endpoint `POST /api/incidents/{id}/pauses`, los DTOs en C# y el catálogo de códigos RFC 9457.",
        ],
        "Especificación Técnica en plan.md (Contratos C# 13)",
        [
            "public enum PauseReason { WaitingForCustomer, MaintenanceWindow }",
            "",
            "public sealed record RegisterPauseWindowRequest(",
            "    PauseReason Reason,",
            "    DateTimeOffset StartsAtUtc,",
            "    DateTimeOffset EndsAtUtc);",
            "",
            "// Códigos ProblemDetails RFC 9457 obligatorios:",
            "// - SLA-400-INVALID-PAUSE-WINDOW (EndsAtUtc <= StartsAtUtc)",
            "// - SLA-400-UNSUPPORTED-PAUSE-REASON",
            "// - SLA-422-P1-PAUSE-CAP-EXCEEDED (> 30 min en P1)",
        ],
        True,
        "Paso 4 (35m): Peer-Review Cruzado y Cierre del Día 3",
        [
            "Cada dupla audita el `spec.md` y `plan.md` de otro equipo verificando que haya **cero marcadores `[NEEDS CLARIFICATION]`** pendientes.",
        ],
        accent=TEAL,
    )


# ==============================================================================
# DAY 4 (8 hs): Unidades 2.2 (Impacto/DAG) y 2.3 (Full AI vs. HITL + Oráculo)
# ==============================================================================
def append_day4(prs: Presentation):
    add_cover(
        prs,
        "DÍA 4 · GUÍA PASO A PASO (8 HORAS · UNIDADES 2.2 Y 2.3)",
        "Día 4: Análisis de Impacto, Grafos DAG\ne Implementación Full AI vs. HITL",
        "Descomposición de tareas sin conflictos de merge, construcción del oráculo con NetArchTest y laboratorio comparativo en git worktrees.",
        [
            ("Bloque 1 (4 hs)", "Unidad 2.2: Impacto Brownfield,\nEstimación y DAG tasks.md"),
            ("Bloque 2 (4 hs)", "Unidad 2.3: Oráculo NetArchTest\ny HITL vs. Full AI"),
            ("5.0 hs Práctica", "2h 30m en Unidad 2.2 +\n2h 30m en Unidad 2.3"),
            ("Repositorios", "ws-m2-sdd-dotnet &\nws-m2-harness-oracle-dotnet"),
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 2.2 · 00:00 a 01:30 (90 min) · Impacto, Estimación y DAG",
        "Cómo Planificar para Múltiples Desarrolladores y Agentes sin Colisiones",
        "Evitamos la trampa del 27.67% de conflictos de merge en PRs paralelos (estudio AgenticFlict).",
        "Análisis de Impacto y Grafos Acíclicos (00:00 – 00:45)",
        [
            "Antes de generar tareas, corremos al agente en modo *Read-Only / Plan* para inventariar qué archivos `.cs`, contratos OpenAPI y tests existentes se ven afectados.",
            "Regla de oro del DAG (`tasks.md`):",
            "  • Fase 1 (Secuencial): Congelar contratos DTO/interfaces en `Domain` y escribir los tests de aceptación en rojo.",
            "  • Fase 2 (Paralela `[P]`): Tareas con **conjuntos de archivos estrictamente disjuntos**.",
        ],
        "Recalibrando la Estimación con IA (00:45 – 01:30)",
        [
            "La IA reduce entre 50% y 70% el tiempo de *escritura inicial*, pero NO reduce automáticamente el tiempo de *verificación, code review y pruebas de integración*.",
            "Plantilla de estimación del curso por tarea:",
            "  1. Complejidad del Oráculo (¿Fácil o difícil de testear?).",
            "  2. Modo sugerido (`HITL` vs. `Full AI`).",
            "  3. Tiempo estimado de generación vs. tiempo de revisión humana.",
        ],
        False,
        "Fenómeno 'Workslop' (BetterUp / Stanford) y Cómo Prevenirlo",
        [
            "Un PR de 1.500 líneas generado sin descomposición traslada ~2 horas de carga cognitiva al revisor. Tareas atómicas (<150 LOC) con su propio comando `dotnet test --filter` se revisan en 5 minutos.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 2.2 · Workshop Paso a Paso · 01:30 a 04:00 (150 min)",
        "Taller 2.2: Mapa de Impacto, Construcción del DAG `tasks.md` y Estimación",
        "Guía completa en `curriculum/unidades/unidad-2.2-impacto-estimacion-y-dag-dotnet.md`.",
        "Pasos Guiados del Taller 2.2 (150 min)",
        [
            "Paso 1 (40m) — Análisis de Impacto en Modo Lectura: auditar `GuardiaCloud.Sla.sln` contra `spec.md` y `plan.md` sin modificar archivos.",
            "Paso 2 (50m) — Construcción de `tasks.md` (DAG): dividir en Fase 1 secuencial (`T001` contratos, `T002` tests en rojo) y Fase 2 paralela `[P]` (`T003` algoritmo en `SlaCalculator.cs`, `T004` endpoint en `Program.cs`).",
            "Paso 3 (35m) — Tabla de Estimación en 2 Columnas: estimar tiempo tradicional vs. generación con IA + verificación humana.",
            "Paso 4 (25m) — Auditoría Cruzada de Colisiones: comprobar que dos tareas `[P]` no toquen el mismo archivo `.cs`.",
        ],
        "Grafo de Tareas en specs/001-sla-pause-windows/tasks.md",
        [
            "## Fase 1: Contratos y Oráculo en Rojo (Secuencial)",
            "- [ ] T001 [HITL] Crear PauseReason y SlaPauseWindow",
            "  Archivos: src/GuardiaCloud.Sla.Domain/SlaPauseWindow.cs",
            "- [ ] T002 [HITL] Crear tests xUnit de bordes y RFC 9457",
            "  Archivos: tests/GuardiaCloud.Sla.Tests/PauseTests.cs",
            "",
            "## Fase 2: Ejecución Paralela en Worktrees [P]",
            "- [ ] T003 [P] [Full AI] Unión matemática de intervalos",
            "  Archivos exclusivos: Domain/SlaCalculator.cs",
            "- [ ] T004 [P] [HITL] Endpoint POST /pauses + RFC 9457",
            "  Archivos exclusivos: Api/Program.cs",
        ],
        True,
        "Artefacto Entregable de la Unidad 2.2",
        [
            "Informe de Impacto Brownfield + `specs/001-sla-pause-windows/tasks.md` validado sin conflictos de archivos.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 2.3 · 00:00 a 01:30 (90 min) · Oráculos .NET y Autonomía",
        "Full AI vs. Human-in-the-Loop (HITL) y el Oráculo de 4 Capas en .NET 10",
        "Un agente autónomo solo es tan confiable como el oráculo determinista que valida su salida.",
        "¿Cuándo Elegir HITL vs. Full AI en `git worktree`?",
        [
            "Elegí **Human-in-the-Loop (HITL)** cuando: hay reglas financieras/regulatorias críticas, cambios de esquema de base de datos o contratos públicos aún en discusión.",
            "Elegí **Full AI (Autónomo en `git worktree` aislado)** cuando: la especificación está cerrada, los contratos están congelados y ya escribiste los tests de aceptación + reglas `NetArchTest`.",
        ],
        "El Oráculo Determinista de 4 Capas en .NET 10",
        [
            "// 1. Compilador C# 13: TreatWarningsAsErrors=true",
            "// 2. NetArchTest.Rules (v1.3.2): Fitness Functions",
            "Types.InAssembly(typeof(Incident).Assembly)",
            "    .ShouldNot().HaveDependencyOnAny(",
            '        "GuardiaCloud.Sla.Infrastructure",',
            '        "Microsoft.AspNetCore");',
            "// 3. WebApplicationFactory<Program> + FakeTimeProvider",
            "// 4. Validación de contrato ProblemDetails RFC 9457",
        ],
        True,
        "Por qué los Tests Funcionales Solos No Alcanzan con Agentes Autónomos",
        [
            "Sin `NetArchTest.Rules`, un agente en modo Full AI puede acoplar `Domain` directamente con `Infrastructure` o `HttpContext` para hacer pasar el test funcional en menos pasos.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 2.3 · Workshop Paso a Paso · 01:30 a 04:00 (150 min)",
        "Taller 2.3: Fitness Functions `NetArchTest` y Laboratorio HITL vs. Full AI",
        "Ejecución sobre `workshops/ws-m2-harness-oracle-dotnet` (`GuardiaCloud.Sla.HarnessLab.sln`).",
        "Pasos Guiados del Laboratorio (150 min)",
        [
            "Paso 1 (45m) — Oráculo Arquitectónico: implementar las 3 reglas en `ArchitectureFitnessTests.cs`, detectar la violación en `LegacyVibeCodedHelper.cs`, eliminarla y verificar `dotnet test`.",
            "Paso 2 (45m) — Tarea A en modo HITL: implementar el cálculo de créditos financieros mensuales por SLA incumplido (`SlaCreditCalculator`) con redondeo bancario y revisión humana paso a paso.",
            "Paso 3 (40m) — Tarea B en modo Full AI (`git worktree`): crear un worktree paralelo, dejar los tests de `ShiftHandoverSummary` en rojo y lanzar al agente autónomo hasta que los 7 tests pasen.",
            "Paso 4 (20m) — Debrief de Métricas: completar `comparativa-hitl-vs-full-ai.md`.",
        ],
        "Comandos del Laboratorio con git worktree y dotnet test",
        [
            "# Crear worktree aislado para el agente en modo Full AI",
            "$ git worktree add ../harness-full-ai -b feat/shift-summary",
            "$ cd ../harness-full-ai",
            "",
            "# Ejecutar el oráculo completo (Arquitectura + API)",
            "$ dotnet test GuardiaCloud.Sla.HarnessLab.sln",
            "Passed! - Failed: 0, Passed: 7, Total: 7 (353 ms)",
            " ✓ 3 NetArchTest.Rules fitness functions",
            " ✓ 2 HITL SlaCreditCalculator tests",
            " ✓ 2 Full AI ShiftHandoverSummary endpoint tests",
        ],
        True,
        "Artefacto Entregable de la Unidad 2.3",
        [
            "Solución `GuardiaCloud.Sla.HarnessLab.sln` con los 7 tests en verde + informe empírico `comparativa-hitl-vs-full-ai.md`.",
        ],
        accent=PURPLE,
    )


# ==============================================================================
# DAY 5 (6 hs): Unidad 2.4 (Herramientas para SDD: Spec Kit y OpenSpec)
# ==============================================================================
def append_day5(prs: Presentation):
    add_cover(
        prs,
        "DÍA 5 · GUÍA PASO A PASO (6 HORAS · UNIDAD 2.4)",
        "Día 5: Herramientas para SDD en .NET 10\n(GitHub Spec Kit v1.2.5 y OpenSpec v1.15.0)",
        "Jornada intensiva de laboratorio cerrando el Módulo 2 y el Entregable Evaluable #2 (15% de la nota final).",
        [
            ("00:00 – 01:30", "Taxonomía SDD, Spec Kit,\nOpenSpec, Kiro, BMAD, Tessl"),
            ("01:30 – 03:45", "Lab Parte A: Bugfix y Feature\ncon Spec Kit v1.2.5"),
            ("03:45 – 05:00", "Lab Parte B: Delta Brownfield\ncon OpenSpec v1.15.0"),
            ("05:00 – 06:00", "Cierre y Calificación del\nEntregable #2 (15% nota)"),
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 2.4 · 00:00 a 01:30 (90 min) · Ecosistema de Herramientas SDD",
        "GitHub Spec Kit (`v1.2.5`) + OpenSpec (`v1.15.0`): El Dúo para Consultoría .NET",
        "Cómo combinar especificaciones estructuradas de nuevas capacidades con deltas quirúrgicos en sistemas brownfield.",
        "GitHub Spec Kit (`v1.2.5` · CLI `specify`)",
        [
            "Estructura: `.specify/memory/constitution.md` y `specs/001-feature/{spec,plan,tasks}.md`.",
            "Skills nativas del flujo:",
            "  • `/speckit-constitution` → fija invariantes `.NET 10`.",
            "  • `/speckit-specify` → genera requisitos EARS y GWT.",
            "  • `/speckit-plan` y `/speckit-tasks` → diseño técnico y DAG.",
            "  • `/speckit-implement` y **`/speckit-converge`** → implementa y audita desviaciones contra la spec.",
            "Extensión `bug`: `/speckit-bug-assess`, `/speckit-bug-fix`, `/speckit-bug-test`.",
        ],
        "Fission-AI OpenSpec (`v1.15.0` · Deltas Brownfield)",
        [
            "En sistemas empresariales existentes, el desafío es modificar reglas vigentes sin perder la historia de qué cambió y por qué.",
            "Estructura: `openspec/specs/<capacidad>/spec.md` (verdad actual) + `openspec/changes/<cambio>/` (`proposal.md`, `tasks.md` y delta `ADDED / MODIFIED / REMOVED`).",
            "Comandos: `/opsx:explore` → `/opsx:propose` → `/opsx:apply` → `/opsx:archive` (fusiona el delta en la spec viva).",
        ],
        False,
        "Comparativa con AWS Kiro, BMAD Method (`v6.12.4`) y Tessl (`tessl.io`)",
        [
            "Revisamos cómo AWS Kiro integra `.kiro/specs/` en el IDE, cómo BMAD modela roles multi-agente (PM, Architect, Dev, QA) y hacia dónde apunta el enfoque *Spec-as-Source* de Tessl.",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Unidad 2.4 · Workshop Paso a Paso · 01:30 a 03:45 (135 min)",
        "Taller 2.4 (Fases 1 y 2): Bugfix y Feature Completa con GitHub Spec Kit `v1.2.5`",
        "Trabajamos sobre `workshops/ws-m2-sdd-dotnet` (`GuardiaCloud.Sla.sln`).",
        "Fase 1 (45m): Flujo `/speckit-bug-*` sobre `ResolvedAtUtc`",
        [
            "Ejecutar `/speckit-bug-assess` para documentar la causa raíz del bug de incidentes resueltos en `.specify/bugs/resolved-sla-breach-drift/report.md`.",
            "Aplicar el fix en `SlaCalculator.cs` (`/speckit-bug-fix`) y agregar el test de regresión en `SlaEndpointsTests.cs` (`/speckit-bug-test`).",
        ],
        "Fase 2 (90m): Implementación y `/speckit-converge`",
        [
            "# Estructura generada por Spec Kit en el repo",
            ".specify/",
            "├── memory/constitution.md",
            "└── bugs/resolved-sla-breach-drift/report.md",
            "specs/001-sla-pause-windows/",
            "├── spec.md    # Requisitos EARS + Escenarios GWT",
            "├── plan.md    # Contratos Minimal API + RFC 9457",
            "└── tasks.md   # Grafo DAG ejecutado por el agente",
            "",
            "# Auditoría de convergencia código <-> spec:",
            "/speckit-converge",
        ],
        True,
        "Qué Verifica `/speckit-converge`",
        [
            "Compara cada criterio de aceptación de `spec.md` y cada código de error de `plan.md` contra el código C# y los tests realmente implementados, detectando omisiones antes de abrir el PR.",
        ],
        accent=TEAL,
    )

    add_step_slide(
        prs,
        "Unidad 2.4 · Workshop Evaluable #2 · 03:45 a 06:00 (135 min)",
        "Taller 2.4 (Fases 3 y 4): Delta Brownfield con OpenSpec `v1.15.0` y Entrega #2 (15%)",
        "Simulación de un cambio regulatorio sobre el sistema en producción y calificación del Módulo 2.",
        "Fase 3 (75m): Cambio Brownfield `cap-p1-pause-budget`",
        [
            "Nuevo requisito del cliente sobre el sistema ya andando: *'En incidentes críticos P1, la suma de pausas WaitingForCustomer no puede superar los 30 minutos'*.",
            "Las duplas ejecutan `/opsx:propose cap-p1-pause-budget` creando `proposal.md`, `tasks.md` y el delta `ADDED/MODIFIED`.",
            "Implementan la validación HTTP 422 (`SLA-422-P1-PAUSE-CAP-EXCEEDED`), corren `dotnet test` y archivan el cambio con `/opsx:archive`.",
        ],
        "Verificación Final en Terminal (Solución de Referencia)",
        [
            "$ cd workshops/ws-m2-sdd-dotnet/solution",
            "$ dotnet test GuardiaCloud.Sla.sln",
            "",
            "Passed! - Failed: 0, Passed: 4, Total: 4",
            " ✓ ResolvedIncident_DoesNotDriftIntoBreach_WhenCheckedLater",
            " ✓ OverlappingPauseWindows_AreMergedWithoutDoubleCounting",
            " ✓ InvalidPauseWindow_ReturnsRfc9457ProblemDetails",
            " ✓ P1Incident_Exceeding30MinPauseCap_Returns422ProblemDetails",
        ],
        True,
        "Fase 4 (60m): Evaluación del Entregable #2 (15% de la Nota Final del Curso)",
        [
            "Rúbrica sobre 100 pts (`02-GUIA-FACILITADOR-Y-RUBRICA.md`): 25 pts `spec.md` EARS/GWT · 25 pts `plan.md` + `tasks.md` + Bug report · 25 pts Delta OpenSpec archivado · 25 pts 4 suites `WebApplicationFactory` en verde.",
        ],
        accent=PURPLE,
    )


# ==============================================================================
# DAYS 6 & 7 (14 hs): Módulo 3 Proyecto Integrador Capstone (Unidades 3.1 a 3.4)
# ==============================================================================
def append_days6_and_7(prs: Presentation):
    add_cover(
        prs,
        "DÍAS 6 Y 7 · GUÍA PASO A PASO (14 HORAS · MÓDULO 3 CAPSTONE)",
        "Días 6 y 7: Proyecto Integrador en Equipos\nsobre GuardiaCloud.CommandCenter (.NET 10)",
        "Simulación real de consultoría de principio a fin (70% de la nota final: Entregables #3 [25%], #4 [35%] y #5 [10%]).",
        [
            ("Día 6 · Mañana", "U3.1 (2h) Relevamiento +\nU3.2 Parte 1 (2h) Specs"),
            ("Día 6 · Tarde", "U3.2 Parte 2 (2h) Peer-Review\n+ U3.3 (2h) Plan DAG (25%)"),
            ("Día 7 · Sprints", "U3.4 (4.5h): 2 Sprints en\nWorktrees + Convergencia"),
            ("Día 7 · Cierre", "U3.4 (1.5h): QA Cruzado,\nDemo (35%) y Métricas (10%)"),
        ],
        accent=PURPLE,
    )

    add_step_slide(
        prs,
        "Día 6 · Unidad 3.1 · 00:00 a 02:00 (2 hs) · Relevamiento Funcional con IA",
        "Unidad 3.1: Auditoría del Pliego de Licitación y Entrevista al Cliente",
        "Los equipos de 3 a 5 personas reciben `workshops/ws-m3-capstone-dotnet/starter/` (`GuardiaCloud.CommandCenter.sln`).",
        "Actividades Paso a Paso de la Unidad 3.1 (120 min)",
        [
            "00:00 – 00:40: Auditar `pliego-licitacion-cliente.md` y el código C# de `starter/` con el agente para descubrir `BUG-301` (webhooks duplicados en `ApplyWebhookEvent`) y las 8 ambigüedades del pliego.",
            "00:40 – 01:25: Entrevista en vivo al 'Director de Operaciones' (rol del presentador con la hoja de 8 respuestas oficiales).",
            "01:25 – 02:00: Consolidación del Documento de Alcance y asignación de los 4 roles del equipo (*Spec Lead*, *Harness/MCP Lead*, *QA/Oracle Lead*, *UI/API Lead*).",
        ],
        "Los 4 Requerimientos del Capstone (GuardiaCloud.CommandCenter)",
        [
            "1. BUG-301 (Idempotencia): ignorar EventId duplicados",
            "   en webhooks de telemetría sin recalcular ni duplicar.",
            "2. FEAT-301 (Escalamiento Proactivo): disparar alerta",
            "   al alcanzar >= 80.0% del SLA con cooldown de 15 min.",
            "3. FEAT-302 (Exención por Fuerza Mayor Dual): exigir",
            "   2 aprobadores distintos + token con prefijo 'FM-DUAL-'.",
            "4. FEAT-303 (Tablero Ejecutivo por Tier): métricas",
            "   agregadas por Platinum, Gold y Silver.",
        ],
        True,
        "Por qué Partimos de un Repositorio Semilla Brownfield Pre-Armado",
        [
            "Los equipos no pierden 4 horas configurando boilerplate ni contenedores desde cero: invierten el 100% de las 14 horas en ingeniería agéntica, especificación, oráculos y entrega verificada.",
        ],
        accent=PURPLE,
    )

    add_step_slide(
        prs,
        "Día 6 · Unidades 3.2 (4 hs) y 3.3 (2 hs) · Especificación, Peer-Review y DAG",
        "Unidades 3.2 y 3.3: Constitución, Specs, Auditoría Cruzada y Entregable #3 (25%)",
        "Al finalizar el Día 6, cada equipo tiene sus contratos congelados en `main` y su plan de 2 Sprints aprobado.",
        "Unidad 3.2 (02:00 – 06:00 · 4 hs): Specs + UI + Peer-Review",
        [
            "02:00 – 03:30: Redactar `AGENTS.md` + `specs/command-center-v2/spec.md` (EARS + GWT con umbrales exactos).",
            "03:30 – 05:00: Redactar `plan.md` (contratos HTTP y códigos RFC 9457 `CC-400-SAME-APPROVER`, `CC-422-INVALID-DUAL-TOKEN`) + prototipo UI de `FEAT-303`.",
            "05:00 – 06:00: **Auditoría Adversarial Cruzada** (el Equipo A audita la Spec del Equipo B).",
        ],
        "Unidad 3.3 (06:00 – 08:00 · 2 hs): Grafo DAG `tasks.md`",
        [
            "# Estrategia de Ejecución Paralela para el Día 7",
            "Fase 0 (En main): Congelar DTOs + 8 Tests Oráculo en rojo",
            "",
            "Sprint 1 (00:00 - 02:00 del Día 7):",
            "  - worktree-bug301  [Full AI] -> Idempotencia EventId",
            "  - worktree-feat301 [Full AI] -> Alerta >=80% + 15m",
            "Checkpoint (02:00 - 02:30): git merge + /speckit-converge",
            "",
            "Sprint 2 (02:30 - 04:30 del Día 7):",
            "  - branch-feat302   [HITL]    -> Doble firma FM-DUAL-",
            "  - worktree-feat303 [Full AI] -> Dashboard por Tier + UI",
        ],
        True,
        "Hito de Evaluación al Cierre del Día 6: Entregable #3 (25% de la Nota Final)",
        [
            "Se califica con la Rúbrica A de `02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md`: Constitución `AGENTS.md` (20 pts), `spec.md` EARS/GWT (30 pts), `plan.md` + Prototipo UI (25 pts) y Grafo `tasks.md` sin colisiones (25 pts).",
        ],
        accent=BLUE,
    )

    add_step_slide(
        prs,
        "Día 7 · Unidad 3.4 · 00:00 a 06:00 (6 hs) · Sprints, QA Cruzado y Demo Final",
        "Día 7: Ejecución Agéntica en 2 Sprints, Demo en Vivo (35%) y Retrospectiva (10%)",
        "Cierre práctico del programa de 52 horas con código `.NET 10` corriendo en vivo y métricas reales.",
        "Cronograma Minuto a Minuto del Día 7 (360 min)",
        [
            "00:00 – 02:00 (Sprint 1): Escribir primero los 8 tests del oráculo en `CommandCenterTests.cs` (`NetArchTest` + `WebApplicationFactory`) y resolver `BUG-301` + `FEAT-301` en worktrees.",
            "02:00 – 02:30 (Checkpoint Obligatorio): Integrar ramas del Sprint 1 en `main`, correr `dotnet test` y ejecutar `/speckit-converge`.",
            "02:30 – 04:30 (Sprint 2): Implementar `FEAT-302` en modo HITL y `FEAT-303` en modo Full AI + integración UI.",
            "04:30 – 05:15 (QA Cruzado): El Equipo B prueba la API del Equipo A contra su `spec.md`.",
            "05:15 – 06:00 (Demos y Cierre): Demo en vivo (**Entregable #4 — 35%**) + Retrospectiva de métricas (**Entregable #5 — 10%**).",
        ],
        "Oráculo Completo en Verde (Solución de Referencia M3)",
        [
            "$ cd workshops/ws-m3-capstone-dotnet/solution",
            "$ dotnet test GuardiaCloud.CommandCenter.sln",
            "",
            "Passed! - Failed: 0, Passed: 8, Total: 8 (545 ms)",
            " ✓ Architecture_Domain_Has_No_Infra_Dependencies",
            " ✓ Bug301_Duplicate_Webhook_EventId_Is_Idempotent",
            " ✓ Feat301_Triggers_Warning_At_80_Percent_Threshold",
            " ✓ Feat301_Respects_15_Minute_Alert_Cooldown",
            " ✓ Feat302_Rejects_Same_Approver_With_CC400",
            " ✓ Feat302_Rejects_Invalid_Token_With_CC422",
            " ✓ Feat302_Applies_ForceMajeure_Exemption_When_Valid",
            " ✓ Feat303_Returns_Executive_Dashboard_By_Tier",
        ],
        True,
        "Cierre de los Entregables #4 (35%) y #5 (10%) = 100% del Curso Completado",
        [
            "Cada participante completa las 52 horas habiendo construido y verificado Skills, Servidores MCP en C#, Hooks de Harness, Especificaciones SDD y un Proyecto Integrador `.NET 10` en equipo.",
        ],
        accent=PURPLE,
    )


def main():
    root = Path(__file__).resolve().parent.parent
    slides_dir = root / "curriculum" / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    # 1. Regenerate Day 1 deck via build-day1-deck.py and copy to curriculum/slides/
    import subprocess
    subprocess.run(["python3", str(root / "scripts" / "build-day1-deck.py")], check=True)
    day1_src = root / "curriculum" / "2026-11-03_dia-1-paso-a-paso.pptx"
    day1_dst = slides_dir / "dia-1-unidades-1.1-y-1.2-paso-a-paso.pptx"
    day1_dst.write_bytes(day1_src.read_bytes())
    print(f"copied {day1_dst.relative_to(root)}")

    # 2. Day 2 Deck
    d2 = new_prs()
    append_day2(d2)
    d2_out = slides_dir / "dia-2-unidades-1.3-y-1.4-paso-a-paso.pptx"
    d2.save(str(d2_out))
    print(f"saved {d2_out.relative_to(root)} ({len(d2.slides)} slides)")

    # 3. Day 3 Deck
    d3 = new_prs()
    append_day3(d3)
    d3_out = slides_dir / "dia-3-unidades-1.5-y-2.1-paso-a-paso.pptx"
    d3.save(str(d3_out))
    print(f"saved {d3_out.relative_to(root)} ({len(d3.slides)} slides)")

    # 4. Day 4 Deck
    d4 = new_prs()
    append_day4(d4)
    d4_out = slides_dir / "dia-4-unidades-2.2-y-2.3-paso-a-paso.pptx"
    d4.save(str(d4_out))
    print(f"saved {d4_out.relative_to(root)} ({len(d4.slides)} slides)")

    # 5. Day 5 Deck
    d5 = new_prs()
    append_day5(d5)
    d5_out = slides_dir / "dia-5-unidad-2.4-sdd-tools-paso-a-paso.pptx"
    d5.save(str(d5_out))
    print(f"saved {d5_out.relative_to(root)} ({len(d5.slides)} slides)")

    # 6. Days 6 & 7 (Module 3 Capstone) Deck
    d67 = new_prs()
    append_days6_and_7(d67)
    d67_out = slides_dir / "dia-6-y-7-modulo-3-capstone-paso-a-paso.pptx"
    d67.save(str(d67_out))
    print(f"saved {d67_out.relative_to(root)} ({len(d67.slides)} slides)")

    # 7. Also run build-course-decks.py so the Master & Module decks stay fresh
    subprocess.run(["python3", str(root / "scripts" / "build-course-decks.py")], check=True)


if __name__ == "__main__":
    main()
