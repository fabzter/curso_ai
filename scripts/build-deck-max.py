#!/usr/bin/env python3
"""Build the Temario v2 + Workshops deck for the sync with Max (python-pptx).

Usage: python3 scripts/build-deck-max.py [output.pptx]
Content source: curriculum/2026-10-30_temario-v2-propuesta.md and
curriculum/2026-10-30_update-async-para-max.md. Edit SLIDES below and re-run.
"""
import sys
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = sys.argv[1] if len(sys.argv) > 1 else "curriculum/2026-11-03_deck-temario-v2-para-max.pptx"

NAVY = RGBColor(0x14, 0x21, 0x3D)
ACCENT = RGBColor(0x2E, 0x86, 0xDE)
TEAL = RGBColor(0x1A, 0xB0, 0x9A)
GREY = RGBColor(0x5F, 0x6B, 0x7A)
LIGHT = RGBColor(0xF3, 0xF6, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def rect(slide, x, y, w, h, color):
    shp = slide.shapes.add_shape(1, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return shp


def text(slide, x, y, w, h, value, size=18, bold=False, color=NAVY, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    lines = value if isinstance(value, list) else [value]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.color.rgb = Pt(size), bold, color
        r.font.name = "Calibri"
    return tb


def bullets(slide, x, y, w, h, items, size=18):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        sub = item.startswith("  ")
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = ("– " if sub else "• ") + item.strip()
        r.font.size = Pt(size - 3 if sub else size)
        r.font.color.rgb = GREY if sub else NAVY
        r.font.name = "Calibri"
        if sub:
            p.level = 1
    return tb


def header(slide, title, kicker=None, n=None):
    rect(slide, 0, 0, W, Inches(1.15), NAVY)
    rect(slide, 0, Inches(1.15), W, Inches(0.06), ACCENT)
    text(slide, Inches(0.6), Inches(0.22), Inches(11.5), Inches(0.8), title, 30, True, WHITE)
    if kicker:
        text(slide, Inches(0.6), Inches(1.35), Inches(12), Inches(0.5), kicker, 16, False, ACCENT)
    if n:
        text(slide, Inches(12.3), Inches(7.0), Inches(0.8), Inches(0.4), str(n), 11, False, GREY, PP_ALIGN.RIGHT)


def table(slide, x, y, w, rows, col_w, size=13, row_h=0.42):
    t = slide.shapes.add_table(len(rows), len(rows[0]), x, y, w, Inches(row_h * len(rows))).table
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = NAVY if i == 0 else (LIGHT if i % 2 else WHITE)
            for p in c.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(size)
                    r.font.bold = i == 0 or (j == 0 and val.startswith("Total"))
                    r.font.color.rgb = WHITE if i == 0 else NAVY
                    r.font.name = "Calibri"
    return t


def card(slide, x, y, w, h, title, lines, color=ACCENT):
    rect(slide, x, y, w, h, LIGHT)
    rect(slide, x, y, Inches(0.09), h, color)
    text(slide, x + Inches(0.25), y + Inches(0.12), w - Inches(0.35), Inches(0.5), title, 17, True, NAVY)
    bullets(slide, x + Inches(0.25), y + Inches(0.65), w - Inches(0.4), h - Inches(0.7), lines, 14)


n = 0

# 1 — Title
n += 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
rect(s, Inches(0.8), Inches(3.55), Inches(2.2), Inches(0.08), ACCENT)
text(s, Inches(0.8), Inches(1.9), Inches(11.5), Inches(1.2), "Desarrollo de Software con IA", 48, True, WHITE)
text(s, Inches(0.8), Inches(2.85), Inches(11.5), Inches(0.7), "Temario v2 + Workshops construidos", 26, False, ACCENT)
text(s, Inches(0.8), Inches(3.9), Inches(11.5), Inches(1.2),
     ["Max Déboli & Fabrizio Hernández", "Curso presencial · 52 hs · 3 módulos · .NET + Azure"], 18, False, WHITE)
text(s, Inches(0.8), Inches(6.6), Inches(11.5), Inches(0.5), "Sync de revisión · noviembre 2026", 13, False, GREY)

# 2 — What stays
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Lo que se mantiene de tu draft (v1)", "La estructura maestra queda intacta", n)
card(s, Inches(0.6), Inches(2.1), Inches(5.9), Inches(4.6), "Estructura", [
    "52 hs · 3 módulos · 13 unidades",
    "Herramientas (20 hs) → Metodología SDD (18 hs) → Proyecto (14 hs)",
    "Todo encadena hacia el proyecto integrador",
    "Equipos de 3–5 personas en el Módulo 3",
])
card(s, Inches(6.8), Inches(2.1), Inches(5.9), Inches(4.6), "Evaluación (sin cambios)", [
    "Skill + servidor MCP · 15%",
    "Spec y plan de una feature · 15%",
    "Specs y plan del proyecto · 25%",
    "Proyecto funcionando + demo · 35%",
    "Retrospectiva con métricas · 10%",
], TEAL)

# 3 — Four improvements
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Las 4 mejoras de la v2", None, n)
items = [
    ("1. Práctica real ~70%", ["Cada unidad tiene un workshop de 1h15m a 3h45m", "Sin quitar temas: se compacta la teoría"]),
    ("2. Aterrizado a .NET + Azure", ["MCP y agentes en C# (en lugar de Python/TS)", "Oráculo de tests y arquitectura en .NET"]),
    ("3. Repo semilla brownfield", ["Un mismo dominio de punta a punta", "El Módulo 3 arranca con código andando"]),
    ("4. Workshops ya construidos", ["4 paquetes con código, guías y rúbricas", "Starter + solución, tests en verde"]),
]
for i, (t, ls) in enumerate(items):
    x = Inches(0.6 + (i % 2) * 6.2)
    y = Inches(1.6 + (i // 2) * 2.85)
    card(s, x, y, Inches(5.9), Inches(2.6), t, ls, ACCENT if i % 2 == 0 else TEAL)

# 4 — Practice chart
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Práctica guiada real: v1 vs. v2", "Horas explícitamente prácticas sobre el total de cada módulo", n)
cd = CategoryChartData()
cd.categories = ["Módulos 1–2 (38 hs)", "Curso completo (52 hs)"]
cd.add_series("v1 (draft)", (36.2, 50.5))
cd.add_series("v2 (propuesta)", (62.5, 69.7))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(2.0), Inches(7.6), Inches(5.0), cd).chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.plots[0].has_data_labels = True
ch.plots[0].data_labels.number_format = '0.0"%"'
ch.plots[0].data_labels.number_format_is_linked = False
ch.value_axis.maximum_scale = 100
ch.value_axis.has_major_gridlines = False
for i, col in enumerate((GREY, ACCENT)):
    ch.series[i].format.fill.solid()
    ch.series[i].format.fill.fore_color.rgb = col
bullets(s, Inches(8.6), Inches(2.3), Inches(4.3), Inches(4.5), [
    "v1 declaraba 60–70% práctico; sumando bloques prácticos daba ~36% en M1–2",
    "v2: 23,75 de 38 hs en M1–2",
    "v2: 36,25 de 52 hs en total",
    "M3 queda en ~89% práctico",
], 16)
text(s, Inches(0.6), Inches(7.0), Inches(8), Inches(0.4),
     "v1 total estimado con M3 = 12,5 hs prácticas (cálculo propio sobre el draft)", 10, False, GREY)

# 5 — Tools
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Stack y herramientas: simple y estándar", None, n)
card(s, Inches(0.6), Inches(1.6), Inches(3.9), Inches(5.3), "IDEs del curso", [
    "VS Code + GitHub Copilot",
    "Cursor",
    "Windsurf",
    "Cada dev puede usar el suyo; demos y soporte van sobre estos tres",
])
card(s, Inches(4.75), Inches(1.6), Inches(3.9), Inches(5.3), "Harness / agentes", [
    "Claude Code",
    "OpenAI Codex",
    "GitHub Copilot (agent)",
    "Devin y Kiro: demo guiada si no hay licencias",
], TEAL)
card(s, Inches(8.9), Inches(1.6), Inches(3.9), Inches(5.3), ".NET + SDD", [
    "Agentes en C#: Microsoft.Extensions.AI",
    "MCP: SDK oficial de C#",
    "Oráculo: xUnit + NetArchTest",
    "SDD: GitHub Spec Kit + OpenSpec",
])

# 6 — Module map
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Mapa del curso: 13 unidades", None, n)
rows = [["Unidad", "Hs", "Workshop", "Unidad", "Hs", "Workshop"],
        ["1.1 Diseño", "4", "2:30", "2.1 Spec", "4", "2:30"],
        ["1.2 Herramientas dev", "4", "2:30", "2.2 Estimación y planning", "4", "2:30"],
        ["1.3 Agentes y Skills", "4", "2:30", "2.3 Full AI vs. HITL", "4", "2:30"],
        ["1.4 Harness Engineering", "6", "3:45", "2.4 Herramientas SDD", "6", "3:45"],
        ["1.5 MCP", "2", "1:15", "3.1 Entendimiento funcional", "2", "1:30"],
        ["", "", "", "3.2 Specs y diseño", "4", "3:30"],
        ["", "", "", "3.3 Planificación", "2", "1:45"],
        ["", "", "", "3.4 Implementación y demo", "6", "5:45"],
        ["Total M1", "20", "12:30", "Total M2 / M3", "18 / 14", "11:15 / 12:30"]]
table(s, Inches(0.6), Inches(1.6), Inches(12.1), rows, [3.1, 0.8, 1.15, 4.0, 1.15, 1.9], 14, 0.5)

# 7 — Seed domain
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Hilo conductor: un dominio brownfield único", "GuardiaCloud.Sla — auditoría y liquidación de SLAs para banca y seguros", n)
bullets(s, Inches(0.6), Inches(2.1), Inches(6.2), Inches(4.8), [
    "En consultoría el trabajo diario es sobre sistemas existentes, no proyectos vacíos",
    "El mismo dominio aparece en M1, M2 y M3",
    "Cada unidad agrega una pieza del harness que el equipo reutiliza en M3",
    "  AGENTS.md, Skill de equipo, servidor MCP, flujo SDD, oráculo de tests",
    "El Módulo 3 arranca con una solución .NET compilando y tests en verde",
], 18)
card(s, Inches(7.2), Inches(2.1), Inches(5.5), Inches(4.6), "Por qué importa para M3 (14 hs)", [
    "Cero tiempo perdido en boilerplate",
    "Bug productivo sembrado + 3 vertical slices",
    "Equipos de 3–5 trabajan en paralelo sin pisarse",
    "Demo y métricas reales al cierre",
], TEAL)

# 8-11 — Workshops
ws = [
    ("Workshop M1 · Unidades 1.3 + 1.5", "Skill de equipo + servidor MCP en C# + agente · Entregable #1 (15%)", [
        "Skill de equipo (SKILL.md) con carga progresiva y script validador",
        "Servidor MCP en C# con 3 herramientas de solo lectura",
        "Defensa contra prompt injection indirecto (ticket con instrucción maliciosa)",
        "Agente de triage en C# con condiciones de parada",
        "Tests 100% offline en el aula: no requiere llaves de API",
    ]),
    ("Workshop M2 · Unidades 2.1 + 2.4", "De un brief ambiguo a código verificado · Entregable #2 (15%)", [
        "Role-play con el \"cliente\": destrabar 7 ambigüedades ocultas",
        "Requerimientos en EARS + escenarios Given/When/Then",
        "Spec Kit: bugfix + feature completa hasta convergencia spec ↔ código",
        "OpenSpec: cambio regulatorio brownfield con specs delta",
    ]),
    ("Workshop Harness & Oráculo · Unidades 1.4 + 2.3", "El harness y los tests deciden la calidad, no el prompt", [
        "Reemplazar un AGENTS.md inflado por uno curado (+ CLAUDE.md puente)",
        "Hook post-edición: compila y corre tests en cada cambio del agente",
        "Reglas de arquitectura con NetArchTest atrapan código \"vibe-coded\"",
        "Laboratorio en git worktrees: tarea financiera en HITL vs. tarea operativa en Full AI",
        "Comparativa con métricas: tiempo de generación vs. revisión",
    ]),
    ("Capstone M3 · Unidades 3.1 – 3.4 (14 hs)", "Entregables #3 (25%), #4 (35%) y #5 (10%)", [
        "Pliego del cliente con 8 ambigüedades para la entrevista (3.1)",
        "Specs EARS/GWT + spec técnica + prototipo UI + revisión cruzada (3.2)",
        "Plan paralelizable por roles y worktrees (3.3)",
        "2 sprints + checkpoint de convergencia + QA cruzado + demo (3.4)",
        "1 bug de idempotencia + 3 features: escalamiento al 80%, exención con doble firma, tablero ejecutivo",
    ]),
]
for title, kicker, ls in ws:
    n += 1
    s = prs.slides.add_slide(BLANK)
    header(s, title, kicker, n)
    bullets(s, Inches(0.6), Inches(2.1), Inches(7.6), Inches(4.9), ls, 18)
    card(s, Inches(8.6), Inches(2.1), Inches(4.1), Inches(4.6), "Cada paquete incluye", [
        "Spec del workshop y agenda",
        "Guía paso a paso (voseo)",
        "Guía del facilitador + rúbrica",
        "Starter .NET compilando",
        "Solución de referencia con tests en verde",
    ], TEAL)

# 12 — Evaluation
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Evaluación: 100% práctica y acumulativa", None, n)
rows = [["Entregable", "Momento", "Peso", "Workshop que lo cubre"],
        ["1. Skill + servidor MCP en C#", "Fin M1", "15%", "Workshop M1"],
        ["2. Spec + plan de una feature", "Fin M2", "15%", "Workshop M2 SDD"],
        ["3. Constitución, specs y plan del proyecto", "M3 (3.2–3.3)", "25%", "Capstone"],
        ["4. Proyecto funcionando + oráculo + demo", "M3 (3.4)", "35%", "Capstone"],
        ["5. Retrospectiva con métricas", "Cierre", "10%", "Capstone"]]
table(s, Inches(0.6), Inches(1.7), Inches(12.1), rows, [4.6, 2.0, 1.2, 4.3], 16, 0.62)
text(s, Inches(0.6), Inches(5.9), Inches(12), Inches(0.8),
     "El workshop de Harness & Oráculo no pesa por sí solo: es la base técnica obligatoria del Capstone.", 15, False, GREY)

# 13 — To decide
n += 1
s = prs.slides.add_slide(BLANK)
header(s, "Para definir juntos", None, n)
card(s, Inches(0.6), Inches(1.6), Inches(5.9), Inches(5.3), "Preguntas abiertas", [
    "¿El stack de la consultora es mayormente .NET + Azure?",
    "¿GitHub o Azure DevOps?",
    "Licencias en el aula: ¿1 harness por persona?",
    "Headcount, seniority y uso previo de IA",
    "Fecha de inicio y formato (días / horarios)",
])
card(s, Inches(6.8), Inches(1.6), Inches(5.9), Inches(5.3), "Próximos pasos propuestos", [
    "Validar temario v2 con tu feedback",
    "Workshops faltantes: 1.1, 1.2 y 2.2",
    "Slides por unidad y dry-run interno",
    "Re-verificar versiones de herramientas cerca de la fecha",
], TEAL)

prs.save(OUT)
print(f"saved {OUT} ({n} slides)")
