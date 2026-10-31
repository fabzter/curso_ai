# 04 — Source registry

Every input used by this project. Re-fetch commands assume repo root. Update when a source changes or a new one arrives.

## Authoritative (named by Fab)
| ID | Source | Identifier | Version captured | Local copy | Re-fetch |
|---|---|---|---|---|---|
| S-01 | WhatsApp chat Fab ↔ Max Déboli (course window only, from 2026-10-13) | chat_jid `52399205003325@lid` (ingest only ≥ 2026-10-13) | through 2026-10-30 16:34 (last msg: Fab "Dale te paso update y explicación de lo que hice para que pueda ser async este fin") | `sources/whatsapp/max-chat_2026-10-13_to_2026-10-28.md` | `./scripts/wa-max-chat.sh` |
| S-02 | Voice notes in S-01 (5 clips: 2 Fab 10-13, Max 10-28 14:42, Fab 10-28 ×2) | message ids in S-01 note | transcribed 2026-10-30, Nemotron + Parakeet | `sources/whatsapp/voice/*.txt` | `./scripts/wa-transcribe.sh <message_id>` |
| S-03 | **"Temario Desarrollo de Software con IA.docx"** (Max's draft syllabus) | Drive fileId `1USyhkrKDHFNJihN0eT-FjCRHyZDgHXUh` (owner Max; opened by Fab via link sent 2026-10-28) | Drive `modifiedTime` **2026-10-28T22:17:19Z**, 10 779 bytes | `sources/max-docs/2026-10-28_temario-desarrollo-sw-con-ia.{docx,md}` | `./scripts/drive-fetch.sh 1USyhkrKDHFNJihN0eT-FjCRHyZDgHXUh temario-desarrollo-sw-con-ia` (new dated file if modified) |

The docx is a real Word file stored in Drive (mimeType `…wordprocessingml.document`), opened via `docs.google.com/document/d/<id>/edit`. `gog docs` is for native Google Docs; use `gog drive download` (done by the script).
Max said it's "solo un draft" and that he made it by prompting Claude → treat as hypothesis (AGENTS.md, Evidence rules).

## Seen but NOT ingested (and why)
| Item | Why not |
|---|---|
| WhatsApp 2026-07-11 → 2026-10-12 with Max (incl. voice notes, a .md and a .pptx he got from Fab on 09-17) | Personal/unrelated (a different topic); outside the course window. Not copied. |
| Original proposal/slides sent to the client (Fab asked Max for the slide text on 10-15) | Never received in the chat. **Needed** (Q-003). |
| Fab's Sept-15 Google Doc link in the chat | Unrelated to this course. |
| LIDR free workshop `lidr.co/workshop-arquitectura-multiagente-ia` (Fab attended/was going to record+summarize) | Not yet fetched; candidate benchmark in the research backlog (`07-ROADMAP.md`). Ask Fab whether his recording/summary exists. |

## Vault notes consulted (read-only; `knowledge/`)
- `05_people/Max Déboli.md` — background only; contains unrelated sensitive context, do not copy.
- `01_projects/Shifta Partnership/Shifta (empresa).md`, `…/Shifta Partnership.md`; `01_projects/Agentic SDLC Proposal/Ideas.md` — context on Fab's method + Shifta; relation to this course unconfirmed.

## ASR variants note
Fab's/Max's voice notes were reconciled by hand in the S-01 note. Where models disagreed, the S-01 note says so.

## Cross-referenced local & primary web sources (added 2026-10-30 during P1)
| ID | Source | Identifier / Location | Notes |
|---|---|---|---|
| S-04 | Fab's verified empirical research corpus | `~/Documents/agentic_sdlc_implementation_consulting/docs/01-investigacion.md` (read-only) | Used only for verified public study citations (METR Jul 2025, DORA 2025, Larbi et al. 2025, SWE-EVO 2026, ETH Zurich `AGENTS.md` paper Feb 2026, AgenticFlict 2026, Böckeler/Fowler SDD taxonomy Oct 2025) per `D-011`. |
| S-05 | Primary GitHub & NuGet metadata for syllabus tools (2026-10-30) | Recorded in `research/2026-10-30_tooling-and-dotnet-azure-verification.md` | `modelcontextprotocol/csharp-sdk` (`v2.3.0`), `microsoft/agent-framework` (`Microsoft.Agents.AI` `v1.27.0`), `Microsoft.Extensions.AI` (`v10.11.0`), `github/spec-kit` (`v1.2.5`), `Fission-AI/OpenSpec` (`v1.15.0`), `bmad-code-org/BMAD-METHOD` (`v6.12.4`), `anthropics/claude-code` (`v2.1.314`), `openai/codex` (`rust-v0.166.0`). |
