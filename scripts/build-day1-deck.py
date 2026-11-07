#!/usr/bin/env python3
"""
Generate a detailed, minute-by-minute Step-by-Step PPTX deck for DAY 1 of the course:
"Desarrollo de Software con IA — Día 1 Paso a Paso (Unidades 1.1 y 1.2)"

Output:
  curriculum/2026-11-03_dia-1-paso-a-paso.pptx (16 slides, 16:9 widescreen)
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


def add_header(slide, tag_text: str, title_text: str, subtitle_text: str = "", tag_color=BLUE):
    set_bg(slide, LIGHT_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.10))
    bar.fill.solid()
    bar.fill.fore_color.rgb = tag_color
    bar.line.fill.background()

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.32), Inches(4.3), Inches(0.34))
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
    fp.text = "Desarrollo de Software con IA · Día 1 Paso a Paso (Unidades 1.1 y 1.2) · .NET 10 + Azure · VS Code / Cursor / Windsurf"
    fp.font.size = Pt(9.5)
    fp.font.color.rgb = MUTED
    fp.font.name = "Calibri"


def add_card(slide, left, top, width, height, title: str, bullets: list[str], accent=BLUE, title_size=15, body_size=12):
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


def add_cover(prs: Presentation, badge: str, title: str, subtitle: str, pills: list[tuple[str, str]], accent=TEAL):
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    set_bg(s, NAVY)

    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.95), Inches(5.6), Inches(0.42))
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
    p.font.size = Pt(38)
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
        bp1.font.size = Pt(21)
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
    fp.text = "Guía Paso a Paso del Día 1 · Repositorio Semilla: GuardiaCloud.Sla (.NET 10) · VS Code, Cursor y Windsurf"
    fp.font.size = Pt(12)
    fp.font.color.rgb = RGBColor(148, 163, 184)
    fp.font.name = "Calibri"


def build_day1_deck() -> Presentation:
    prs = new_prs()
    blank = prs.slide_layouts[6]

    # ------------------------------------------------------------------
    # SLIDE 1: Cover
    # ------------------------------------------------------------------
    add_cover(
        prs,
        "DÍA 1 · GUÍA PASO A PASO (8 HORAS / 2 UNIDADES)",
        "Día 1: Del Diseño con IA al Dominio\ndel IDE sobre Código .NET Legado",
        "Cronograma minuto a minuto, ejercicios prácticos, prompts, código C# y entregables de las Unidades 1.1 y 1.2.",
        [
            ("Bloque 1 (4 hs)", "Unidad 1.1: Diseño UI con IA\n+ Handoff a .NET 10"),
            ("Bloque 2 (4 hs)", "Unidad 1.2: VS Code, Cursor\ny Windsurf en .NET"),
            ("62.5% Práctica", "5 horas de laboratorio real\nen el Día 1 (2.5h + 2.5h)"),
            ("Hilo Conductor", "Todo corre sobre el repo\nGuardiaCloud.Sla (.NET 10)"),
        ],
        accent=TEAL,
    )

    # ------------------------------------------------------------------
    # SLIDE 2: Mapa Completo del Día 1 (Minuto a Minuto)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Día 1 · Agenda Minuto a Minuto",
        "Estructura Completa del Día 1 (Bloque Mañana + Bloque Tarde)",
        "Funciona tanto en modalidad Jornada Completa (8 hs = U1.1 + U1.2) como en dos medias jornadas de 4 hs.",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.45,
        "Bloque 1 (Mañana · 4 hs) — Unidad 1.1: Diseño y Handoff .NET",
        [
            "00:00 – 00:20 (20m) · Kickoff del curso + presentación del caso `GuardiaCloud.Sla`.",
            "00:20 – 01:00 (40m) · Mapa de herramientas UI (Stitch, v0, Lovable, Figma Make, Artifacts) y anatomía de un prompt de producto.",
            "01:00 – 01:30 (30m) · Design Systems (`design-tokens.json`) y patrones de Handoff hacia ASP.NET Core / Blazor.",
            "01:30 – 04:00 (2h 30m) · WORKSHOP 1.1 PASO A PASO: Diseño de las 3 pantallas del Monitor SLA, estados de borde, extracción de tokens y handoff tipado C#.",
        ],
        accent=BLUE, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.45,
        "Bloque 2 (Tarde · 4 hs) — Unidad 1.2: IDEs con IA en .NET",
        [
            "00:00 – 00:35 (35m) · Estandarización del IDE (VS Code + Copilot, Cursor, Windsurf), modos de interacción y paradoja METR (-19%).",
            "00:35 – 01:05 (30m) · Configuración de reglas (`.github/copilot-instructions.md`, `.cursor/rules`, `.windsurfrules`, `AGENTS.md`).",
            "01:05 – 01:30 (25m) · Riesgos reales en C#: paquetes NuGet alucinados, `N+1` en EF Core, falta de `CancellationToken` y secretos.",
            "01:30 – 04:00 (2h 30m) · WORKSHOP 1.2 PASO A PASO: Los 5 flujos diarios de ingeniería sobre el repositorio brownfield `GuardiaCloud.Sla.sln`.",
        ],
        accent=TEAL, title_size=14.5, body_size=11.5,
    )
    add_card(
        s, 0.6, 5.38, 12.13, 1.55,
        "Qué se llevan los participantes al terminar el Día 1",
        [
            "1) El prototipo navegable de 3 pantallas + `design-tokens.json` + DTOs/componentes conectados a `GuardiaCloud.Sla.Api`.",
            "2) Su IDE (VS Code, Cursor o Windsurf) configurado con reglas de arquitectura .NET 10 y un PR con 5 tareas reales verificadas con `dotnet test`.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 3: Setup Pre-Vuelo y el Caso Hilo Conductor (Primeros 20 min)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Día 1 · 00:00 a 00:20 · Onboarding Técnico",
        "Paso 0: Verificación de Entorno y Presentación del Caso GuardiaCloud.Sla",
        "En los primeros 20 minutos todos los alumnos clonan el repositorio semilla y validan su entorno sin fricción.",
        TEAL,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.3,
        "El Dominio del Curso: GuardiaCloud.Sla (.NET 10)",
        [
            "Contexto: Plataforma B2B que monitorea acuerdos de nivel de servicio (SLA) para incidentes críticos (P1, P2, P3) de clientes bancarios y retail.",
            "Problema de negocio: Los operadores necesitan visualizar el consumo de SLA en tiempo real, registrar pausas justificadas ('esperando al cliente') y auditar incumplimientos.",
            "Por qué funciona en el aula: Es un dominio que todo ingeniero entiende en 5 minutos, pero tiene reglas temporales, husos horarios y contratos RFC 9457 donde la IA falla si no se la guía con precisión.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_code_card(
        s, 6.78, 1.75, 5.95, 3.3,
        "Checklist de Terminal (Minuto 0 del Día 1)",
        [
            "# 1. Verificar SDK de .NET 10 y Git",
            "$ dotnet --version   # -> 10.0.x",
            "$ git --version",
            "",
            "# 2. Entrar al proyecto base del Día 1 y correr tests",
            "$ cd workshops/ws-m1-dia1-proyecto-base-dotnet/starter",
            "$ dotnet test GuardiaCloud.Sla.sln",
            "# Passed! - Failed: 0, Passed: 2, Total: 2",
            "",
            "# 3. Abrir en VS Code, Cursor o Windsurf",
        ],
        accent=TEAL,
    )
    add_card(
        s, 0.6, 5.22, 12.13, 1.7,
        "Acuerdo de Trabajo en Aula (D-024)",
        [
            "Estandarizamos las demos y guías en VS Code (con GitHub Copilot), Cursor y Windsurf. Si algún participante prefiere usar otro IDE por su cuenta, los archivos `AGENTS.md` y la CLI de `.NET` garantizan compatibilidad total.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 4: Bloque 1 — Unidad 1.1 Teoría Enfocada (00:20 - 01:30)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.1 · 00:20 a 01:30 (70 min) · Encuadre y Demo en Vivo",
        "Diseño de Producto con IA: Cuándo Usar Cada Herramienta y Cómo Promptear",
        "Evitamos que el alumno use el generador de UI como una 'máquina tragamonedas' de pantallas inconexas.",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.3,
        "Matriz de Decisión de Herramientas UI (00:20 – 01:00)",
        [
            "Google Stitch (`stitch.withgoogle.com`): ideal para explorar rápido múltiples disposiciones visuales desde texto o bocetos.",
            "v0 (Vercel) y Lovable: ideales para generar flujos interactivos multi-pantalla con componentes limpios (shadcn/Tailwind).",
            "Figma Make: ideal cuando la consultora ya tiene un Design System corporativo en Figma y necesita extenderlo sin romper estilos.",
            "Claude Artifacts: ideal para prototipar calculadoras de reglas o micro-flujos interactivos frente al cliente en 2 minutos.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.3,
        "Las 5 Capas de un Prompt de Diseño Profesional (01:00 – 01:30)",
        [
            "1. Rol y Contexto Operativo: ¿Quién usa la pantalla y bajo qué presión? (ej. operador NOC con 40 incidentes abiertos).",
            "2. Jerarquía de Información: qué dato es primario (semáforo de SLA consumido %), secundario (tier del cliente) y terciario.",
            "3. Estados Explícitos: estado vacío, estado cargando, alerta de riesgo (>= 80%), incumplimiento (> 100%) y error RFC 9457.",
            "4. Tokens y Restricciones Visuales: paleta, tipografía, densidad de tabla y accesibilidad (contraste AA).",
            "5. Contrato de Datos: nombres exactos de los campos del DTO en C# para no inventar propiedades inexistentes.",
        ],
        accent=TEAL, title_size=15, body_size=12,
    )
    add_card(
        s, 0.6, 5.22, 12.13, 1.7,
        "Demo en Vivo del Instructor (15 min dentro del bloque)",
        [
            "Comparación en vivo: un prompt vago (*'haceme un dashboard de incidentes'*) vs. un prompt estructurado acoplado al DTO `IncidentSlaSummaryDto` de `GuardiaCloud.Sla`.",
        ],
        accent=PURPLE, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 5: Workshop 1.1 — Paso 1 y Paso 2 (01:30 - 02:45)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.1 · Workshop Paso a Paso · 01:30 a 02:45 (75 min)",
        "Workshop 1.1 (Parte A): Generación del Flujo de 3 Pantallas y Estados de Borde",
        "Los alumnos trabajan en duplas generando el flujo completo de GuardiaCloud.Sla a partir del contrato backend.",
        TEAL,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "Paso 1 (40 min): Las 3 Pantallas Nucleares",
        [
            "Pantalla 1 — Tablero de Guardia SLA: grilla filtrable por severidad (P1/P2/P3) con barra de progreso de SLA consumido y badge de estado (`En Tiempo`, `En Riesgo >=80%`, `Vencido`).",
            "Pantalla 2 — Drawer de Registro de Pausa: formulario modal para pausar el reloj de SLA seleccionando motivo (`WaitingForCustomer`, `MaintenanceWindow`) e intervalo UTC.",
            "Pantalla 3 — Vista de Auditoría e Incumplimiento: línea de tiempo que muestra tiempo bruto vs. tiempo pausado neto.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_code_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "Prompt Estructurado que Ejecutan los Alumnos",
        [
            "Contexto: Consola B2B 'GuardiaCloud SLA' para operadores.",
            "Datos exactos del backend (.NET 10 Minimal API):",
            "  - incidentId (string), severity (P1|P2|P3)",
            "  - consumedRatio (0.0 a 1.5), isBreached (bool)",
            "  - pauseReason (WaitingForCustomer | MaintenanceWindow)",
            "Tareas:",
            "1. Diseñar Tablero + Modal de Pausa + Timeline.",
            "2. Si severity == P1, mostrar aviso: 'Tope máx pausa: 30m'.",
            "3. Incluir banner de error RFC 9457 (código + traceId).",
        ],
        accent=TEAL,
    )
    add_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Paso 2 (35 min): Iteración de Estados de Borde (Sin Romper el Layout)",
        [
            "Cada dupla fuerza 3 estados críticos en su prototipo: (a) rechazo HTTP 422 `SLA-422-P1-PAUSE-CAP-EXCEEDED`, (b) incidente con 0 pausas vs. 5 pausas solapadas, y (c) fijación de paleta en `design-tokens.json`.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 6: Workshop 1.1 — Paso 3 y Paso 4 (02:45 - 04:00)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.1 · Workshop Paso a Paso · 02:45 a 04:00 (75 min)",
        "Workshop 1.1 (Parte B): Extracción de Tokens y Handoff al Proyecto .NET 10",
        "Cerramos la brecha entre el prototipo visual y la solución C# real (`GuardiaCloud.Sla.sln`).",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "Paso 3 (45 min): Handoff Diseño → Código .NET",
        [
            "Exportar los tokens visuales a `ui/design-tokens.json` en la raíz del repositorio `GuardiaCloud.Sla`.",
            "Usar el agente del IDE (VS Code / Cursor / Windsurf) para transformar el HTML/Tailwind generado en un componente tipado (Blazor `.razor` o cliente TypeScript conectado al OpenAPI de `GuardiaCloud.Sla.Api`).",
            "Verificar que ningún nombre de propiedad haya sido inventado por la herramienta de diseño.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_code_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "Artefacto Generado: Componente Conectado al DTO C#",
        [
            "@* SlaStatusCard.razor — Handoff verificado *@",
            "<div class=\"sla-card @(Model.IsBreached ? \"border-red\" : \"\")\">",
            "  <header>",
            "    <span class=\"badge\">@Model.Severity</span>",
            "    <h4>@Model.IncidentId</h4>",
            "  </header>",
            "  <progress value=\"@Model.ConsumedRatio\" max=\"1.0\" />",
            "  @if (Model.ConsumedRatio >= 0.80 && !Model.IsBreached) {",
            "    <p class=\"alert-amber\">En riesgo de SLA (>=80%)</p>",
            "  }",
            "</div>",
        ],
        accent=TEAL,
    )
    add_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Paso 4 (30 min): Revisión Cruzada y Cierre del Bloque 1",
        [
            "Checklist de salida de la Unidad 1.1: ✓ 3 pantallas navegables · ✓ `design-tokens.json` versionado en Git · ✓ Estados de error RFC 9457 contemplados · ✓ Componente acoplado sin errores de tipos.",
        ],
        accent=PURPLE, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 7: Bloque 2 Cover — Unidad 1.2 (Herramientas de Desarrollo)
    # ------------------------------------------------------------------
    add_cover(
        prs,
        "DÍA 1 · BLOQUE 2 (4 HORAS) · UNIDAD 1.2",
        "Herramientas de Desarrollo con IA:\nVS Code, Cursor y Windsurf en .NET 10",
        "Configuración profesional del workspace, prevención de anti-patrones C# y los 5 flujos diarios sobre código legado.",
        [
            ("00:00 – 01:30", "Modos de IDE, Reglas y\nRiesgos en C# (90 min)"),
            ("01:30 – 04:00", "Workshop Práctico: 5 Flujos\nsobre Código Legado (150m)"),
            ("IDEs Estándar", "VS Code + Copilot,\nCursor y Windsurf"),
            ("Verificación", "Todo cambio pasa por\ndotnet build + dotnet test"),
        ],
        accent=BLUE,
    )

    # ------------------------------------------------------------------
    # SLIDE 8: Unidad 1.2 — Encuadre y Configuración de Reglas (00:00 - 01:30)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.2 · 00:00 a 01:30 (90 min) · Teoría Aplicada y Configuración",
        "Configuración de VS Code, Cursor y Windsurf para Ingeniería .NET",
        "Por qué el mismo modelo produce código excelente o deuda técnica según cómo esté configurado el workspace.",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "1. Modos del IDE y Archivos de Reglas (00:00 – 01:05)",
        [
            "Cuándo usar cada modo: Tab/Autocomplete (1–3 líneas), Inline Edit (`Cmd+I` / `Ctrl+I`, refactor local de un método) vs. Agent Mode (cambio coordinado entre `Domain`, `Api` y `Tests`).",
            "Configuración unificada en el repo para que todo el equipo comparta las mismas reglas sin importar si abren VS Code, Cursor o Windsurf:",
            "  • `AGENTS.md` en la raíz (leído por Copilot, Cursor, Windsurf y Codex).",
            "  • `.github/copilot-instructions.md` y `.cursor/rules/dotnet10.mdc`.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "2. Los 4 Errores Clásicos de la IA en C# (01:05 – 01:30)",
        [
            "Alucinación de NuGet (*Slopsquatting*): el agente sugiere paquetes inexistentes o mezcla sintaxis vieja de `Swashbuckle` con `Microsoft.AspNetCore.OpenApi` de .NET 10.",
            "Consultas `N+1` y carga en memoria: hacer `.ToList()` antes de filtrar en EF Core o iterar consultas dentro de un `foreach`.",
            "Asincronía rota: omitir `CancellationToken` en endpoints Minimal API o bloquear hilos con `.Result` / `.Wait()`.",
            "Tiempo no determinista: usar `DateTime.UtcNow` directo en vez de `TimeProvider`, haciendo imposible testear bordes de SLA.",
        ],
        accent=TEAL, title_size=15, body_size=12,
    )
    add_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Ejercicio de Calentamiento (15 min): Escribir las Reglas del Workspace",
        [
            "Antes de tocar el código C#, cada alumno crea y commitea las reglas de su IDE prohibiendo `DateTime.Now`, exigiendo `CancellationToken` y obligando a correr `dotnet test` antes de dar una tarea por terminada.",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    # ------------------------------------------------------------------
    # SLIDE 9: Workshop 1.2 — Flujo 1 y Flujo 2 (01:30 - 02:25)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.2 · Workshop Paso a Paso · 01:30 a 02:25 (55 min)",
        "Flujos 1 y 2: Comprensión de Legado y Refactoring Seguro en C# 13",
        "Trabajamos sobre el código brownfield de GuardiaCloud.Sla usando VS Code, Cursor o Windsurf.",
        TEAL,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "Flujo 1 (25 min): Arqueología y Mapa de Código Legado",
        [
            "Objetivo: Entender una base de código desconocida en minutos verificando cada afirmación del asistente contra el AST/código real.",
            "Acción del alumno: Pedir al IDE (`#codebase` / `@workspace`) el diagrama de secuencia desde `POST /api/incidents/{id}/evaluate` hasta `SlaCalculator.Evaluate` e identificar dónde se pierden las zonas horarias.",
            "Trampa didáctica: Detectar un comentario engañoso dejado en el código legado que contradice lo que realmente hace el método.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "Flujo 2 (30 min): Refactoring Seguro con Red de Pruebas",
        [
            "Objetivo: Refactorizar un método complejo de 90 líneas con `if/else` anidados a *pattern matching* exhaustivo de C# 13 sin alterar su comportamiento.",
            "Acción del alumno: Usar Inline Edit / Agent Mode para extraer funciones puras en `SlaCalculator.cs`, inyectar `TimeProvider` y verificar en cada paso con `dotnet test`.",
            "Criterio de aceptación: Cero warnings de compilador (`TreatWarningsAsErrors=true`) y 100% de tests previos pasando.",
        ],
        accent=TEAL, title_size=15, body_size=12,
    )
    add_code_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Antes vs. Después del Refactoring C# 13 (Verificado con dotnet test)",
        [
            "// ANTES (Legado frágil): if (inc.Tier == \"P1\") { max = 60; } else if ...",
            "// DESPUÉS (C# 13 Switch Expression puro y exhaustivo):",
            "public static TimeSpan GetTargetResponseWindow(SeverityTier tier) => tier switch {",
            "    SeverityTier.P1 => TimeSpan.FromMinutes(60),  SeverityTier.P2 => TimeSpan.FromHours(4),",
            "    SeverityTier.P3 => TimeSpan.FromHours(24),    _ => throw new ArgumentOutOfRangeException(nameof(tier)) };",
        ],
        accent=BLUE,
    )

    # ------------------------------------------------------------------
    # SLIDE 10: Workshop 1.2 — Flujo 3 y Flujo 4 (02:25 - 03:30)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.2 · Workshop Paso a Paso · 02:25 a 03:30 (65 min)",
        "Flujos 3 y 4: Generación de Tests xUnit y Debugging Asistido",
        "Cómo evitar tests tautológicos (que prueban el mock) y cómo diagnosticar bugs reales con el agente.",
        BLUE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "Flujo 3 (35 min): Tests de Casos Borde con FakeTimeProvider",
        [
            "El problema clásico: Si le pedís a la IA *'escribí tests para SlaCalculator'*, suele generar 5 tests felices redundantes que solo prueban que el código hace lo que ya hace.",
            "Acción del alumno: Guiar al IDE para generar una matriz `[Theory]` en xUnit cubriendo bordes reales: (1) exactamente en el minuto límite (60.0m), (2) cruce de medianoche UTC, (3) pausas solapadas, y (4) incidente ya resuelto.",
            "Uso de `Microsoft.Extensions.TimeProvider.Testing` (`FakeTimeProvider`) para avanzar el reloj sin `Thread.Sleep`.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "Flujo 4 (30 min): Debugging del Bug de ResolvedAtUtc",
        [
            "Al correr los nuevos tests de borde del Flujo 3, ¡uno falla! Cuando un incidente ya está cerrado (`ResolvedAtUtc != null`), pero se consulta el tablero horas después, el sistema lo marca falsamente como vencido.",
            "Acción del alumno: Pasar el output fallido de `dotnet test` al agente en VS Code / Cursor / Windsurf, pedirle la hipótesis de causa raíz y aplicar el fix mínimo en `SlaCalculator.cs` (`var effectiveEnd = incident.ResolvedAtUtc ?? nowUtc;`).",
        ],
        accent=TEAL, title_size=15, body_size=12,
    )
    add_code_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Test de Regresión que Cierra el Flujo 4 en GuardiaCloud.Sla.Tests",
        [
            "[Fact]",
            "public void Evaluate_Uses_ResolvedAtUtc_Instead_Of_CurrentTime_When_Incident_Is_Closed() {",
            "    var clock = new FakeTimeProvider(new DateTimeOffset(2026, 10, 30, 18, 0, 0, TimeSpan.Zero));",
            "    var status = SlaCalculator.Evaluate(openedAt_10_00, resolvedAt_10_45, SeverityTier.P1, clock.GetUtcNow());",
            "    Assert.False(status.IsBreached); // 45m <= 60m P1 SLA, aunque el reloj actual sea 8 horas después",
            "}",
        ],
        accent=TEAL,
    )

    # ------------------------------------------------------------------
    # SLIDE 11: Workshop 1.2 — Flujo 5 y Cierre del Día 1 (03:30 - 04:00)
    # ------------------------------------------------------------------
    s = prs.slides.add_slide(blank)
    add_header(
        s,
        "Unidad 1.2 · Workshop Paso a Paso · 03:30 a 04:00 (30 min)",
        "Flujo 5: Code Review Asistido de Seguridad y Performance + Cierre del Día 1",
        "Auditoría de un Pull Request contaminado antes de que llegue a producción.",
        PURPLE,
    )
    add_card(
        s, 0.6, 1.75, 5.95, 3.35,
        "Flujo 5 (30 min): Auditoría de un PR 'Vibe-Codeado'",
        [
            "Los alumnos abren la rama `pr/vibe-coded-export` que simula un PR generado sin supervisión.",
            "Usando su IDE con una checklist estructurada de revisión, deben encontrar y corregir los 4 defectos sembrados:",
            "  1. Connection string con clave de Azure hardcodeada.",
            "  2. Endpoint Minimal API sin `CancellationToken` ni límite de paginación.",
            "  3. Consulta `N+1` iterando pausas por cada incidente.",
            "  4. Excepción cruda 500 en lugar de `ProblemDetails` RFC 9457.",
        ],
        accent=PURPLE, title_size=15, body_size=12,
    )
    add_card(
        s, 6.78, 1.75, 5.95, 3.35,
        "Conexión Directa con los Días 2 y 3 del Curso",
        [
            "Al terminar el Día 1, los alumnos comprobaron en carne propia que las reglas manuales en el IDE ayudan, pero necesitan automatización.",
            "Eso abre la puerta directamente al **Día 2 (Unidades 1.3, 1.4 y 1.5)**:",
            "  • Convertir la checklist del Flujo 5 en una **Agent Skill (`SKILL.md` + `verify-minimal-api.sh`)**.",
            "  • Automatizar `dotnet build/test` en un **Hook `PostToolUse`** de Claude Code / Codex.",
            "  • Exponer `SlaCalculator` en un **Servidor MCP en C# (`ModelContextProtocol` v2.3.0)**.",
        ],
        accent=BLUE, title_size=15, body_size=12,
    )
    add_card(
        s, 0.6, 5.25, 12.13, 1.68,
        "Resumen de Entregables Completados en el Día 1",
        [
            "✓ Prototipo UI de 3 pantallas + `design-tokens.json` + componente tipado (U1.1) · ✓ Reglas de workspace en VS Code / Cursor / Windsurf + 5 flujos en verde con `dotnet test` (U1.2).",
        ],
        accent=AMBER, title_size=14, body_size=11.5,
    )

    return prs


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "curriculum" / "2026-11-03_dia-1-paso-a-paso.pptx"
    out.parent.mkdir(parents=True, exist_ok=True)
    prs = build_day1_deck()
    prs.save(str(out))
    print(f"saved {out} ({len(prs.slides)} slides)")
