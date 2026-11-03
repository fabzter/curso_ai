#!/usr/bin/env python3
"""
Bidirectional Course Material Pipeline for `curso_ai`:
  1. `build`         -> Regenerates all .md, .docx, and .pptx course deliverables and updates `.course-manifest.json`.
  2. `publish-vault` -> Publishes all Markdown notes to `knowledge/01_projects/Curso Desarrollo de Software con IA/`
                        and all .docx/.pptx deliverables to `knowledge/99_attachments/Curso Desarrollo de Software con IA/`.
  3. `status`        -> Detects manual edits in any .docx, .pptx, or Obsidian Vault file compared to `.course-manifest.json`.
  4. `ingest`        -> Extracts changes from edited .docx, .pptx, or Obsidian Vault files into `curriculum/.ingested/`
                        (and with `--apply`, retroactively updates the canonical Markdown docs in `curriculum/`).
"""
import argparse
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / ".course-manifest.json"
INGEST_DIR = ROOT / "curriculum" / ".ingested"

VAULT_ROOT = Path("/Users/fabzter/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge")
VAULT_PROJECT_DIR = VAULT_ROOT / "01_projects" / "Curso Desarrollo de Software con IA"
VAULT_ATTACH_DIR = VAULT_ROOT / "99_attachments" / "Curso Desarrollo de Software con IA"

# Mapping of canonical repo Markdown <-> DOCX export
DOCX_PAIRS = [
    (
        ROOT / "curriculum" / "2026-10-30_temario-v2-propuesta.md",
        ROOT / "curriculum" / "2026-10-30_temario-v2-propuesta.docx",
    ),
    (
        ROOT / "curriculum" / "2026-10-30_update-async-para-max.md",
        ROOT / "curriculum" / "2026-10-30_update-async-para-max.docx",
    ),
    (
        ROOT / "curriculum" / "2026-11-03_guia-presentador-paso-a-paso-curso-completo.md",
        ROOT / "curriculum" / "2026-11-03_guia-presentador-paso-a-paso-curso-completo.docx",
    ),
]

# Mapping of canonical repo Markdown <-> Obsidian Vault Markdown
VAULT_MD_PAIRS = [
    (
        ROOT / "curriculum" / "2026-10-30_temario-v2-propuesta.md",
        VAULT_PROJECT_DIR / "01 - Temario v2 Propuesta.md",
    ),
    (
        ROOT / "curriculum" / "2026-11-03_guia-presentador-paso-a-paso-curso-completo.md",
        VAULT_PROJECT_DIR / "02 - Guia del Presentador Paso a Paso (Curso Completo).md",
    ),
    (
        ROOT / "curriculum" / "2026-10-30_update-async-para-max.md",
        VAULT_PROJECT_DIR / "03 - Update y Walkthrough para Max.md",
    ),
    (
        ROOT / "curriculum" / "2026-10-30_syllabus-review-v1.md",
        VAULT_PROJECT_DIR / "04 - Auditoria Temario v1 a v2.md",
    ),
    (
        ROOT / "research" / "2026-10-30_tooling-and-dotnet-azure-verification.md",
        VAULT_PROJECT_DIR / "05 - Verificacion Herramientas .NET 10 y Azure.md",
    ),
    (
        ROOT / "curriculum" / "unidades" / "unidad-1.1-diseno-ui-y-handoff-dotnet.md",
        VAULT_PROJECT_DIR / "Unidades" / "Unidad 1.1 - Diseno UI y Handoff .NET.md",
    ),
    (
        ROOT / "curriculum" / "unidades" / "unidad-1.2-ides-vscode-cursor-windsurf-dotnet.md",
        VAULT_PROJECT_DIR / "Unidades" / "Unidad 1.2 - IDEs VS Code Cursor y Windsurf.md",
    ),
    (
        ROOT / "curriculum" / "unidades" / "unidad-2.2-impacto-estimacion-y-dag-dotnet.md",
        VAULT_PROJECT_DIR / "Unidades" / "Unidad 2.2 - Impacto Estimacion y DAG.md",
    ),
    (
        ROOT / "workshops" / "ws-m1-skills-mcp-dotnet" / "01-GUIA-PASO-A-PASO.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS1 - Guia Paso a Paso (Skills y MCP en CSharp).md",
    ),
    (
        ROOT / "workshops" / "ws-m1-skills-mcp-dotnet" / "02-GUIA-FACILITADOR-Y-RUBRICA.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS1 - Facilitador y Rubrica (Skills y MCP).md",
    ),
    (
        ROOT / "workshops" / "ws-m2-sdd-dotnet" / "01-GUIA-PASO-A-PASO.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS2 - Guia Paso a Paso (SDD Spec Kit y OpenSpec).md",
    ),
    (
        ROOT / "workshops" / "ws-m2-sdd-dotnet" / "02-GUIA-FACILITADOR-Y-RUBRICA.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS2 - Facilitador y Rubrica (SDD).md",
    ),
    (
        ROOT / "workshops" / "ws-m2-harness-oracle-dotnet" / "01-GUIA-PASO-A-PASO.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS3 - Guia Paso a Paso (Harness y Oraculo NetArchTest).md",
    ),
    (
        ROOT / "workshops" / "ws-m2-harness-oracle-dotnet" / "02-GUIA-FACILITADOR-Y-RUBRICA.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS3 - Facilitador y Rubrica (Harness y Oraculo).md",
    ),
    (
        ROOT / "workshops" / "ws-m3-capstone-dotnet" / "01-PLIEGO-CASO-Y-GUIA-EQUIPOS.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS4 - Pliego y Guia de Equipos (Capstone Modulo 3).md",
    ),
    (
        ROOT / "workshops" / "ws-m3-capstone-dotnet" / "02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md",
        VAULT_PROJECT_DIR / "Workshops" / "WS4 - Facilitador y 3 Rubricas Oficiales (Capstone Modulo 3).md",
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_pptx_to_markdown(pptx_path: Path) -> str:
    """Extract all slide text, titles, cards, code blocks, and speaker notes from a PPTX into clean Markdown."""
    prs = Presentation(str(pptx_path))
    lines = [
        f"# Extracted Slides — `{pptx_path.name}`",
        f"- **Total slides:** {len(prs.slides)}",
        "",
    ]
    for idx, slide in enumerate(prs.slides, start=1):
        lines.append(f"## Slide {idx}")
        for shape in slide.shapes:
            if not getattr(shape, "has_text_frame", False):
                continue
            paras = [p.text.strip() for p in shape.text_frame.paragraphs if p.text.strip()]
            if not paras:
                continue
            if len(paras) == 1:
                lines.append(f"- **{paras[0]}**")
            else:
                lines.append(f"### {paras[0]}")
                for p in paras[1:]:
                    lines.append(f"  - {p}")
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
            notes = slide.notes_slide.notes_text_frame.text.strip()
            lines.append(f"\n> **Speaker Notes:** {notes}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def get_all_pptx_files() -> list[Path]:
    out = sorted((ROOT / "curriculum").glob("*.pptx"))
    slides_dir = ROOT / "curriculum" / "slides"
    if slides_dir.exists():
        out.extend(sorted(slides_dir.glob("*.pptx")))
    return out


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"files": {}, "pptx_snapshots": {}}


def save_manifest(manifest: dict):
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_current_state_in_manifest():
    manifest = load_manifest()
    files_meta = manifest.setdefault("files", {})
    pptx_snaps = manifest.setdefault("pptx_snapshots", {})

    tracked_paths = []
    for md_p, docx_p in DOCX_PAIRS:
        tracked_paths.extend([md_p, docx_p])
    for repo_p, vault_p in VAULT_MD_PAIRS:
        tracked_paths.append(repo_p)
        if vault_p.exists():
            tracked_paths.append(vault_p)
    for pptx_p in get_all_pptx_files():
        tracked_paths.append(pptx_p)
        rel_key = str(pptx_p.relative_to(ROOT))
        pptx_snaps[rel_key] = extract_pptx_to_markdown(pptx_p)

    if VAULT_ATTACH_DIR.exists():
        for vp in VAULT_ATTACH_DIR.rglob("*"):
            if vp.is_file() and vp.suffix.lower() in {".docx", ".pptx"}:
                tracked_paths.append(vp)

    for p in tracked_paths:
        if p.exists():
            files_meta[str(p)] = {
                "sha256": sha256_file(p),
                "size": p.stat().st_size,
            }
    save_manifest(manifest)


def cmd_build(args):
    guide_md = ROOT / "curriculum" / "2026-11-03_guia-presentador-paso-a-paso-curso-completo.md"
    if not guide_md.exists() or getattr(args, "reset_guide", False):
        print("==> [1/4] Initializing Presenter Guide (.md + .docx) from template...")
        subprocess.run(["python3", str(ROOT / "scripts" / "build-presenter-guide.py")], check=True)
    else:
        print("==> [1/4] Using canonical Presenter Guide .md (preserving any manual/ingested edits)...")

    print("==> [2/4] Exporting all curriculum .md files to .docx via pandoc...")
    for md_path, docx_path in DOCX_PAIRS:
        subprocess.run(
            ["pandoc", str(md_path), "-f", "gfm", "-t", "docx", "-o", str(docx_path)],
            check=True,
        )
        print(f"    exported {docx_path.relative_to(ROOT)} ({docx_path.stat().st_size} bytes)")

    print("==> [3/4] Generating Executive Deck for Max + All Day-by-Day & Module .pptx Decks...")
    subprocess.run(["python3", str(ROOT / "scripts" / "build-deck-max.py")], check=True)
    subprocess.run(["python3", str(ROOT / "scripts" / "build-all-day-decks.py")], check=True)

    print("==> [4/4] Recording SHA-256 & slide text snapshots in .course-manifest.json...")
    record_current_state_in_manifest()
    print("==> Build complete.")


def build_vault_readme() -> str:
    return """---
type: project
status: active
owner: Fabrizio Hernández & Max Déboli
stack: ".NET 10 + Azure"
ides: "VS Code, Cursor, Windsurf"
repo: "/Users/fabzter/Documents/curso_ai"
remote: "https://github.com/fabzter/curso_ai"
updated: 2026-11-03
---

# Curso: Desarrollo de Software con IA (.NET 10 + Azure)

Proyecto co-creado con **Max Déboli** para consultora de software en Buenos Aires (**52 horas presenciales**, **3 módulos**, **13 unidades**, **70% práctica guiada / 36.25 hs**).

> **Repositorio fuente local:** `/Users/fabzter/Documents/curso_ai` (`https://github.com/fabzter/curso_ai`)  
> **Sincronización bidireccional (On-Command):**
> - Regenerar todo (`.docx` + `.pptx`): `cd ~/Documents/curso_ai && ./scripts/course-sync.sh build`
> - Publicar hacia este Vault: `cd ~/Documents/curso_ai && ./scripts/course-sync.sh publish-vault`
> - Detectar e ingerir ediciones hechas en `.docx`, `.pptx` o en este Vault hacia la documentación fuente: `cd ~/Documents/curso_ai && ./scripts/course-sync.sh ingest --apply`

---

## 1. Documentos Principales del Curso (Notas en este Proyecto)

1. [[01_projects/Curso Desarrollo de Software con IA/01 - Temario v2 Propuesta|01 - Temario v2 Propuesta (52 hs, Rioplatense)]]
2. [[01_projects/Curso Desarrollo de Software con IA/02 - Guia del Presentador Paso a Paso (Curso Completo)|02 - Guía del Presentador y Facilitador Paso a Paso (Día 1 a Día 7)]]
3. [[01_projects/Curso Desarrollo de Software con IA/03 - Update y Walkthrough para Max|03 - Update Ejecutivo y Walkthrough para Max]]
4. [[01_projects/Curso Desarrollo de Software con IA/04 - Auditoria Temario v1 a v2|04 - Auditoría Pedagógica y Técnica (Temario v1 → v2)]]
5. [[01_projects/Curso Desarrollo de Software con IA/05 - Verificacion Herramientas .NET 10 y Azure|05 - Investigación y Verificación de Herramientas (.NET 10 + Azure, Oct 2026)]]

---

## 2. Guías Prácticas por Unidad y Paquetes de Workshop (`.NET 10`)

### Unidades Individuales
- [[01_projects/Curso Desarrollo de Software con IA/Unidades/Unidad 1.1 - Diseno UI y Handoff .NET|Unidad 1.1 — Diseño UI con IA y Handoff a .NET 10]]
- [[01_projects/Curso Desarrollo de Software con IA/Unidades/Unidad 1.2 - IDEs VS Code Cursor y Windsurf|Unidad 1.2 — Herramientas de Desarrollo (VS Code, Cursor y Windsurf)]]
- [[01_projects/Curso Desarrollo de Software con IA/Unidades/Unidad 2.2 - Impacto Estimacion y DAG|Unidad 2.2 — Análisis de Impacto, Estimación y Grafo de Tareas (DAG)]]

###Los 4 Workshops Calificados (100% de la Nota del Curso)
- **Workshop M1 (Unidades 1.3 + 1.5 · 15% Nota):**
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS1 - Guia Paso a Paso (Skills y MCP en CSharp)|WS1 — Guía Paso a Paso: Agent Skill (SKILL.md) + Servidor MCP en C# + Extensions.AI]]
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS1 - Facilitador y Rubrica (Skills y MCP)|WS1 — Guía del Facilitador y Rúbrica (15%)]]
- **Workshop M2-A (Unidades 2.1 + 2.4 · 15% Nota):**
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS2 - Guia Paso a Paso (SDD Spec Kit y OpenSpec)|WS2 — Guía Paso a Paso: SDD con GitHub Spec Kit v1.2.5 y OpenSpec v1.15.0]]
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS2 - Facilitador y Rubrica (SDD)|WS2 — Guía del Facilitador y Rúbrica (15%)]]
- **Workshop M2-B (Unidades 1.4 + 2.3 · Harness + Oráculo):**
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS3 - Guia Paso a Paso (Harness y Oraculo NetArchTest)|WS3 — Guía Paso a Paso: Harness Engineering, NetArchTest y HITL vs. Full AI]]
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS3 - Facilitador y Rubrica (Harness y Oraculo)|WS3 — Guía del Facilitador y Rúbrica]]
- **Workshop M3 Capstone (Unidades 3.1 a 3.4 · 70% Nota):**
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS4 - Pliego y Guia de Equipos (Capstone Modulo 3)|WS4 — Pliego del Caso y Guía de Equipos (GuardiaCloud.CommandCenter)]]
  - [[01_projects/Curso Desarrollo de Software con IA/Workshops/WS4 - Facilitador y 3 Rubricas Oficiales (Capstone Modulo 3)|WS4 — Guía del Facilitador y las 3 Rúbricas Oficiales (25% + 35% + 10% = 70%)]]

---

## 3. Entregables Exportados (`.docx` y Presentaciones `.pptx`) en `99_attachments`

### Documentos Word (`.docx`)
- [[99_attachments/Curso Desarrollo de Software con IA/2026-11-03_guia-presentador-paso-a-paso-curso-completo.docx|Guía del Presentador Paso a Paso — Curso Completo (.docx)]]
- [[99_attachments/Curso Desarrollo de Software con IA/2026-10-30_temario-v2-propuesta.docx|Propuesta de Temario v2 (.docx)]]
- [[99_attachments/Curso Desarrollo de Software con IA/2026-10-30_update-async-para-max.docx|Update y Walkthrough para Max (.docx)]]

### Presentaciones PowerPoint (`.pptx`)
- **Decks Generales y Ejecutivos:**
  - [[99_attachments/Curso Desarrollo de Software con IA/2026-11-03_curso-completo-desarrollo-sw-con-ia.pptx|Master Deck — Curso Completo (29 slides .pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/2026-11-03_deck-temario-v2-para-max.pptx|Deck Ejecutivo de Alineación con Max (13 slides .pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/2026-11-03_dia-1-paso-a-paso.pptx|Deck Día 1 Paso a Paso — Unidades 1.1 y 1.2 (11 slides .pptx)]]
- **Decks Paso a Paso por Día (`slides/dia-*`):**
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-1-unidades-1.1-y-1.2-paso-a-paso.pptx|Día 1 — Unidades 1.1 y 1.2 Paso a Paso (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-2-unidades-1.3-y-1.4-paso-a-paso.pptx|Día 2 — Unidades 1.3 y 1.4 Paso a Paso (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-3-unidades-1.5-y-2.1-paso-a-paso.pptx|Día 3 — Unidades 1.5 y 2.1 Paso a Paso (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-4-unidades-2.2-y-2.3-paso-a-paso.pptx|Día 4 — Unidades 2.2 y 2.3 Paso a Paso (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-5-unidad-2.4-sdd-tools-paso-a-paso.pptx|Día 5 — Unidad 2.4 Herramientas SDD Paso a Paso (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/dia-6-y-7-modulo-3-capstone-paso-a-paso.pptx|Días 6 y 7 — Módulo 3 Proyecto Integrador Capstone Paso a Paso (.pptx)]]
- **Decks por Módulo (`slides/modulo-*`):**
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/modulo-1-fundamentos-herramientas-agentes.pptx|Módulo 1 — Fundamentos, Herramientas y Agentes (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/modulo-2-spec-driven-development.pptx|Módulo 2 — Spec-Driven Development (.pptx)]]
  - [[99_attachments/Curso Desarrollo de Software con IA/slides/modulo-3-capstone-proyecto-integrador.pptx|Módulo 3 — Proyecto Integrador Capstone (.pptx)]]
"""


def cmd_publish_vault(_args):
    if not VAULT_ROOT.exists():
        print(f"ERROR: Vault path not found: {VAULT_ROOT}", file=sys.stderr)
        sys.exit(1)

    print(f"==> Publishing Markdown notes to: {VAULT_PROJECT_DIR}")
    (VAULT_PROJECT_DIR / "Unidades").mkdir(parents=True, exist_ok=True)
    (VAULT_PROJECT_DIR / "Workshops").mkdir(parents=True, exist_ok=True)

    readme_path = VAULT_PROJECT_DIR / "README.md"
    readme_path.write_text(build_vault_readme(), encoding="utf-8")
    print(f"    wrote {readme_path.relative_to(VAULT_ROOT)}")

    for repo_md, vault_md in VAULT_MD_PAIRS:
        vault_md.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo_md, vault_md)
        print(f"    synced {vault_md.relative_to(VAULT_ROOT)}")

    print(f"==> Publishing .docx and .pptx attachments to: {VAULT_ATTACH_DIR}")
    (VAULT_ATTACH_DIR / "slides").mkdir(parents=True, exist_ok=True)

    for _, docx_path in DOCX_PAIRS:
        dst = VAULT_ATTACH_DIR / docx_path.name
        shutil.copy2(docx_path, dst)
        print(f"    copied {dst.relative_to(VAULT_ROOT)}")

    for pptx_path in (ROOT / "curriculum").glob("*.pptx"):
        dst = VAULT_ATTACH_DIR / pptx_path.name
        shutil.copy2(pptx_path, dst)
        print(f"    copied {dst.relative_to(VAULT_ROOT)}")

    for pptx_path in (ROOT / "curriculum" / "slides").glob("*.pptx"):
        dst = VAULT_ATTACH_DIR / "slides" / pptx_path.name
        shutil.copy2(pptx_path, dst)
        print(f"    copied {dst.relative_to(VAULT_ROOT)}")

    record_current_state_in_manifest()
    print("==> Vault publication complete and manifest updated.")


def detect_changes() -> list[dict]:
    manifest = load_manifest()
    files_meta = manifest.get("files", {})
    changes = []

    # 1. Check Vault Markdown notes edited in Obsidian
    for repo_md, vault_md in VAULT_MD_PAIRS:
        if vault_md.exists():
            recorded = files_meta.get(str(vault_md), {}).get("sha256")
            current = sha256_file(vault_md)
            if recorded and current != recorded and current != sha256_file(repo_md):
                changes.append({
                    "kind": "vault_md",
                    "source": vault_md,
                    "target_md": repo_md,
                })

    # 2. Check DOCX files (both in repo and in Vault attachments)
    for repo_md, repo_docx in DOCX_PAIRS:
        candidates = [repo_docx, VAULT_ATTACH_DIR / repo_docx.name]
        for docx_candidate in candidates:
            if not docx_candidate.exists():
                continue
            recorded = files_meta.get(str(docx_candidate), {}).get("sha256")
            current = sha256_file(docx_candidate)
            if recorded and current != recorded:
                changes.append({
                    "kind": "docx",
                    "source": docx_candidate,
                    "target_md": repo_md,
                    "repo_docx": repo_docx,
                })

    # 3. Check PPTX files (both in repo and in Vault attachments)
    for pptx_p in get_all_pptx_files():
        rel_from_curr = pptx_p.relative_to(ROOT / "curriculum")
        vault_pptx = VAULT_ATTACH_DIR / rel_from_curr
        for candidate in [pptx_p, vault_pptx]:
            if not candidate.exists():
                continue
            recorded = files_meta.get(str(candidate), {}).get("sha256")
            current = sha256_file(candidate)
            if recorded and current != recorded:
                changes.append({
                    "kind": "pptx",
                    "source": candidate,
                    "repo_pptx": pptx_p,
                    "rel_key": str(pptx_p.relative_to(ROOT)),
                })

    return changes


def cmd_status(_args):
    changes = detect_changes()
    if not changes:
        print("==> Status: CLEAN. All .md, .docx, .pptx, and Vault files match `.course-manifest.json`.")
        return
    print(f"==> Status: {len(changes)} modified artifact(s) detected:")
    for item in changes:
        print(f"  - [{item['kind'].upper()}] {item['source']} -> affects {item.get('target_md') or item.get('repo_pptx')}")


def cmd_ingest(args):
    INGEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    pptx_snaps = manifest.get("pptx_snapshots", {})
    changes = detect_changes()

    if not changes:
        print("==> No external edits detected in .docx, .pptx, or Vault notes since last sync.")
        return

    report_lines = [
        f"# Ingested Changes Report ({datetime.now(timezone.utc).isoformat()})",
        "",
    ]

    for item in changes:
        kind = item["kind"]
        src: Path = item["source"]

        if kind == "vault_md":
            target_md: Path = item["target_md"]
            old_text = target_md.read_text(encoding="utf-8").splitlines()
            new_text = src.read_text(encoding="utf-8").splitlines()
            diff = "\n".join(difflib.unified_diff(old_text, new_text, fromfile=str(target_md), tofile=str(src), lineterm=""))
            diff_file = INGEST_DIR / f"{target_md.stem}.vault.diff"
            diff_file.write_text(diff + "\n", encoding="utf-8")
            report_lines.append(f"## Vault Markdown Edit: `{src.name}` -> `{target_md.relative_to(ROOT)}`")
            report_lines.append(f"- Diff saved to `{diff_file.relative_to(ROOT)}`")
            if args.apply:
                shutil.copy2(src, target_md)
                report_lines.append(f"- **APPLIED:** Updated `{target_md.relative_to(ROOT)}` from Vault note.")
                print(f"    [APPLIED] Vault edit {src.name} -> {target_md.relative_to(ROOT)}")

        elif kind == "docx":
            target_md: Path = item["target_md"]
            ingested_md = INGEST_DIR / f"{target_md.stem}.from-docx.md"
            subprocess.run(
                ["pandoc", str(src), "-f", "docx", "-t", "gfm", "--wrap=none", "-o", str(ingested_md)],
                check=True,
            )
            old_text = target_md.read_text(encoding="utf-8").splitlines()
            new_text = ingested_md.read_text(encoding="utf-8").splitlines()
            diff = "\n".join(difflib.unified_diff(old_text, new_text, fromfile=str(target_md), tofile=str(ingested_md), lineterm=""))
            diff_file = INGEST_DIR / f"{target_md.stem}.docx.diff"
            diff_file.write_text(diff + "\n", encoding="utf-8")
            report_lines.append(f"## DOCX Edit: `{src}` -> `{target_md.relative_to(ROOT)}`")
            report_lines.append(f"- Converted Markdown: `{ingested_md.relative_to(ROOT)}`")
            report_lines.append(f"- Unified Diff: `{diff_file.relative_to(ROOT)}`")
            if args.apply:
                shutil.copy2(ingested_md, target_md)
                if src != item["repo_docx"]:
                    shutil.copy2(src, item["repo_docx"])
                report_lines.append(f"- **APPLIED:** Retroactively updated `{target_md.relative_to(ROOT)}` from edited `.docx`.")
                print(f"    [APPLIED] DOCX edit {src.name} -> {target_md.relative_to(ROOT)}")

        elif kind == "pptx":
            repo_pptx: Path = item["repo_pptx"]
            rel_key: str = item["rel_key"]
            new_md = extract_pptx_to_markdown(src)
            old_md = pptx_snaps.get(rel_key, "")
            extracted_file = INGEST_DIR / f"{repo_pptx.stem}.slides.md"
            extracted_file.write_text(new_md, encoding="utf-8")
            diff = "\n".join(
                difflib.unified_diff(
                    old_md.splitlines(),
                    new_md.splitlines(),
                    fromfile=f"baseline:{rel_key}",
                    tofile=f"edited:{src.name}",
                    lineterm="",
                )
            )
            diff_file = INGEST_DIR / f"{repo_pptx.stem}.pptx.diff"
            diff_file.write_text(diff + "\n", encoding="utf-8")
            report_lines.append(f"## PPTX Edit: `{src}` (`{rel_key}`)")
            report_lines.append(f"- Extracted Slide Text: `{extracted_file.relative_to(ROOT)}`")
            report_lines.append(f"- Slide Text Diff: `{diff_file.relative_to(ROOT)}`")
            if args.apply and src != repo_pptx:
                shutil.copy2(src, repo_pptx)
                report_lines.append(f"- **APPLIED:** Synced edited `.pptx` back to `{repo_pptx.relative_to(ROOT)}`.")
                print(f"    [APPLIED] PPTX edit {src.name} -> {repo_pptx.relative_to(ROOT)}")

    report_path = INGEST_DIR / "LATEST-INGEST-REPORT.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"==> Ingestion report written to: {report_path.relative_to(ROOT)}")
    if args.apply:
        record_current_state_in_manifest()


def main():
    parser = argparse.ArgumentParser(description="Bidirectional Course Material Pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Regenerate all .docx and .pptx deliverables from canonical sources")
    p_build.add_argument("--reset-guide", action="store_true", help="Reset Presenter Guide .md from build-presenter-guide.py template")
    sub.add_parser("publish-vault", help="Publish course notes & attachments to Obsidian knowledge vault")
    sub.add_parser("status", help="Check for external edits in .docx, .pptx, or Vault notes")
    p_ingest = sub.add_parser("ingest", help="Extract & retroactively apply changes from edited .docx, .pptx, or Vault notes")
    p_ingest.add_argument("--apply", action="store_true", help="Apply ingested changes directly to canonical repo files")

    args = parser.parse_args()
    if args.cmd == "build":
        cmd_build(args)
    elif args.cmd == "publish-vault":
        cmd_publish_vault(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "ingest":
        cmd_ingest(args)


if __name__ == "__main__":
    main()
