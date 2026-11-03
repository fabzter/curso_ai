#!/usr/bin/env python3
"""
Generate the actual CLASSROOM TEACHING PRESENTATIONS (.pptx, 16:9 widescreen)
to project to students during the 52-hour course "Desarrollo de Software con IA (.NET 10 + Azure)".

Each of the 13 Units gets its own complete classroom slide deck (12 slides per unit = 156 slides total),
plus 3 Module decks and 1 Master Full-Course deck (156 slides), written to:
  1. /Users/fabzter/Documents/curso_ai/presentaciones/
  2. /Users/fabzter/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge/01_projects/Curso Desarrollo de Software con IA/Presentaciones/
"""
import shutil
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

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.32), Inches(4.8), Inches(0.34))
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
    fp.text = "Desarrollo de Software con IA (.NET 10 + Azure) · Material de Clase"
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

    pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.95), Inches(6.0), Inches(0.42))
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
    p.font.size = Pt(36)
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
        bp1.font.size = Pt(19)
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
    fp.text = "Desarrollo de Software con IA · Presentación de Aula · .NET 10 + Azure · VS Code, Cursor y Windsurf"
    fp.font.size = Pt(12)
    fp.font.color.rgb = RGBColor(148, 163, 184)
    fp.font.name = "Calibri"

    if notes:
        s.notes_slide.notes_text_frame.text = notes


def add_teaching_slide(prs: Presentation, tag: str, title: str, subtitle: str,
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
# DATA-DRIVEN FULL UNIT CLASSROOM DECK DEFINITIONS (10–12 SLIDES PER UNIT)
# ==============================================================================
from classroom_units_data import UNITS_DATA


def render_unit_into(prs: Presentation, unit: dict):
    accent = {"BLUE": BLUE, "TEAL": TEAL, "PURPLE": PURPLE, "AMBER": AMBER}.get(unit.get("accent", "BLUE"), BLUE)
    add_cover(
        prs,
        unit["badge"],
        unit["title"],
        unit["subtitle"],
        unit["pills"],
        accent=accent,
        notes=unit.get("cover_notes", ""),
    )
    for sl in unit["slides"]:
        sl_accent = {"BLUE": BLUE, "TEAL": TEAL, "PURPLE": PURPLE, "AMBER": AMBER}.get(sl.get("accent", unit.get("accent", "BLUE")), accent)
        add_teaching_slide(
            prs,
            sl["tag"],
            sl["title"],
            sl["subtitle"],
            sl["left_title"],
            sl["left_bullets"],
            sl["right_title"],
            sl["right_items"],
            sl["right_is_code"],
            sl["bottom_title"],
            sl["bottom_bullets"],
            accent=sl_accent,
            notes=sl.get("notes", ""),
        )


def main():
    root = Path(__file__).resolve().parent.parent
    out_dir = root / "presentaciones"
    out_dir.mkdir(parents=True, exist_ok=True)

    vault_pres_dir = Path("/Users/fabzter/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge/01_projects/Curso Desarrollo de Software con IA/Presentaciones")
    vault_attach_dir = Path("/Users/fabzter/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge/99_attachments/Curso Desarrollo de Software con IA/presentaciones")

    master_prs = new_prs()
    module_prs = {
        1: new_prs(),
        2: new_prs(),
        3: new_prs(),
    }

    for unit in UNITS_DATA:
        u_prs = new_prs()
        render_unit_into(u_prs, unit)
        render_unit_into(master_prs, unit)
        render_unit_into(module_prs[unit["module"]], unit)

        u_path = out_dir / unit["filename"]
        u_prs.save(str(u_path))
        print(f"saved {u_path.relative_to(root)} ({len(u_prs.slides)} slides)")

    # Save Module Decks
    mod_names = {
        1: "00-Modulo-1-Completo-Fundamentos-Agentes-Harness-MCP.pptx",
        2: "00-Modulo-2-Completo-Spec-Driven-Development-SDD.pptx",
        3: "00-Modulo-3-Completo-Proyecto-Integrador-Capstone.pptx",
    }
    for m_num, m_prs in module_prs.items():
        m_path = out_dir / mod_names[m_num]
        m_prs.save(str(m_path))
        print(f"saved {m_path.relative_to(root)} ({len(m_prs.slides)} slides)")

    # Save Master Full Course Deck
    master_path = out_dir / "00-CURSO-COMPLETO-52HS-TODAS-LAS-CLASES.pptx"
    master_prs.save(str(master_path))
    print(f"saved {master_path.relative_to(root)} ({len(master_prs.slides)} slides)")

    # Also update curriculum/2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx with the full classroom master deck
    shutil.copy2(master_path, root / "curriculum" / "2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx")

    # Copy all into Obsidian Vault project folder (`01_projects/.../Presentaciones/`) and `99_attachments/`
    if vault_pres_dir.parent.exists():
        vault_pres_dir.mkdir(parents=True, exist_ok=True)
        vault_attach_dir.mkdir(parents=True, exist_ok=True)
        for p in out_dir.glob("*.pptx"):
            shutil.copy2(p, vault_pres_dir / p.name)
            shutil.copy2(p, vault_attach_dir / p.name)
        print(f"synced all {len(list(out_dir.glob('*.pptx')))} classroom decks to Obsidian Vault (`01_projects/.../Presentaciones/`)")


if __name__ == "__main__":
    main()
