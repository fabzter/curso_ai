# AGENTS.md — curso_ai

Entry point for ANY agent (Antigravity, Claude Code, Codex, Hermes/Bean, Devin…) working in this directory.
Read this file fully, then follow **Session start protocol**. Keep it under ~150 lines: details live in `docs/`.

## What this project is

Research + design of an **in-person course with workshops: "Desarrollo de Software con IA"** (draft: 52 h, 3 modules),
for the members of a software consultancy in Buenos Aires (a friend of Max's; NOT Disney staff, NOT Shifta). Co-owned by **Fab** (Fabrizio Hernández, the user) and **Max Déboli**
(Senior Engineering Manager at Mercado Libre, Fab's long-time mentor/friend). It is a **long-horizon project**: many sessions,
many agents. Chat memory does not survive; **files in this repo are the only memory**.

Status snapshot: [`docs/00-STATE.md`](docs/00-STATE.md) (always current). Background: [`docs/01-CONTEXT.md`](docs/01-CONTEXT.md).

## Session start protocol (do this, in order)

1. Read `docs/00-STATE.md` (where we left off, next actions, paste-ready handoff prompt).
2. Read `docs/03-OPEN-QUESTIONS.md` and `docs/02-DECISIONS.md` (don't re-litigate decided things; don't assume answers to open ones).
3. Run `./scripts/check-access.sh` (read-only; ~3 s). If anything fails, see `docs/05-TOOLING.md`. Never declare an access path "broken"
   from a single probe: verify with account/path-specific evidence first.
4. **Check for new input before working**: `./scripts/wa-max-chat.sh | tail -20` (new WhatsApp from Max) and, if a Drive doc is
   being iterated, `gog --readonly -a faboster@gmail.com drive get <fileId> -j` and compare `modifiedTime` against `docs/04-SOURCES.md`.
5. Tell Fab in 3-5 lines what you found + what you propose to do. Then work.

## Session end protocol (mandatory, even if the session is cut short)

1. Update `docs/00-STATE.md` (what changed, next actions, refresh the handoff prompt).
2. Append an entry to `docs/06-SESSION-LOG.md` (date, agent/model, what was done, files touched).
3. Record decisions in `docs/02-DECISIONS.md`; new unknowns in `docs/03-OPEN-QUESTIONS.md`; new sources in `docs/04-SOURCES.md`.
4. `git add -A && git commit` with a descriptive message (local commits only; **never push** without explicit permission).

## HARD RULES (non-negotiable)

- **No outbound actions without explicit per-action permission from Fab:** no WhatsApp/email/Slack sends, no Drive edits/shares/comments,
  no calendar invites. WhatsApp bridge `/api/send` and any MCP `send_message` are **off limits**. `gog` is always run with `--readonly` unless Fab approves a write.
- **Write only inside this directory** (plus `$TMPDIR`). The Obsidian vault (`knowledge`), Drive, `~/src/*`, other repos are **read-only**
  unless Fab explicitly authorizes a specific write. Propose it, don't do it.
- **Luca Edu is dead:** its vault (`knowledge_luca`), accounts and credentials were purged (Sep 2026, possible legal dispute).
  Never read/write/reference/re-authenticate them. Some skill files still mention them: those are stale (see `docs/05-TOOLING.md`).
- **Privacy:** the Max WhatsApp chat before **2026-10-13** is personal and unrelated: do not ingest, quote or summarize it anywhere.
  Never put personal identifiers, finances, employment/legal matters or third parties' phone numbers in this repo.
- **Never fabricate.** Every factual claim about tools/products/versions/prices needs a source + access date (see *Evidence rules*).
  "I couldn't verify" is an acceptable output; an invented tool feature in a course is not.
- Don't modify files you didn't create in this repo without saying so; preserve existing comments/docs unrelated to your change.

## Evidence rules (this course teaches fast-moving tools; stale facts are the #1 risk)

- Tag each research claim: `claim · source URL · accessed YYYY-MM-DD · version/date of the tool · confidence (high/med/low)`.
  Prefer official docs/changelogs > vendor blogs > third-party posts > model memory (model memory = **low**, never cite as fact).
- Transcripts (voice notes) are **evidence, not ground truth**: ASR errs. Keep both model outputs; flag disagreements on names/numbers/dates/decisions.
- LLM-generated content (including Max's draft, which he produced by prompting Claude) is a **hypothesis** until verified.
- Separate in every note: **Fact** (sourced) · **Inference** (yours) · **Open** (unknown). Say which is which.
- When Max/Fab say a source is authoritative (this chat, that doc), use it first; escalate to broader sources only if blocked or asked.

## Where things live

| Path | Purpose |
|---|---|
| `docs/00-STATE.md` | Living status, next actions, handoff prompt. **Update every session.** |
| `docs/01-CONTEXT.md` | Project brief: people, client, constraints, timeline, how the course came to be |
| `docs/02-DECISIONS.md` | Append-only decision log (D-###) |
| `docs/03-OPEN-QUESTIONS.md` | Unknowns that block or shape work (Q-###), with owner |
| `docs/04-SOURCES.md` | Registry of every input (WhatsApp, Drive docs, vault notes) with IDs, dates, how to re-fetch |
| `docs/05-TOOLING.md` | Verified access paths, commands, gotchas, stale-skill warnings |
| `docs/06-SESSION-LOG.md` | Append-only session journal |
| `docs/07-ROADMAP.md` | Phases, research backlog, first-read analysis of the syllabus |
| `sources/` | Raw/ingested inputs, versioned by date. `max-docs/` (Drive docs), `whatsapp/` (curated course-window chat + voice transcripts) |
| `research/` | One note per research topic/unit (evidence-tagged) |
| `curriculum/` | Course design outputs (objectives, unit plans, assessment) |
| `workshops/` | Workshop specs, exercise repos, case studies |
| `scripts/` | Helper scripts (`env.sh` holds all paths/IDs; fix paths there only) |

Naming: dated artifacts `YYYY-MM-DD_short-name.ext`. Course deliverables in **Rioplatense Spanish (voseo)**, since the audience is Argentine (D-016); agent-facing docs in English (technical terms stay in English). Primary exercise stack: **.NET + Azure** (D-014).

## Other agents' skills on this machine (read the SKILL.md before using the tool)

Skills are NOT auto-loaded in every agent. Locations: `~/.agents/skills/`, `~/.hermes/skills/` (Hermes/"Bean", the most up to date), `~/.claude/skills/`, `~/.codex/skills/`.
Relevant: `~/.hermes/skills/mcp/whatsapp-mcp-local-bridge` (WhatsApp, contact/LID resolution, pitfalls), `~/.hermes/skills/whatsapp-chat-export`,
`~/.hermes/skills/note-taking/obsidian-cli` + `personal-vault-para` (vault), `~/.hermes/skills/productivity/gog`, `~/.agents/skills/gog-api-token` (raw Google REST),
`~/.hermes/skills/research/grounded-citations`, `~/.hermes/skills/research-methodology`, `~/.agents/skills/firecrawl*` (web research), `~/.hermes/skills/media/local-audio-enhance-transcribe` (whisper fallback).
Full map and stale-skill warnings: `docs/05-TOOLING.md`.

## Working with Fab

- Concise, direct, bluntness welcome, **no walls of text, no apology loops** — after a mistake: diagnose, fix, move on. If Fab steps away, wait.
- Talk to Fab in English (technical) or **Mexican Spanish — never voseo / Argentinian Spanish**. The ONLY place voseo is correct is the course material itself (D-016); never in chat with Fab or in agent-facing docs.
- Prefers explicit SPEC/PLAN/TODO/CONTEXT files over relying on memory; compact paste-ready handoff prompts.
- Prefers small helper scripts over long raw command lines. No cron/background workarounds unless he asks to schedule.
- Uncertain state claims ("X is broken", "Y doesn't exist") must be verified with concrete evidence before stating them.
- Default Google account for everything here: `faboster@gmail.com`.
