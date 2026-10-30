# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 16:35 CST · Antigravity (Claude Sonnet 5.5) · Phase: **P0 done → P1 Syllabus review (next, not started)**

## One-line status
Access to all tools verified, Max's chat + latest Drive doc (Temario v1, 2026-10-28) + voice notes ingested, long-horizon scaffolding in place. **No course content has been created yet** and **no outbound action has been taken** (nothing sent, nothing written to Drive/vault).

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, in person. **Audience: members of a Buenos Aires software consultancy** (a friend of Max's; name unknown; not Shifta; not Disney staff).
- Max's Temario v1 (docx, made by prompting Claude, a draft calendar) is the baseline. Fab sent nothing to anyone.
- **Plan (D-009, D-013):** the Friday session with Max has NOT happened. Fab develops first, alone: review/improve the whole syllabus, then build one workshop; then go back to Max.
- **Design decisions so far:** workshop = 2-4 h hands-on session inside a unit with full package (D-015) · stack .NET + Azure (D-014) · material in Rioplatense voseo (D-016) · client constraints/licenses out of scope for now (D-011).

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search.
Not available in this agent: WhatsApp MCP tools (SQL+REST used instead).

## Gotchas discovered (don't relearn)
- Two "Max Deboli" contacts exist; the right chat is `52399205003325@lid`.
- `~/.agents/skills/obsidian-cli` is stale (points to purged Luca vault). Use the Hermes skill.
- The Drive "doc" is a .docx → `drive download` + pandoc, not `gog docs cat`.
- ASR: run both models; Nemotron garbles starts of short clips, Parakeet hallucinates English on Max's long clip.

## NEXT ACTIONS (ordered)
1. **P1 syllabus review.** Create `curriculum/2026-10-30_syllabus-review-v1.md` with one section per unit (13 units): for each, (a) **verified/outdated/unverified** table of every tool/product claim with source+date (`research/` notes hold the evidence), (b) learning objectives (missing in v1), (c) practice vs theory ratio actually measured, (d) .NET/Azure adaptation, (e) gaps/risks. Start with Module 2 and Module 3 (stable concepts); do 1.1, 1.2, 1.4, 2.4 (perishable tool facts) last.
2. Produce a **proposed Temario v2** (`curriculum/`), diffed against v1, in Rioplatense. Do not edit Max's original (`sources/max-docs/`).
3. With the review in hand, ask Fab **Q-013** (which workshop first), then build it per D-015 in `workshops/<unit>/`.
4. Re-check for news from Max before each session (`./scripts/wa-max-chat.sh | tail -20`; S-03 `modifiedTime`).
5. Open: Q-002 (is the consultancy a .NET/Azure shop?), Q-001 (name). Not blocking.

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
Follow the session start/end protocols in AGENTS.md exactly. Hard rules: nothing outbound (WhatsApp/email/Drive writes) without Fab's explicit OK; write only inside this dir; Luca vault/creds are dead; verify every tool claim with dated sources.
Then tell Fab in 3-5 lines what's new and continue with NEXT ACTIONS (P1 syllabus review). Decisions D-009..D-016 are settled: don't re-ask.
```
