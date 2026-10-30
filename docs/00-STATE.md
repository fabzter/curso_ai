# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 16:42 CST · Antigravity (Gemini 4 Argon) · Phase: **P1 & P2 Initial Pass Done → Ready for Q-013 (Pick First Workshop for P3)**

## One-line status
Completed the **P1 Syllabus Audit** (`curriculum/2026-10-30_syllabus-review-v1.md`), the **P2 Tooling & .NET/Azure Verification** (`research/2026-10-30_tooling-and-dotnet-azure-verification.md`), and the complete **Proposed Temario v2 in Rioplatense Spanish** (`curriculum/2026-10-30_temario-v2-propuesta.md`). Ready for Fab to review Temario v2 and pick the first workshop (`Q-013`) to build in full (`D-015`).

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, 13 units, in person. **Audience: members of a Buenos Aires software consultancy** (a friend of Max's; name unknown; not Shifta; not Disney staff).
- Max's Temario v1 (`sources/max-docs/2026-10-28_temario-desarrollo-sw-con-ia.md`) was audited and preserved intact; our proposed **Temario v2** lives in `curriculum/2026-10-30_temario-v2-propuesta.md`.
- **Key improvements in Temario v2:**
  1. **.NET + Azure spine across all 13 units (`D-014`):** Visual Studio 2022/2026 + JetBrains Rider alongside VS Code/Cursor; `Microsoft.Extensions.AI` (`v10.11.0`) + Microsoft Agent Framework (`Microsoft.Agents.AI` `v1.27.0` + Azure AI Foundry) in Unit 1.3; Official C# MCP SDK (`ModelContextProtocol` NuGet `v2.3.0`) + Azure MCP Server (`microsoft/mcp`) in Unit 1.5; xUnit + `WebApplicationFactory` + `Testcontainers` + `NetArchTest` as the deterministic verification oracle in Modules 2 & 3.
  2. **Practice ratio fixed:** Raised from ~36% explicit practice in v1 (Modules 1–2) to **62.5% real Workshop time in Modules 1–2** and **69.7% (36.25 h / 52 h) overall**.
  3. **Brownfield .NET + Azure Seed Repo ("Hilo Conductor"):** Used from Unit 1.2 through Module 3 so teams don't waste their 6-hour Module 3 implementation window on project scaffolding.
  4. **Updated SDD tooling (Oct 2026):** GitHub Spec Kit `v1.2.5` (`/speckit-constitution` $\rightarrow$ `/speckit-converge` + `bug` extension) for greenfield/feature flows and OpenSpec `v1.15.0` (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`) for brownfield deltas.

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search.

## Gotchas discovered (don't relearn)
- Two "Max Deboli" contacts exist; the right chat is `52399205003325@lid`.
- `~/.agents/skills/obsidian-cli` is stale (points to purged Luca vault). Use the Hermes skill.
- The Drive "doc" is a .docx → `drive download` + pandoc, not `gog docs cat`.
- ASR: run both models; Nemotron garbles starts of short clips, Parakeet hallucinates English on Max's long clip.
- Cross-harness `AGENTS.md`: Claude Code does not read `AGENTS.md` natively (issue `#34235`); always pair `AGENTS.md` with a 1-line `CLAUDE.md` containing `@AGENTS.md`.

## NEXT ACTIONS (ordered)
1. **Get Fab's feedback on `curriculum/2026-10-30_temario-v2-propuesta.md` and answer `Q-013`** (which 2–4 h workshop to build first per `D-015`):
   - *Option A (Recommended):* **Units 1.3 + 1.5 Combined Deliverable Workshop** — *Construcción de una Skill de equipo (`SKILL.md`) y un Servidor MCP en C# (`ModelContextProtocol` v2.3.0)* (+ mini-agent with `Microsoft.Extensions.AI`). Covers the 15% Module 1 graded deliverable and showcases the .NET/Azure upgrade for Max.
   - *Option B:* **Units 2.1 + 2.4 SDD Workshop** — *De requerimiento ambiguo a código .NET verificado con GitHub Spec Kit (`v1.2.5`) y OpenSpec (`v1.15.0`)*.
   - *Option C:* **Units 1.4 + 2.3 Harness & Verification Oracle Workshop** — *Harness Engineering (`AGENTS.md` + hooks `.NET`) y Full AI vs. HITL con xUnit, Testcontainers y NetArchTest*.
2. **Build the chosen Workshop package (`P3`)** under `workshops/<unit-slug>/`:
   - `00-WORKSHOP-SPEC.md` (objectives, agenda, prerequisites)
   - `01-STEP-BY-STEP-GUIDE.md` (student instructions in Rioplatense Spanish)
   - `02-FACILITATOR-GUIDE.md` (timing, common failure modes, live prompts, rubric)
   - `starter/` (compilable .NET 9/10 C# starter project with tests)
   - `solution/` (verified working reference solution)
3. Re-check for news from Max before each session (`./scripts/wa-max-chat.sh | tail -20`; S-03 `modifiedTime`).

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
P1 (Syllabus Review + Proposed Temario v2 in Rioplatense for .NET/Azure) is complete in:
- research/2026-10-30_tooling-and-dotnet-azure-verification.md
- curriculum/2026-10-30_syllabus-review-v1.md
- curriculum/2026-10-30_temario-v2-propuesta.md
Follow the session start/end protocols in AGENTS.md. Ask Fab which workshop (Q-013) to build first (or proceed if already chosen) and build the full D-015 workshop package under workshops/.
```
