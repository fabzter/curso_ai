# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 16:20 CST · Antigravity (Claude Sonnet 5.5) · Phase: **P0 done → P1 Align (next)**

## One-line status
Access to all tools verified, Max's chat + latest Drive doc (Temario v1, 2026-10-28) + voice notes ingested, long-horizon scaffolding in place. **No course content has been created yet** and **no outbound action has been taken** (nothing sent, nothing written to Drive/vault).

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, in person, for Disney teams in Argentina (per Max), via a consultancy that is **not yet identified**.
- Client reacted positively; Max announced the "go" on 10-28; **no start date**.
- Max's Temario v1 (docx, made by prompting Claude, "solo un draft") is the working baseline.
- Friday 2026-10-30: working session Fab+Max planned. **We don't know if/what happened (Q-005).**

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search.
Not available in this agent: WhatsApp MCP tools (SQL+REST used instead).

## Gotchas discovered (don't relearn)
- Two "Max Deboli" contacts exist; the right chat is `52399205003325@lid`.
- `~/.agents/skills/obsidian-cli` is stale (points to purged Luca vault). Use the Hermes skill.
- The Drive "doc" is a .docx → `drive download` + pandoc, not `gog docs cat`.
- ASR: run both models; Nemotron garbles starts of short clips, Parakeet hallucinates English on Max's long clip.

## NEXT ACTIONS (ordered)
1. **Ask Fab Q-005, then Q-001/Q-003/Q-004/Q-006** (the blocking ones; batch them). Record answers in `03-OPEN-QUESTIONS.md` / `02-DECISIONS.md`.
2. Re-check for news: `./scripts/wa-max-chat.sh | tail -20`; check whether S-03 changed (`drive get` → `modifiedTime` ≠ `2026-10-28T22:17:19Z` → run `drive-fetch.sh`, then diff the new `.md` against the old).
3. If Fab provides new voice notes/docs, ingest per `04-SOURCES.md` and update the S-01 note.
4. Start **P2 Research** with the highest-perishability units first? **No:** verify last. Begin with Module 2 (SDD/spec, stable concepts) + the Module 3 case design; leave 1.4 and 2.4 tool facts for the end. (Proposal; confirm with Fab.)
5. Offer Fab (needs OK): vault project note (Q-009).

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
Follow the session start/end protocols in AGENTS.md exactly. Hard rules: nothing outbound (WhatsApp/email/Drive writes) without Fab's explicit OK; write only inside this dir; Luca vault/creds are dead; verify every tool claim with dated sources.
Then tell Fab in 3-5 lines what's new and which of the open questions (Q-005, Q-001, Q-003, Q-004, Q-006) you need answered first.
```
