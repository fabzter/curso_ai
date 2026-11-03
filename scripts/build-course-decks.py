#!/usr/bin/env python3
"""
Generate the complete slide decks (.pptx, 16:9 widescreen) for the 52-hour course:
"Desarrollo de Software con IA (.NET 10 & Azure)"

Outputs:
  1. curriculum/2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx (Master Deck, all 3 modules / 13 units / 4 workshops)
  2. curriculum/slides/modulo-1-fundamentos-herramientas-agentes.pptx (Module 1: Units 1.1 - 1.5 + Workshop M1)
  3. curriculum/slides/modulo-2-spec-driven-development.pptx (Module 2: Units 2.1 - 2.4 + Workshops M2-SDD & M2-Harness)
  4. curriculum/slides/modulo-3-capstone-proyecto-integrador.pptx (Module 3: Units 3.1 - 3.4 Capstone)
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
GREEN_SOFT = RGBColor(22, 163, 74)


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


def add_header(slide, tag_text: str, title_text: str, subtitle_text: str = "", tag_color=BLUE):
    set_bg(slide, LIGHT_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.10))
    bar.fill.solid()
    bar.fill.fore_color.rgb = tag_color
    bar.line.fill.background()

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.32), Inches(3.8), Inches(0.34))
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
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.font.name = "Calibri"

    if subtitle_text:
        tb3 = slide.shapes.add_textbox(Inches(0.6), Inches(1.26), Inches(12.1), Inches(0.38))
        tf3 = tb3.text_frame
        tf3.word_wrap = True
        p3 = tf3.paragraphs[0]
        p3.text = subtitle_text
        p3.font.size = Pt(13)
        p3.font.color.rgb = MUTED
        p3.font.name = "Calibri"

    footer = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(12.1), Inches(0.3))
    ftf = footer.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "Desarrollo de Software con IA · Programa Presencial 52 hs (.NET 10 + Azure) · VS Code / Cursor / Windsurf"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = MUTED
    fp.font.name = "Calibri"


def add_card(slide, left, top, width, height, title: str, bullets: list[str], accent=BLUE, title_size=15, body_size=12.5):
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


def add_cover_slide(prs: Presentation, badge_text: str, main_title: str, subtitle: str, pills: list[tuple[str, str]], accent=TEAL):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    set_bg(s, NAVY)

    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.95), Inches(5.4), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = DARK_BLUE
    pill.line.fill.background()
    ptf = pill.text_frame
    pp = ptf.paragraphs[0]
    pp.text = badge_text
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = WHITE
    pp.font.name = "Calibri"

    tb = s.shapes.add_textbox(Inches(0.9), Inches(1.65), Inches(11.5), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = main_title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"

    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(19)
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
        bp1.font.size = Pt(22)
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
    fp.text = "Modalidad Presencial con Workshops Guiados · Stack Primario: .NET 10 + Azure · IDEs: VS Code, Cursor y Windsurf"
    fp.font.size = Pt(12)
    fp.font.color.rgb = RGBColor(148, 163, 184)
    fp.font.name = "Calibri"


def add_unit_concept_slide(prs: Presentation, unit_tag: str, title: str, subtitle: str,
                           col1_title: str, col1_bullets: list[str],
                           col2_title: str, col2_bullets: list[str],
                           bottom_title: str, bottom_bullets: list[str],
                           accent=BLUE):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    add_header(s, unit_tag, title, subtitle, accent)
    add_card(s, 0.6, 1.75, 5.95, 3.25, col1_title, col1_bullets, accent=accent, title_size=15, body_size=12)
    add_card(s, 6.78, 1.75, 5.95, 3.25, col2_title, col2_bullets, accent=TEAL, title_size=15, body_size=12)
    add_card(s, 0.6, 5.18, 12.13, 1.75, bottom_title, bottom_bullets, accent=AMBER, title_size=14, body_size=11.5)


def add_unit_lab_slide(prs: Presentation, unit_tag: str, title: str, subtitle: str,
                       lab_title: str, lab_steps: list[str],
                       code_title: str, code_lines: list[str],
                       deliverable_title: str, deliverable_bullets: list[str],
                       accent=TEAL):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    add_header(s, unit_tag, title, subtitle, accent)
    add_card(s, 0.6, 1.75, 5.95, 3.35, lab_title, lab_steps, accent=accent, title_size=15, body_size=12)
    add_code_card(s, 6.78, 1.75, 5.95, 3.35, code_title, code_lines, accent=accent)
    add_card(s, 0.6, 5.25, 12.13, 1.68, deliverable_title, deliverable_bullets, accent=PURPLE, title_size=14, body_size=11.5)


# ==============================================================================
# SLIDE BUILDERS BY SECTION
# ==============================================================================

def build_intro_slides(prs: Presentation):
    # Slide 1: Cover
    add_cover_slide(
        prs,
        "PROGRAMA DE FORMACIÓN INTENSIVA · 52 HORAS",
        "Desarrollo de Software con IA\nen Ecosistemas .NET 10 y Azure",
        "De la asistencia en el IDE (VS Code, Cursor, Windsurf) al desarrollo guiado por especificaciones (SDD), agentes verificables y entrega en equipo.",
        [
            ("52 Horas", "30% encuadre conceptual\n70% práctica real (36.25 hs)"),
            ("3 Módulos", "13 unidades encadenadas\n+ 4 Workshops evaluables"),
            (".NET 10 + Azure", "Minimal APIs, EF Core, xUnit,\nMCP C# SDK, Extensions.AI"),
            ("VS Code / Cursor", "Windsurf + Claude Code / Codex\n(o tu IDE habitual)"),
        ],
        accent=TEAL,
    )

    # Slide 2: Arquitectura del Curso y Progresión Pedagógica
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Visión General · 52 Horas",
        "Arquitectura del Programa: 3 Módulos y 13 Unidades Encadenadas",
        "Cada unidad produce un artefacto técnico concreto sobre el repositorio semilla que alimenta la unidad siguiente.",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 3.85, 3.45,
        "Módulo 1 · Fundamentos y Agentes (20 hs)",
        [
            "1.1 Diseño asistido por IA y Handoff .NET (4 hs)",
            "1.2 IDEs con IA: VS Code, Cursor y Windsurf (4 hs)",
            "1.3 Agentes, Patrones y Agent Skills SKILL.md (4 hs)",
            "1.4 Harness Engineering: Claude Code, Codex, Devin (6 hs)",
            "1.5 Model Context Protocol (MCP) en C# y Azure (2 hs)",
            "Entregable #1 (15%): Skill de Equipo + Servidor MCP C#",
        ],
        accent=BLUE, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 4.74, 1.75, 3.85, 3.45,
        "Módulo 2 · Spec-Driven Dev (SDD) (18 hs)",
        [
            "2.1 Especificaciones ejecutables EARS / GWT (4 hs)",
            "2.2 Estimación, Análisis de Impacto y DAG (4 hs)",
            "2.3 Implementación: Full AI vs. HITL + Oráculo (4 hs)",
            "2.4 Herramientas SDD: Spec Kit v1.2.5 y OpenSpec (6 hs)",
            "Entregable #2 (15%): Flujo SDD completo + Spec aprobada",
        ],
        accent=TEAL, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 8.88, 1.75, 3.85, 3.45,
        "Módulo 3 · Proyecto Integrador (14 hs)",
        [
            "3.1 Relevamiento Funcional sobre Brownfield (2 hs)",
            "3.2 Constitución, Specs, UI y Auditoría Cruzada (4 hs)",
            "3.3 Planificación y Grafo de Tareas en Equipo (2 hs)",
            "3.4 Ejecución Agéntica en 2 Sprints + QA y Demo (6 hs)",
            "Entregables #3 (25%), #4 (35%) y #5 (10%) = 70% nota",
        ],
        accent=PURPLE, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 0.6, 5.38, 12.13, 1.55,
        "Regla de Oro del Curso: Verificar antes de confiar",
        [
            "La IA comprime el costo de generar código, pero desplaza el cuello de botella hacia la especificación, la arquitectura y la verificación determinista (`dotnet test`, `NetArchTest`, contratos OpenAPI RFC 9457).",
            "Estandarizamos el trabajo de aula en VS Code (con GitHub Copilot), Cursor y Windsurf + harnesses CLI (Claude Code y Codex), permitiendo que cada desarrollador use su IDE habitual si lo prefiere.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    # Slide 3: El Hilo Conductor (Repositorio Semilla Brownfield .NET 10)
    s2 = prs.slides.add_slide(blank)
    add_header(
        s2,
        "Metodología Práctica · Hilo Conductor",
        "El Repositorio Semilla Brownfield: GuardiaCloud.Sla (.NET 10 + Azure)",
        "Evitamos ejemplos de juguete ('Hola Mundo'): trabajamos desde el Día 1 sobre una solución empresarial multicapa real.",
        TEAL,
    )
    add_card(
        s2, 0.6, 1.75, 5.95, 3.3,
        "Arquitectura del Repositorio Semilla (Módulos 1 y 2)",
        [
            "Solución .NET 10 (`GuardiaCloud.Sla.sln`): `Domain`, `Application`, `Infrastructure`, `Api` y `Tests`.",
            "ASP.NET Core Minimal APIs con contratos de error estandarizados `ProblemDetails` (RFC 9457) y `TimeProvider`.",
            "Deuda técnica e incidentes intencionales sembrados: bug sutil de SLA resuelto, falta de `CancellationToken`, violación de capas y notas con prompt injection indirecto.",
            "En el Módulo 3 escala a `GuardiaCloud.CommandCenter.sln` para el proyecto integrador en equipos de 3 a 5 personas.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_code_card(
        s2, 6.78, 1.75, 5.95, 3.3,
        "Estructura de Solución .NET 10 en los Workshops",
        [
            "GuardiaCloud.Sla/",
            "├── AGENTS.md                 # Fuente única de reglas",
            "├── CLAUDE.md                 # @AGENTS.md bridge",
            "├── .agents/skills/           # SKILL.md + scripts/",
            "├── .specify/ & specs/        # GitHub Spec Kit v1.2.5",
            "├── openspec/                 # OpenSpec v1.15.0 deltas",
            "├── src/",
            "│   ├── GuardiaCloud.Sla.Domain/",
            "│   ├── GuardiaCloud.Sla.Api/",
            "│   └── GuardiaCloud.Sla.McpServer/",
            "└── tests/GuardiaCloud.Sla.Tests/ # xUnit + NetArchTest",
        ],
        accent=TEAL,
    )
    add_card(
        s2, 0.6, 5.22, 12.13, 1.7,
        "Cadena de Artefactos Unidad por Unidad (1.1 → 3.4)",
        [
            "U1.1 Prototipo UI + Tokens → U1.2 Reglas de IDE (`VS Code / Cursor / Windsurf`) → U1.3 `SKILL.md` + Agente C# → U1.4 `AGENTS.md` + Hooks `dotnet` → U1.5 Servidor MCP C#.",
            "U2.1 `spec.md` (EARS/GWT) + `plan.md` → U2.2 Informe de Impacto + `tasks.md` (DAG) → U2.3 Oráculo `NetArchTest` + HITL vs. Full AI → U2.4 Flujo Spec Kit / OpenSpec → Módulo 3 Capstone.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )


def build_module1_slides(prs: Presentation):
    # Module 1 Section Cover
    add_cover_slide(
        prs,
        "MÓDULO 1 · 20 HORAS (5 UNIDADES)",
        "Fundamentos: Herramientas, Agentes,\nHarness Engineering y MCPs",
        "Dominá las herramientas de diseño y desarrollo asistido por IA, construí Skills reutilizables y conectá servidores MCP en C# (.NET 10).",
        [
            ("Unidad 1.1", "Diseño UI y Handoff\na .NET (4 hs)"),
            ("Unidad 1.2", "VS Code, Cursor y\nWindsurf (4 hs)"),
            ("Unidad 1.3", "Agentes, Patrones y\nSKILL.md (4 hs)"),
            ("Unidades 1.4 y 1.5", "Harness (6 hs) +\nMCP Server C# (2 hs)"),
        ],
        accent=BLUE,
    )

    # Unit 1.1 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 1 · Unidad 1.1 (4 hs) · Teoría y Arquitectura",
        "Diseño de Producto e Interfaces con IA + Handoff a .NET",
        "Cómo pasar de una necesidad de negocio a un flujo navegable y un sistema de diseño consumible por agentes de código.",
        "Panorama de Herramientas de Diseño con IA",
        [
            "Figma Make: generación y edición sobre sistemas de diseño existentes en Figma.",
            "v0 (Vercel) y Lovable: generación conversacional de interfaces y flujos completos.",
            "Google Stitch (`stitch.withgoogle.com`): ideación rápida de pantallas a partir de lenguaje natural e imágenes.",
            "Claude Artifacts: prototipado interactivo inmediato para validar flujos y micro-interacciones con stakeholders.",
        ],
        "Prompting para UI y Sistemas de Diseño",
        [
            "Estructura de un buen prompt de UI: contexto de dominio + jerarquía visual + estados vacíos/error + restricciones técnicas.",
            "Extracción de Design Tokens (colores, tipografía, espaciado, radios) en archivos estructurados (`design-tokens.json`).",
            "Evitar el rediseño accidental entre iteraciones fijando invariantes visuales y componentes base.",
            "Atención en .NET: las herramientas generan React/Tailwind o HTML/CSS por defecto; diseñamos el puente limpio hacia nuestro backend.",
        ],
        "Dos Patrones de Handoff Diseño → .NET 10",
        [
            "Patrón A (SPA React/Next.js + ASP.NET Core Minimal API): conservar el frontend generado y acoplarlo estrictamente al contrato OpenAPI (`ProblemDetails` RFC 9457) del backend .NET.",
            "Patrón B (HTML/Tailwind → Blazor `.razor`): exportar marcado semántico + tokens y usar el agente de código para traducirlo a componentes Blazor tipados con `[Parameter]`.",
        ],
        accent=BLUE,
    )

    # Unit 1.1 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 1 · Unidad 1.1 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 1.1: Prototipado del Tablero SLA y Paquete de Handoff .NET",
        "Construcción de un flujo de 3 pantallas para GuardiaCloud.Sla, extracción de tokens y generación de componentes.",
        "Paso a Paso del Ejercicio Guiado (150 min)",
        [
            "Paso 1 (40 min): Redactar el prompt estructurado de diseño y generar en Stitch / v0 / Artifacts las 3 pantallas del Monitor de Incidentes SLA (Lista, Detalle de Pausa, Alerta de Incumplimiento).",
            "Paso 2 (35 min): Iterar estados de borde (incidente en riesgo >= 80%, error de validación RFC 9457, vista mobile/desktop).",
            "Paso 3 (45 min): Extraer `design-tokens.json` y convertir la pantalla principal a componente Blazor `.razor` (o cliente tipado sobre el contrato OpenAPI de `GuardiaCloud.Sla.Api`).",
            "Paso 4 (30 min): Revisión cruzada entre pares verificando fidelidad visual y tipado de props.",
        ],
        "Ejemplo de Handoff: Tokens + Contrato Tipado C#",
        [
            "// Contrato DTO en GuardiaCloud.Sla.Api",
            "public sealed record IncidentSlaCardDto(",
            "    string IncidentId,",
            "    string ClientTier,      // Platinum | Gold | Silver",
            "    double ConsumedRatio,   // 0.00 .. 1.00+",
            "    bool IsBreached,",
            "    DateTimeOffset DeadlineUtc);",
            "",
            "// Regla en AGENTS.md para UI:",
            "// - Usar tokens de design-tokens.json",
            "// - Mostrar banner ámbar cuando ConsumedRatio >= 0.80",
        ],
        "Artefacto Entregable de la Unidad 1.1",
        [
            "Prototipo navegable de 3 pantallas + archivo `design-tokens.json` + componente frontend integrado al contrato de datos del repositorio semilla `GuardiaCloud.Sla`.",
        ],
        accent=TEAL,
    )

    # Unit 1.2 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 1 · Unidad 1.2 (4 hs) · Teoría y Evidencia Empírica",
        "Herramientas de Desarrollo: VS Code, Cursor y Windsurf",
        "Estandarización del entorno de aula, configuración de reglas de workspace y prevención de riesgos en código C#.",
        "IDEs del Curso (D-024) y Modos de Interacción",
        [
            "Estandarizamos el curso en VS Code (con GitHub Copilot), Cursor y Windsurf (cada desarrollador puede usar su IDE habitual si lo desea).",
            "Tres modos de uso en el IDE: Autocompletado predictivo (baja latencia) vs. Inline Edit focalizado vs. Agent Mode multi-archivo.",
            "Configuración de reglas por repositorio: `.github/copilot-instructions.md` (VS Code), `.cursor/rules/*.mdc` (Cursor), `.windsurfrules` (Windsurf) y `AGENTS.md`.",
            "Cuándo quedarse en el IDE vs. cuándo delegar a un harness de terminal o cloud (Claude Code / Codex).",
        ],
        "La Paradoja de la Productividad y Riesgos en .NET",
        [
            "Evidencia METR (RCT jul 2025): desarrolladores experimentados trabajando sin disciplina de contexto ni oráculo tardaron 19% más, creyendo ser 20% más rápidos.",
            "Riesgo 1 — Alucinación de paquetes NuGet ('slopsquatting'): el modelo inventa paquetes inexistentes o versiones con APIs obsoletas.",
            "Riesgo 2 — Anti-patrones silenciosos en C#: consultas `N+1` en EF Core, bloqueo `Sync-over-Async` (`.Result`), y omisión de `CancellationToken`.",
            "Riesgo 3 — Seguridad: secretos hardcodeados en `appsettings.json` o inyección SQL en interpolaciones crudas.",
        ],
        "Principio Operativo para el Desarrollador .NET",
        [
            "Nunca aceptes un diff multi-archivo sin contexto de solución ni verificación automática (`dotnet build` + `dotnet test`). El humano es el arquitecto y garante del cambio.",
        ],
        accent=BLUE,
    )

    # Unit 1.2 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 1 · Unidad 1.2 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 1.2: Los 5 Flujos Diarios de Ingeniería sobre Código .NET Legado",
        "Práctica cronometrada en VS Code, Cursor o Windsurf sobre el repositorio brownfield GuardiaCloud.Sla.",
        "Los 5 Flujos Prácticos del Taller (150 min)",
        [
            "Flujo 1 — Comprensión de legado (25 min): mapear el flujo de cálculo de SLA y dependencias ocultas sin leer archivo por archivo.",
            "Flujo 2 — Refactoring seguro C# 13 (30 min): modernizar lógica condicional anidada preservando invariantes y pasando tests.",
            "Flujo 3 — Generación de tests xUnit (35 min): cubrir casos borde de husos horarios y ventanas de pausa con `FakeTimeProvider`.",
            "Flujo 4 — Debugging asistido (30 min): diagnosticar el bug de `ResolvedAtUtc` a partir del stack trace y un test fallido.",
            "Flujo 5 — Code Review asistido (30 min): auditar un PR artificialmente defectuoso (secretos, `N+1`, falta de `CancellationToken`).",
        ],
        "Reglas de Workspace para VS Code / Cursor / Windsurf",
        [
            "# .github/copilot-instructions.md / AGENTS.md",
            "- Target: .NET 10 (net10.0), C# 13, Nullable enable.",
            "- NUNCA usar DateTime.Now ni DateTime.UtcNow directo;",
            "  inyectar siempre System.TimeProvider.",
            "- Todo endpoint Minimal API debe recibir CancellationToken",
            "  y devolver ProblemDetails (RFC 9457) ante errores 4xx.",
            "- Verificar siempre con: dotnet test --no-restore",
        ],
        "Artefacto Entregable de la Unidad 1.2",
        [
            "Repositorio `GuardiaCloud.Sla` configurado en VS Code, Cursor o Windsurf + PR con los 5 flujos resueltos, suite xUnit en verde y checklist de code review completada.",
        ],
        accent=TEAL,
    )

    # Unit 1.3 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 1 · Unidad 1.3 (4 hs) · Teoría y Arquitectura",
        "Agentes, Patrones Agénticos y Agent Skills Reutilizables (`SKILL.md`)",
        "Cómo funciona el bucle de un agente, cuándo usar un flujo determinista y cómo empaquetar conocimiento del equipo.",
        "Anatomía de un Agente y Patrones de Orquestación",
        [
            "El bucle fundamental: Percepción (Contexto) → Razonamiento (Plan) → Acción (Tool Call) → Observación (Resultado/Error).",
            "Workflow determinista vs. Agente autónomo: si el camino de pasos es fijo, usá un pipeline; si requiere decidir herramientas dinámicamente, usá un agente.",
            "4 patrones clásicos (Anthropic): Prompt Chaining, Routing, Orchestrator-Workers (subagentes) y Evaluator-Optimizer.",
            "Control de costos y bucles: `MaximumIterationsPerRequest`, presupuesto de tokens y parada temprana ante fallos repetidos.",
        ],
        "Estándar Abierto SKILL.md y SDKs de Agentes en .NET 10",
        [
            "Estándar `SKILL.md` (`agentskills.io`): carpeta con `SKILL.md` (frontmatter YAML `name` + `description`), `references/` y `scripts/` cargados bajo demanda (*progressive disclosure*).",
            "`Microsoft.Extensions.AI` (`v10.11.0`): abstracción oficial .NET (`IChatClient`, `FunctionInvokingChatClient`, `AIFunctionFactory.Create`).",
            "`Microsoft.Agents.AI` (`v1.27.0`, Microsoft Agent Framework): unifica Semantic Kernel y AutoGen con soporte para Azure AI Foundry.",
            "Comparativa arquitectónica con `Claude Agent SDK` y `OpenAI Agents SDK`.",
        ],
        "Por qué las Skills (`SKILL.md`) superan a un prompt gigante",
        [
            "Un prompt monolítico consume ventana de contexto en cada turno. Una Skill expone solo ~50 tokens de metadatos y carga las referencias y scripts de verificación únicamente cuando la tarea lo requiere.",
        ],
        accent=BLUE,
    )

    # Unit 1.3 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 1 · Unidad 1.3 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 1.3: Creación de una Skill `.NET` y un Agente en C# (`Extensions.AI`)",
        "Parte A y C del Workshop Evaluable M1 (`workshops/ws-m1-skills-mcp-dotnet`).",
        "Agenda Práctica de la Unidad 1.3 (150 min)",
        [
            "Parte 1 (95 min) — Ingeniería de Agent Skills (`SKILL.md`): construir `.agents/skills/dotnet-minimal-api-guardian/SKILL.md` con reglas de arquitectura Minimal API, catálogo RFC 9457 en `references/` y script verificador `scripts/verify-minimal-api.sh`.",
            "Parte 2 (55 min) — Agente Programático en C#: implementar `SlaTriageAgent.cs` usando `Microsoft.Extensions.AI` (`v10.11.0`), `ChatClientBuilder`, `UseFunctionInvocation` (`MaximumIterationsPerRequest = 4`) y `AIFunctionFactory.Create`.",
        ],
        "Agente en C# con Microsoft.Extensions.AI (v10.11.0)",
        [
            "IChatClient agentClient = new ChatClientBuilder(innerClient)",
            "    .UseFunctionInvocation( client => {",
            "        client.MaximumIterationsPerRequest = 4;",
            "    })",
            "    .Build();",
            "",
            "var tools = [",
            "    AIFunctionFactory.Create(SlaMcpTools.GetClientSlaPolicy),",
            "    AIFunctionFactory.Create(SlaMcpTools.InspectIncidentSlaStatus)",
            "];",
        ],
        "Artefacto Entregable de la Unidad 1.3 (Integra el Entregable #1 — 15%)",
        [
            "Skill `dotnet-minimal-api-guardian` validada con `./scripts/verify-minimal-api.sh` + `SlaTriageAgent.cs` ejecutando el bucle multi-herramienta en xUnit.",
        ],
        accent=TEAL,
    )

    # Unit 1.4 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 1 · Unidad 1.4 (6 hs) · Teoría y Evidencia Empírica",
        "Harness Engineering: Claude Code, OpenAI Codex y Devin",
        "El rendimiento de un agente depende tanto de la ingeniería de su arnés (contexto, permisos, hooks y sandboxes) como del modelo subyacente.",
        "¿Qué es el Harness y qué dice la Evidencia (ETH Zurich)?",
        [
            "El *Harness* envuelve al LLM: gestiona qué archivos entran al contexto, qué comandos bash pueden correrse, qué hooks validan cada edición y cómo se aísla el entorno.",
            "Interoperabilidad multi-herramienta: `AGENTS.md` es leído nativamente por VS Code Copilot, Cursor, Windsurf y Codex; `CLAUDE.md` importa `@AGENTS.md` para mantener una única fuente de verdad.",
            "Estudio ETH Zurich (`arXiv:2602.11988`): archivos `AGENTS.md` autogenerados por LLMs reducen la precisión hasta 2% e inflan el costo de tokens +20–23%. Los archivos breves (<80 líneas) curados por humanos mejoran la tasa de éxito.",
        ],
        "Tres Harnesses de Referencia en la Industria (Oct 2026)",
        [
            "Claude Code (`v2.1.314`): modo `/plan`, permisos granulares, subagentes en `.claude/agents/`, hooks deterministas (`PreToolUse` / `PostToolUse` / `Stop`) y ejecución headless `claude -p` en CI.",
            "OpenAI Codex (`rust-v0.166.0`): CLI local open-source en Rust + agente cloud asíncrono; modos de sandbox (`read-only`, `workspace-write`, `danger-full-access`) y ejecución paralela de tareas.",
            "Devin (Cognition): sesiones autónomas cloud orientadas a tickets completos; gestión de *Knowledge*, *Playbooks* reutilizables y *DeepWiki*.",
        ],
        "Hooks Deterministas en .NET: El Cinturón de Seguridad del Agente",
        [
            "Un hook `PostToolUse` que ejecuta `dotnet build --no-restore` tras cada edición de un archivo `.cs` impide que el agente acumule errores de compilación y lo obliga a autocorregirse en el acto.",
        ],
        accent=BLUE,
    )

    # Unit 1.4 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 1 · Unidad 1.4 (6 hs) · Workshop Práctico (3h 45m)",
        "Taller 1.4: Endurecimiento del Harness .NET, Hooks y Subagentes",
        "Parte 1 del Workshop `workshops/ws-m2-harness-oracle-dotnet` sobre `GuardiaCloud.Sla.HarnessLab.sln`.",
        "Agenda Práctica del Laboratorio (225 min)",
        [
            "Fase 1 (60 min) — Poda de `AGENTS.md`: auditar un `AGENTS.md` inflado de 180 líneas, podarlo a <60 líneas de alta señal verificables y enlazar `CLAUDE.md` (`@AGENTS.md`).",
            "Fase 2 (65 min) — Hook Determinista `PostToolUse`: configurar `.claude/settings.json` para disparar `scripts/post-edit-dotnet-hook.sh` (`dotnet build` + `dotnet test`) tras cada `Write`/`Edit`.",
            "Fase 3 (50 min) — Subagente Especialista: configurar `.claude/agents/dotnet-arch-reviewer.md` en modo solo lectura (`Read`, `Grep`, `Glob`) para auditar PRs.",
            "Fase 4 (50 min) — Comparativa Claude Code vs. Codex: resolver el mismo ticket .NET en ambos harnesses y comparar diffs, tiempos y consumo de tokens.",
        ],
        "Hook PostToolUse en .claude/settings.json",
        [
            "{",
            '  "hooks": {',
            '    "PostToolUse": [',
            "      {",
            '        "matcher": "Write|Edit|MultiEdit",',
            '        "hooks": [{',
            '          "type": "command",',
            '          "command": "./scripts/post-edit-dotnet-hook.sh"',
            "        }]",
            "      }",
            "    ]",
            "  }",
            "}",
        ],
        "Artefacto Entregable de la Unidad 1.4",
        [
            "Repositorio `.NET 10` con `AGENTS.md` curado (<60 líneas), `CLAUDE.md` puenteado, hook `PostToolUse` activo y subagente revisor probado.",
        ],
        accent=TEAL,
    )

    # Unit 1.5 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 1 · Unidad 1.5 (2 hs) · Teoría y Seguridad MCP",
        "Model Context Protocol (MCP) en .NET 10 y Azure",
        "Conectá tus agentes a bases de datos, telemetría de Azure y herramientas de dominio escritas directamente en C#.",
        "Arquitectura MCP y SDK Oficial de C# (`v2.3.0`)",
        [
            "Arquitectura Host → Client → Server: desacopla el agente (Claude Code, VS Code, Cursor, Windsurf) de las fuentes de datos corporativas.",
            "3 primitivas del protocolo: `Tools` (acciones invocables por el modelo), `Resources` (datos leíbles por URI) y `Prompts` (plantillas parametrizadas).",
            "Transportes estándar: `stdio` (procesos locales sin abrir puertos) y `Streamable HTTP` (`ModelContextProtocol.AspNetCore` para servidores remotos).",
            "SDK oficial de C# en NuGet: `ModelContextProtocol` (`v2.3.0`), mantenido por Microsoft y Anthropic con soporte nativo para `net10.0` y DI.",
        ],
        "Servidores MCP Empresariales y Seguridad Defensiva",
        [
            "Servidores listos para usar en consultoría: Azure MCP Server (`microsoft/mcp`), GitHub / Azure DevOps MCP, PostgreSQL / SQL Server MCP y Sentry/Grafana.",
            "Riesgo crítico — *Indirect Prompt Injection*: notas de soporte o textos de terceros en la base de datos que intentan secuestrar las instrucciones del agente.",
            "Riesgo crítico — *Tool Poisoning* y exceso de privilegios: herramientas mutables sin confirmación humana o que exponen cadenas de conexión.",
            "Regla `stdio` en C#: redirigir todos los logs a `stderr` (`LogToStandardErrorThreshold = LogLevel.Trace`) para no corromper el canal JSON-RPC de `stdout`.",
        ],
        "Anotaciones de Seguridad en Herramientas MCP C#",
        [
            "Declarar explícitamente `ReadOnlyHint = true`, `DestructiveHint = false` e `IdempotentHint = true` en `[McpServerTool]` permite que el IDE/harness pida confirmación solo cuando corresponde.",
        ],
        accent=BLUE,
    )

    # Unit 1.5 Lab + Workshop M1 Summary
    add_unit_lab_slide(
        prs,
        "Módulo 1 · Unidad 1.5 (2 hs) · Workshop Evaluable #1 (15% de la Nota)",
        "Taller 1.5: Construcción de un Servidor MCP en C# y Defensa Anti-Inyección",
        "Cierre del Workshop `workshops/ws-m1-skills-mcp-dotnet` (`GuardiaCloud.Sla.McpWorkshop.sln`).",
        "Implementación del Servidor MCP en C# (75 min)",
        [
            "Paso 1: Inspeccionar `Program.cs` (`AddMcpServer().WithStdioServerTransport().WithToolsFromAssembly()`) y la herramienta base `get_client_sla_policy`.",
            "Paso 2: Implementar `inspect_incident_sla_status` calculando el consumo de SLA y sanitizando `CustomerNotes` con `SanitizeUntrustedNotes` para neutralizar el ataque en `INC-2026-1002`.",
            "Paso 3: Implementar `validate_rfc9457_contract` auditando payloads de error contra la lista blanca de códigos `SLA-4xx`.",
            "Paso 4: Ejecutar `dotnet test` (6/6 tests en verde) y conectar el servidor en `.mcp.json` desde VS Code / Cursor / Claude Code.",
        ],
        "Tool MCP en C# (ModelContextProtocol v2.3.0)",
        [
            "[McpServerToolType]",
            "public static class SlaMcpTools {",
            "  [McpServerTool(",
            '    Name = "inspect_incident_sla_status",',
            "    ReadOnlyHint = true, DestructiveHint = false)]",
            "  [Description(\"Calcula estado SLA y sanitiza notas.\")]",
            "  public static IncidentSlaStatusResult InspectIncident(",
            "      SlaRepository repo, string incidentId) { ... }",
            "}",
        ],
        "Rúbrica del Entregable Evaluable #1 (Cierre del Módulo 1 — 15% Nota Final)",
        [
            "30 pts: `SKILL.md` + `verify-minimal-api.sh` · 35 pts: Servidor MCP C# con 3 tools tipadas · 20 pts: Sanitización anti-inyección (`INC-2026-1002`) · 15 pts: Agente `SlaTriageAgent` con `Microsoft.Extensions.AI`.",
        ],
        accent=PURPLE,
    )


def build_module2_slides(prs: Presentation):
    # Module 2 Section Cover
    add_cover_slide(
        prs,
        "MÓDULO 2 · 18 HORAS (4 UNIDADES)",
        "Spec-Driven Development (SDD)\nen Ingeniería de Software con .NET",
        "Convertí requerimientos ambiguos en especificaciones ejecutables, grafos de tareas sin conflictos y código verificado por oráculos deterministas.",
        [
            ("Unidad 2.1", "Specs Ejecutables:\nEARS + GWT (4 hs)"),
            ("Unidad 2.2", "Impacto, Estimación\ny DAG (4 hs)"),
            ("Unidad 2.3", "Full AI vs. HITL +\nOráculo .NET (4 hs)"),
            ("Unidad 2.4", "Spec Kit v1.2.5 y\nOpenSpec v1.15 (6 hs)"),
        ],
        accent=TEAL,
    )

    # Unit 2.1 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 2 · Unidad 2.1 (4 hs) · Teoría y Evidencia Empírica",
        "El Arte de Especificar: De la Ambigüedad a EARS y Given/When/Then",
        "Por qué la calidad de la especificación es el predictor #1 del éxito o fracaso de un agente de código.",
        "Evidencia Científica sobre Especificaciones y Agentes",
        [
            "Estudio Larbi et al. (`arXiv:2507.20439`): requerimientos con ambigüedades o contradicciones provocan una caída de 20 a 40 puntos porcentuales en Pass@1.",
            "Benchmark SWE-EVO (`arXiv:2512.18470`): más del 60% de los fallos de agentes en evolución de software provienen de malinterpretar requerimientos implícitos, no de errores de sintaxis.",
            "El anti-patrón del 'Vibe Coding Empresarial': pedirle al agente *'agregá pausas de SLA'* sin definir husos horarios, topes por severidad ni códigos de error.",
        ],
        "La Jerarquía de Artefactos SDD y Notación EARS",
        [
            "1. Constitución del Proyecto (`constitution.md` / `AGENTS.md`): invariantes arquitectónicas no negociables de toda la solución.",
            "2. Especificación Funcional (`spec.md`): historias de usuario, reglas de negocio en sintaxis EARS (`WHEN <evento> WHILE <condición> THE SYSTEM SHALL <respuesta>`) y escenarios Given/When/Then.",
            "3. Especificación Técnica (`plan.md` + ADRs): contratos de endpoints Minimal API, esquema de datos EF Core, códigos `ProblemDetails` RFC 9457 y estrategia de tests.",
        ],
        "El Agente como Crítico Adversarial de Especificaciones",
        [
            "Antes de escribir una sola línea de C#, usamos al agente con un prompt adversarial (*Spec Critic*) para detectar huecos lógicos, condiciones de carrera y casos borde ausentes en el pedido del cliente.",
        ],
        accent=TEAL,
    )

    # Unit 2.1 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 2 · Unidad 2.1 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 2.1: Auditoría Adversarial y Redacción de `spec.md` + `plan.md`",
        "Primera mitad del Workshop Evaluable M2 (`workshops/ws-m2-sdd-dotnet`) sobre `GuardiaCloud.Sla.sln`.",
        "Paso a Paso del Taller (150 min)",
        [
            "Paso 1 (35 min): Analizar `brief-cliente-ambiguo.md` (*'Queremos pausar el reloj de SLA cuando esperamos al cliente'*) con un agente en modo *Spec Critic* para descubrir las 7 ambigüedades ocultas.",
            "Paso 2 (30 min): Entrevistar al instructor (rol Gerente de Operaciones) para cerrar definiciones exactas (motivos válidos, solapamiento de intervalos, límite en incidentes P1).",
            "Paso 3 (50 min): Redactar `specs/001-sla-pause-windows/spec.md` usando sintaxis EARS y escenarios Given/When/Then verificables.",
            "Paso 4 (35 min): Redactar `specs/001-sla-pause-windows/plan.md` definiendo DTOs C#, códigos RFC 9457 (`SLA-400-*`, `SLA-422-*`) y algoritmo de fusión de intervalos.",
        ],
        "Ejemplo de Requerimiento EARS + Escenario GWT",
        [
            "### REQ-SLA-002 (Sintaxis EARS)",
            "WHEN un operador registra una ventana de pausa",
            "WHILE el incidente tiene severidad P1 (Crítica)",
            "IF la duración acumulada supera los 30 minutos",
            "THE SYSTEM SHALL rechazar la pausa con HTTP 422",
            "y código ProblemDetails 'SLA-422-P1-PAUSE-CAP-EXCEEDED'.",
            "",
            "### Escenario GWT",
            "Given un incidente P1 con 20 min de pausa previa",
            "When se envía una nueva pausa de 15 min...",
        ],
        "Artefacto Entregable de la Unidad 2.1",
        [
            "`specs/001-sla-pause-windows/spec.md` + `plan.md` aprobados tras revisión cruzada entre duplas (sin ningún marcador `[NEEDS CLARIFICATION]` pendiente).",
        ],
        accent=BLUE,
    )

    # Unit 2.2 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 2 · Unidad 2.2 (4 hs) · Teoría y Métricas de Ingeniería",
        "Estimación, Análisis de Impacto y Planificación en Grafos (DAG)",
        "Cómo descomponer una especificación técnica para que múltiples desarrolladores y agentes trabajen en paralelo sin pisarse.",
        "Análisis de Impacto Brownfield y la Trampa del Merge",
        [
            "Uso de agentes en modo *Read-Only / Plan* para mapear el radio de explosión (*blast radius*) en soluciones .NET: proyectos afectados, migraciones EF Core y cambios rompedores en OpenAPI.",
            "Evidencia AgenticFlict (2026): cuando múltiples agentes ejecutan tareas en paralelo sin fronteras explícitas de archivos, el **27.67% de los PRs** sufre conflictos de merge severos.",
            "Solución de ingeniería: descomponer `plan.md` en un **Grafo Acíclico Dirigido (`tasks.md`)** donde cada tarea declara exactamente qué archivos `.cs` crea o modifica.",
        ],
        "Cómo Cambia la Estimación con IA en Consultoría",
        [
            "Separar dos curvas distintas: el **tiempo de generación de código** cae drásticamente (50–70%), pero el **tiempo de revisión, pruebas de integración y QA** escala con el tamaño y riesgo del diff.",
            "Fenómeno 'Workslop' (BetterUp / Stanford): artefactos generados rápido pero sin validación trasladan ~2 horas de retrabajo por ítem al revisor senior.",
            "Nuevas variables de estimación: complejidad del oráculo de pruebas, acoplamiento legacy, costo de tokens/iteraciones y nivel de escrutinio regulatorio.",
        ],
        "Regla para Tareas Paralelizables `[P]` en `tasks.md`",
        [
            "Dos tareas solo pueden marcarse como paralelas `[P]` si sus conjuntos de archivos modificados son disjuntos y su contrato de interfaz (DTO/interfaz C#) ya fue fijado en una tarea previa.",
        ],
        accent=TEAL,
    )

    # Unit 2.2 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 2 · Unidad 2.2 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 2.2: Análisis de Impacto Automatizado y Construcción del DAG `tasks.md`",
        "Transformación de la especificación técnica de la Unidad 2.1 en un plan de ejecución libre de conflictos.",
        "Agenda Práctica del Taller (150 min)",
        [
            "Paso 1 (40 min): Ejecutar un análisis de impacto en modo solo lectura sobre `GuardiaCloud.Sla.sln` para identificar todos los puntos de acoplamiento de `SlaCalculator` y `Program.cs`.",
            "Paso 2 (50 min): Descomponer `plan.md` en un grafo `tasks.md` de 6 a 8 tareas atómicas (<150 LOC por tarea), especificando precondiciones, archivos tocados y comando `dotnet test --filter` de verificación.",
            "Paso 3 (35 min): Estimar el esfuerzo de cada tarea comparando estimación tradicional vs. asistida por IA (desglosando tiempo de generación vs. tiempo de verificación/review).",
            "Paso 4 (25 min): Auditoría cruzada del grafo de tareas buscando colisiones de archivos entre tareas marcadas `[P]`.",
        ],
        "Estructura de un Grafo de Tareas (tasks.md)",
        [
            "## Fase 1: Contratos y Oráculo (Secuencial)",
            "- [ ] T001: Crear DTOs y códigos RFC 9457 en Domain",
            "  - Archivos: src/.../Domain/SlaPauseWindow.cs",
            "  - Verificación: dotnet build --no-restore",
            "- [ ] T002: Escribir tests de integración en rojo",
            "  - Archivos: tests/.../SlaPauseEndpointsTests.cs",
            "## Fase 2: Implementación Paralela [P]",
            "- [ ] T003 [P] [Full-AI]: Algoritmo fusión en SlaCalculator",
            "- [ ] T004 [P] [HITL]: Endpoint POST /pauses en Program.cs",
        ],
        "Artefacto Entregable de la Unidad 2.2",
        [
            "Informe de Impacto Brownfield + archivo `specs/001-sla-pause-windows/tasks.md` con grafo DAG, fronteras de archivos y tabla de estimación.",
        ],
        accent=BLUE,
    )

    # Unit 2.3 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 2 · Unidad 2.3 (4 hs) · Teoría y Arquitectura de Verificación",
        "Implementación: Full AI vs. Human-in-the-Loop (HITL) y Oráculos .NET",
        "Cómo decidir el grado de autonomía por tarea y cómo construir un oráculo determinista que impida falsos positivos.",
        "Matriz de Decisión: ¿Cuándo usar Full AI vs. HITL?",
        [
            "Modo Full AI (Autónomo en `git worktree` aislado): ideal para tareas acotadas con especificación cerrada y un oráculo de pruebas 100% determinista (ej. cálculos puros, exportadores, proyectores de lectura, tests).",
            "Modo Human-in-the-Loop (HITL con checkpoints): indispensable en lógica financiera/regulatoria, migraciones destructivas, autenticación/autorización o cuando el diseño emerge durante la exploración.",
            "Aislamiento con `git worktree`: permite que un agente autónomo corra en una carpeta paralela sin bloquear tu rama de trabajo principal.",
        ],
        "Las 4 Capas del Oráculo de Verificación en .NET 10",
        [
            "1. Compilador C# y Analizadores Roslyn (`TreatWarningsAsErrors=true`, `Nullable=enable`).",
            "2. Fitness Functions de Arquitectura con `NetArchTest.Rules` (`v1.3.2`): tests unitarios que fallan si `Domain` referencia a `Infrastructure` o `Microsoft.AspNetCore`.",
            "3. Pruebas de Integración en Memoria/Contenedores (`WebApplicationFactory<Program>` + `Testcontainers` + `FakeTimeProvider`).",
            "4. Validación de Contratos OpenAPI y códigos de error `ProblemDetails` (RFC 9457).",
        ],
        "Por qué `NetArchTest.Rules` es Esencial cuando Programan Agentes",
        [
            "Un agente en modo autónomo busca el camino más corto para que el test funcional pase, aunque eso implique inyectar `DbContext` o `HttpContext` dentro de una entidad de dominio. `NetArchTest` bloquea esa deriva arquitectónica automáticamente.",
        ],
        accent=TEAL,
    )

    # Unit 2.3 Lab
    add_unit_lab_slide(
        prs,
        "Módulo 2 · Unidad 2.3 (4 hs) · Workshop Práctico (2h 30m)",
        "Taller 2.3: Oráculo `NetArchTest` y Laboratorio Comparativo HITL vs. Full AI",
        "Segunda mitad del Workshop `workshops/ws-m2-harness-oracle-dotnet` (`GuardiaCloud.Sla.HarnessLab.sln`).",
        "Agenda Práctica del Laboratorio (150 min)",
        [
            "Paso 1 (45 min) — Fitness Functions con `NetArchTest.Rules` (`v1.3.2`): escribir las 3 reglas arquitectónicas en `ArchitectureFitnessTests.cs`, detectar la violación en `LegacyVibeCodedHelper.cs` y corregirla.",
            "Paso 2 (45 min) — Tarea A en modo HITL: implementar el cálculo de créditos financieros mensuales por SLA incumplido con aprobación humana paso a paso.",
            "Paso 3 (40 min) — Tarea B en modo Full AI (`git worktree`): delegar el endpoint de resumen de guardia a un agente autónomo guiado únicamente por el oráculo xUnit + `NetArchTest`.",
            "Paso 4 (20 min) — Debrief de Métricas: completar `comparativa-hitl-vs-full-ai.md` (tiempo total, iteraciones, limpieza del diff).",
        ],
        "Oráculo Arquitectónico con NetArchTest.Rules (v1.3.2)",
        [
            "[Fact]",
            "public void Domain_Should_Not_Depend_On_Infrastructure_Or_Web()",
            "{",
            "    var result = Types.InAssembly(typeof(Incident).Assembly)",
            "        .ShouldNot()",
            "        .HaveDependencyOnAny(",
            '            "GuardiaCloud.Sla.Infrastructure",',
            '            "Microsoft.AspNetCore")',
            "        .GetResult();",
            "    Assert.True(result.IsSuccessful);",
            "}",
        ],
        "Artefacto Entregable de la Unidad 2.3",
        [
            "Suite de 7 tests en verde (3 `NetArchTest.Rules` + 4 `WebApplicationFactory`) + informe empírico `comparativa-hitl-vs-full-ai.md`.",
        ],
        accent=BLUE,
    )

    # Unit 2.4 Concept
    add_unit_concept_slide(
        prs,
        "Módulo 2 · Unidad 2.4 (6 hs) · Teoría y Ecosistema SDD (Oct 2026)",
        "Herramientas para SDD: GitHub Spec Kit, OpenSpec, Kiro, BMAD y Tessl",
        "Taxonomía de herramientas SDD y criterios para elegir el flujo correcto en proyectos greenfield vs. brownfield.",
        "Taxonomía SDD (Martin Fowler / Birgitta Böckeler)",
        [
            "1. Spec-first: se escribe la especificación antes de generar el código de la iteración, pero luego el código es la única fuente de verdad.",
            "2. Spec-anchored (el punto dulce en consultoría): las especificaciones viven en el repositorio junto al código y evolucionan en cada cambio.",
            "3. Spec-as-source: el humano edita solo la especificación y el código es un artefacto compilado (enfoque experimental de Tessl).",
            "Comparativa del mercado actual: AWS Kiro (`.kiro/specs/`), BMAD Method (`v6.12.4`, roles multi-agente) y Tessl (`tessl.io` Spec Registry).",
        ],
        "Las Dos Herramientas Centrales de Nuestro Stack SDD",
        [
            "GitHub Spec Kit (`v1.2.5`, oct 2026): CLI `specify` + comandos `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` y `/speckit-converge`, más extensión `bug` (`/speckit-bug-*`). Ideal para features nuevas estructuradas.",
            "Fission-AI OpenSpec (`v1.15.0`, oct 2026): flujo de **deltas brownfield** (`openspec/specs/` + `openspec/changes/`). Comandos `/opsx:explore` → `/opsx:propose` → `/opsx:apply` → `/opsx:archive`. Ideal para modificar sistemas .NET existentes trazando `ADDED / MODIFIED / REMOVED`.",
        ],
        "Por qué Combinamos Spec Kit + OpenSpec en Consultoría .NET",
        [
            "Spec Kit estructura la constitución y el diseño inicial de una capacidad; OpenSpec permite auditar exactamente qué requisito de negocio existente cambió meses después sin perder trazabilidad histórica.",
        ],
        accent=TEAL,
    )

    # Unit 2.4 Lab + Workshop M2 Summary
    add_unit_lab_slide(
        prs,
        "Módulo 2 · Unidad 2.4 (6 hs) · Workshop Evaluable #2 (15% de la Nota)",
        "Taller 2.4: Ciclo Completo con GitHub Spec Kit `v1.2.5` y OpenSpec `v1.15.0`",
        "Cierre del Workshop Evaluable M2 (`workshops/ws-m2-sdd-dotnet`) sobre `GuardiaCloud.Sla.sln`.",
        "Agenda Práctica del Laboratorio SDD (225 min)",
        [
            "Fase 1 (45 min) — Bugfix con Spec Kit: diagnosticar y corregir el bug de `ResolvedAtUtc` en `SlaCalculator.cs` documentando causa raíz y test de regresión en `.specify/bugs/resolved-sla-breach-drift/report.md`.",
            "Fase 2 (75 min) — Feature con Spec Kit (`001-sla-pause-windows`): ejecutar `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`.",
            "Fase 3 (65 min) — Cambio Brownfield con OpenSpec: crear el cambio `cap-p1-pause-budget` (`ADDED`/`MODIFIED` sobre incidentes P1), implementar la validación `SLA-422-P1-PAUSE-CAP-EXCEEDED` y archivar en `openspec/changes/archive/`.",
            "Fase 4 (40 min) — Armado del Flujo SDD propio del equipo listo para el Módulo 3.",
        ],
        "Comandos SDD y Verificación en .NET 10",
        [
            "# Ciclo GitHub Spec Kit v1.2.5",
            "/speckit-constitution  -> .specify/memory/constitution.md",
            "/speckit-specify       -> specs/001-sla-pause-windows/spec.md",
            "/speckit-plan          -> specs/001-sla-pause-windows/plan.md",
            "/speckit-tasks         -> specs/001-sla-pause-windows/tasks.md",
            "/speckit-implement     -> src/GuardiaCloud.Sla.Api/...",
            "/speckit-converge      -> Verifica código vs. spec.md",
            "",
            "# Ciclo OpenSpec v1.15.0 (Brownfield Delta)",
            "/opsx:explore -> /opsx:propose -> /opsx:apply -> /opsx:archive",
        ],
        "Rúbrica del Entregable Evaluable #2 (Cierre del Módulo 2 — 15% Nota Final)",
        [
            "25 pts: Descubrimiento de ambigüedades + `spec.md` EARS/GWT · 25 pts: `plan.md` + `tasks.md` + Bug report · 25 pts: Delta OpenSpec archivado · 25 pts: 4 suites de integración `WebApplicationFactory` en verde.",
        ],
        accent=PURPLE,
    )


def build_module3_slides(prs: Presentation):
    # Module 3 Section Cover
    add_cover_slide(
        prs,
        "MÓDULO 3 · 14 HORAS (4 UNIDADES · CAPSTONE)",
        "Ejecución de Proyecto Integrador\ncon Flujo SDD y Agentes en .NET 10",
        "Simulación intensiva en equipos de 3 a 5 personas sobre `GuardiaCloud.CommandCenter.sln` (70% de la nota final del curso).",
        [
            ("Unidad 3.1 (2 hs)", "Relevamiento y Auditoría\nBrownfield con IA"),
            ("Unidad 3.2 (4 hs)", "Constitución, Specs,\nUI y Revisión Cruzada"),
            ("Unidad 3.3 (2 hs)", "Impacto, Roles y Grafo\nde Tareas (DAG)"),
            ("Unidad 3.4 (6 hs)", "2 Sprints Agénticos,\nQA Cruzado y Demo"),
        ],
        accent=PURPLE,
    )

    # Unit 3.1 Slide
    add_unit_lab_slide(
        prs,
        "Módulo 3 · Unidad 3.1 (2 hs) · Relevamiento Funcional y Alcance",
        "Unidad 3.1: Descubrimiento Asistido por IA sobre `GuardiaCloud.CommandCenter`",
        "Los equipos reciben un pliego de licitación con 8 ambigüedades deliberadas y un repositorio .NET 10 brownfield con deuda técnica.",
        "Actividades del Equipo en la Unidad 3.1 (120 min)",
        [
            "1. Ingesta del caso (`pliego-licitacion-cliente.md`): el cliente pide corregir un bug de duplicación de webhooks (`BUG-301`) y construir 3 capacidades nuevas (`FEAT-301` escalamiento proactivo 80%, `FEAT-302` exención por fuerza mayor con doble firma, `FEAT-303` tablero ejecutivo).",
            "2. Auditoría del repositorio `starter/` con agentes en modo exploración para detectar el bug en `CommandCenterEvaluator.ApplyWebhookEvent`.",
            "3. Generación asistida del cuestionario de descubrimiento (8 preguntas críticas) y entrevista en vivo con el instructor ('Director de Operaciones').",
            "4. Cierre del Documento de Alcance y Reglas de Negocio validadas.",
        ],
        "Topología Recomendada por Equipo (3 a 5 Integrantes)",
        [
            "Rol 1 · Spec & Architecture Lead:",
            "  Custodia AGENTS.md, spec.md y plan.md.",
            "Rol 2 · Harness, MCP & Backend Lead:",
            "  Configura hooks, MCP C# y lógica de dominio.",
            "Rol 3 · QA, Verification Oracle & Security Lead:",
            "  Escribe tests NetArchTest + WebApplicationFactory.",
            "Rol 4 · UI Prototype & API Integration Lead:",
            "  Diseña el tablero FEAT-303 y valida contratos DTO.",
        ],
        "Salida de la Unidad 3.1",
        [
            "Las 8 reglas de negocio clarificadas (umbral exacto `>= 80.0%`, ventana de enfriamiento de 15 min, prefijo `FM-DUAL-`, aprobación por 2 operadores distintos, etc.) listas para especificar.",
        ],
        accent=PURPLE,
    )

    # Unit 3.2 Slide
    add_unit_lab_slide(
        prs,
        "Módulo 3 · Unidad 3.2 (4 hs) · Especificaciones y Revisión Adversarial Cruzada",
        "Unidad 3.2: Constitución, Specs EARS/GWT, Prototipo UI y Auditoría entre Equipos",
        "Ningún equipo puede abrir un PR de implementación sin haber aprobado la auditoría adversarial cruzada de su especificación.",
        "Actividades del Equipo en la Unidad 3.2 (240 min)",
        [
            "1. Configurar la Constitución del repositorio (`AGENTS.md` + `CLAUDE.md`) y los hooks de validación `.NET` heredados del Módulo 1.",
            "2. Redactar `specs/command-center-v2/spec.md` (requisitos EARS + criterios Given/When/Then para `BUG-301`, `FEAT-301`, `FEAT-302` y `FEAT-303`).",
            "3. Redactar `specs/command-center-v2/plan.md` fijando contratos HTTP, DTOs C# y catálogo de errores RFC 9457 (`CC-400-SAME-APPROVER`, `CC-422-INVALID-DUAL-TOKEN`).",
            "4. Generar el prototipo UI del Tablero Ejecutivo (`FEAT-303`) y ejecutar la **Auditoría Adversarial Cruzada** (el Equipo A audita la Spec del Equipo B con su agente).",
        ],
        "Contratos RFC 9457 Exigidos en plan.md (Unidad 3.2)",
        [
            "// Códigos ProblemDetails obligatorios en FEAT-302:",
            "// 1. Si ApproverA == ApproverB (case-insensitive):",
            "//    Status = 400 Bad Request",
            '//    errorCode = "CC-400-SAME-APPROVER"',
            "",
            "// 2. Si ApprovalToken no inicia con 'FM-DUAL-':",
            "//    Status = 422 Unprocessable Entity",
            '//    errorCode = "CC-422-INVALID-DUAL-TOKEN"',
        ],
        "Salida de la Unidad 3.2 (Núcleo del Entregable Evaluable #3 — 25% Nota Final)",
        [
            "`AGENTS.md` + `specs/command-center-v2/spec.md` + `plan.md` + prototipo UI corregidos tras el peer-review cruzado.",
        ],
        accent=BLUE,
    )

    # Unit 3.3 Slide
    add_unit_lab_slide(
        prs,
        "Módulo 3 · Unidad 3.3 (2 hs) · Planificación y Estrategia de Paralelización",
        "Unidad 3.3: Grafo de Tareas (`tasks.md`), Asignación HITL vs. Full AI y Worktrees",
        "Diseño de la estrategia de ejecución en equipo para que las 6 horas de la Unidad 3.4 fluyan sin bloqueos ni conflictos de merge.",
        "Actividades del Equipo en la Unidad 3.3 (120 min)",
        [
            "1. Ejecutar análisis de impacto sobre `GuardiaCloud.CommandCenter.sln` y dividir el trabajo en un DAG `specs/command-center-v2/tasks.md`.",
            "2. Asignar el modo de ejecución por tarea con justificación técnica:",
            "   • `BUG-301` (idempotencia de webhooks) y `FEAT-303` (tablero ejecutivo de solo lectura) → candidatos ideales para **Full AI** en `git worktrees`.",
            "   • `FEAT-302` (exención regulatoria por fuerza mayor con doble firma) → obligatorio en modo **Human-in-the-Loop (HITL)**.",
            "3. Congelar las firmas de DTOs e interfaces en `Domain` antes de abrir ramas paralelas.",
        ],
        "Asignación de Ramas y Worktrees para la Unidad 3.4",
        [
            "main (Contratos congelados + Tests Oráculo base)",
            " ├── worktree-bug301  [Full AI] -> Idempotencia EventId",
            " ├── worktree-feat301 [Full AI] -> Alerta 80% + Cooldown",
            " ├── branch-feat302   [HITL]    -> Doble firma FM-DUAL-",
            " └── worktree-feat303 [Full AI] -> Dashboard por Tier",
            "",
            "# Checkpoint obligatorio en Minuto 120:",
            "git merge + dotnet test + /speckit-converge",
        ],
        "Cierre del Entregable Evaluable #3 (25% de la Nota del Curso)",
        [
            "Con `tasks.md` aprobado al finalizar la Unidad 3.3, el equipo completa el **Entregable #3 (25%)** y queda habilitado para iniciar los Sprints de código.",
        ],
        accent=TEAL,
    )

    # Unit 3.4 Slide
    add_unit_lab_slide(
        prs,
        "Módulo 3 · Unidad 3.4 (6 hs) · Ejecución Agéntica, QA Cruzado y Demo Final",
        "Unidad 3.4: Dos Sprints de Implementación, Convergencia y Retrospectiva",
        "Ejecución real cronometrada de extremo a extremo sobre `GuardiaCloud.CommandCenter.sln`.",
        "Cronograma de las 6 Horas de Ejecución (360 min)",
        [
            "0:00 – 2:00 (Sprint 1 — Oráculo + Core): escribir primero los tests en `CommandCenterTests.cs` (`NetArchTest` + `WebApplicationFactory`) y resolver `BUG-301` y `FEAT-301`.",
            "2:00 – 2:30 (Checkpoint de Convergencia): integrar ramas del Sprint 1 a `main`, correr `dotnet test` y verificar alineación con `spec.md` (`/speckit-converge`).",
            "2:30 – 4:30 (Sprint 2 — Paralelización + UI): implementar `FEAT-302` (HITL) y `FEAT-303` (Full AI + integración con el prototipo UI).",
            "4:30 – 5:15 (QA Cruzado entre Equipos): el Equipo B ejecuta pruebas de aceptación contra la API del Equipo A usando únicamente su `spec.md`.",
            "5:15 – 6:00 (Demo en Vivo y Retrospectiva): presentación del sistema andando (Entregable #4 — 35%) y lectura de métricas (Entregable #5 — 10%).",
        ],
        "Suite Oráculo de Referencia (8 Tests en Verde)",
        [
            "$ dotnet test GuardiaCloud.CommandCenter.sln",
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
        "Cierre del Curso: Entregables #4 (35%) y #5 (10%)",
        [
            "Cada equipo se lleva un flujo SDD + Harness `.NET 10` probado en batalla y un informe de métricas reales para adoptar el lunes siguiente en sus proyectos de consultoría.",
        ],
        accent=PURPLE,
    )

    # Slide: Sistema de Evaluación y los 5 Entregables Calificados
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Evaluación y Acreditación · 100% Práctico",
        "Esquema de Evaluación del Curso: 5 Entregables Encadenados",
        "Cada entregable cuenta con una rúbrica analítica sobre 100 puntos y una solución de referencia compilable en .NET 10.",
        AMBER,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 2.45,
        "Módulos 1 y 2 · Fundamentos y SDD (30% de la Nota)",
        [
            "Entregable #1 (15% — Cierre Módulo 1, Unidades 1.3 + 1.5): Skill reutilizable (`SKILL.md` + verificador) + Servidor MCP en C# (`ModelContextProtocol` v2.3.0) + Agente `Microsoft.Extensions.AI` (`workshops/ws-m1-skills-mcp-dotnet`).",
            "Entregable #2 (15% — Cierre Módulo 2, Unidades 2.1 + 2.4): Especificación funcional/técnica EARS/GWT + ciclo Spec Kit `v1.2.5` + delta OpenSpec `v1.15.0` con tests en verde (`workshops/ws-m2-sdd-dotnet`).",
        ],
        accent=BLUE, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 2.45,
        "Módulo 3 · Proyecto Integrador Capstone (70% de la Nota)",
        [
            "Entregable #3 (25% — Unidades 3.1 a 3.3): Constitución `AGENTS.md`, `spec.md`, `plan.md`, Prototipo UI y Grafo de Tareas `tasks.md` auditados.",
            "Entregable #4 (35% — Unidad 3.4): Solución `.NET 10` funcionando en vivo, suite oráculo (`NetArchTest` + `WebApplicationFactory`) y Demo.",
            "Entregable #5 (10% — Cierre Unidad 3.4): Retrospectiva de ingeniería basada en métricas (`retrospectiva-metricas.md`).",
        ],
        accent=PURPLE, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 0.6, 4.42, 12.13, 2.45,
        "Mapa Completo de Workshops Listos en el Repositorio (`workshops/`)",
        [
            "1. `workshops/ws-m1-skills-mcp-dotnet/` → Guía paso a paso, guía del facilitador, rúbrica (15%), `starter/` (2 tests) y `solution/` (6 tests).",
            "2. `workshops/ws-m2-sdd-dotnet/` → Guía paso a paso, guía del facilitador, rúbrica (15%), `starter/` (2 tests + 1 bug) y `solution/` (4 suites).",
            "3. `workshops/ws-m2-harness-oracle-dotnet/` → Guía paso a paso, guía del facilitador, rúbrica, `starter/` (2 tests + violación de capa) y `solution/` (7 tests).",
            "4. `workshops/ws-m3-capstone-dotnet/` → Pliego del caso, guía de equipos, 3 rúbricas oficiales (70%), `starter/` (3 tests) y `solution/` (8 tests).",
        ],
        accent=TEAL, title_size=14.5, body_size=11.5,
    )


def main():
    root = Path(__file__).resolve().parent.parent
    slides_dir = root / "curriculum" / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    # 1. Master Full-Course Deck
    master_prs = new_prs()
    build_intro_slides(master_prs)
    build_module1_slides(master_prs)
    build_module2_slides(master_prs)
    build_module3_slides(master_prs)
    master_out = root / "curriculum" / "2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx"
    master_prs.save(str(master_out))
    print(f"saved {master_out.relative_to(root)} ({len(master_prs.slides)} slides)")

    # 2. Module 1 Standalone Deck
    m1_prs = new_prs()
    build_intro_slides(m1_prs)
    build_module1_slides(m1_prs)
    m1_out = slides_dir / "modulo-1-fundamentos-herramientas-agentes.pptx"
    m1_prs.save(str(m1_out))
    print(f"saved {m1_out.relative_to(root)} ({len(m1_prs.slides)} slides)")

    # 3. Module 2 Standalone Deck
    m2_prs = new_prs()
    build_module2_slides(m2_prs)
    m2_out = slides_dir / "modulo-2-spec-driven-development.pptx"
    m2_prs.save(str(m2_out))
    print(f"saved {m2_out.relative_to(root)} ({len(m2_prs.slides)} slides)")

    # 4. Module 3 Standalone Deck
    m3_prs = new_prs()
    build_module3_slides(m3_prs)
    m3_out = slides_dir / "modulo-3-capstone-proyecto-integrador.pptx"
    m3_prs.save(str(m3_out))
    print(f"saved {m3_out.relative_to(root)} ({len(m3_prs.slides)} slides)")


if __name__ == "__main__":
    main()
