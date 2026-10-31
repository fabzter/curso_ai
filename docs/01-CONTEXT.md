# 01 — Context

> Facts below are tagged by source (see `04-SOURCES.md`). Anything not sourced is marked **(inference)** or **(unknown)**.

## The project in one paragraph
Fab and Max are designing an in-person course (with workshops) on AI-assisted software development. **Audience (Fab, 2026-10-30, D-010):
the members of a software consultancy in Buenos Aires, a friend of Max's; NOT Disney employees; consultancy name unknown, definitely not Shifta.**
On 2026-10-13 Max told Fab he was exploring, with a third person he calls "el 5" (**unidentified**), giving an "AI for development"
course "en unos equipos de Disney" (exact Disney link unknown; inference: the consultancy's staff work on Disney engagements; not needed now),
and invited Fab to build it with him. Fab said yes. On 2026-10-28 Max reported that **"they liked what we sent and will give the go"**
(what was sent: unknown, **Fab sent nothing**); start date undefined. Max then shared a **draft syllabus/calendar** (docx, Drive, made by prompting Claude).
**Current plan (D-009):** the Friday 10-30 session with Max has NOT happened; Fab will first expand Max's draft and develop part of the program
and an actual workshop on his own, then return to Max.

## People
| Who | Role here | Notes |
|---|---|---|
| **Fab** (Fabrizio Hernández) | Co-author, user | Software architect/EM, CDMX. Account `faboster@gmail.com`. Has a separate method/IP project (see below). |
| **Max Déboli** | Co-author, brings the client channel | Sr Software Eng. Manager @ Mercado Libre (Argentine, based in CDMX), ex-Lagash Chief Architect/Delivery Manager. Writes in Rioplatense Spanish. Vault note: `knowledge/05_people/Max Déboli.md` (read-only; contains unrelated sensitive context: do not copy). |
| **"El 5"** | Unknown third party in Max's side conversation | **(unknown)**. Not blocking. |
| **Audience / client** | Members of a Buenos Aires software consultancy (friend of Max's) | Headcount/seniority/stacks **(unknown)**, Q-002. Not Disney employees. |
| **Consultancy firm** | Friend's firm in Buenos Aires | Name **unknown**; **definitely not Shifta** (Fab, 2026-10-30). Q-001, not blocking. |

## Timeline (course window of the Max chat; times CDMX, UTC-6)
| Date | Event | Source |
|---|---|---|
| 2026-10-13 13:27 | Max proposes the Disney-Argentina AI course; asks if Fab wants to do it together | WA text |
| 2026-10-13 17:43 | Fab (voice): "yes, I'm in" and asks to be told if they meet to review it | WA voice |
| 2026-10-13 18:47 | Call fixed for **Thu 2026-10-15 17:00** (Max may add "el 5") | WA text |
| 2026-10-15 16:29–19:25 | Fab joins late; afterwards asks for the **text of the slides**; Max will try to give access to "the file" | WA text |
| 2026-10-19 | Fab shares a free LIDR workshop on multi-agent architecture; he signed up to watch how it's taught and what questions people ask; will record/transcribe/summarize it | WA text |
| 2026-10-20 21:15Z | The syllabus docx is created in Drive (header: "Oct 20, 2026 · @Max") | Drive metadata |
| 2026-10-28 14:42 | Max (voice): client liked what was sent, **"nos van a dar go"**, no start date yet (to be defined "in the following days"); wants to advance the material; proposes a meeting **this Friday** to shape it by prompting | WA voice |
| 2026-10-28 15:55 | Max: he is NOT working on the link Fab had; he's on a **new file/doc made by prompting Claude** | WA text |
| 2026-10-28 16:17 | Max sends the doc: "solo un draft, pero sobre eso podemos ir trabajando. El viernes nos organizamos" | WA text + Drive |
| 2026-10-30 | Fab: the Friday session has **not** happened; he will develop first and go back to Max after (D-009) | Fab, chat with agent |
| 2026-10-30 16:21–16:34 | Fab texts Max that he is advancing the material and will send an update; Max replies he has things to attend to today and will work on it over the weekend; Fab confirms he'll send an **async update + explanation** for the weekend | WA text (`S-01`) |

## The draft syllabus (Max, v1, Drive modified 2026-10-28T22:17Z)
Full text: `sources/max-docs/2026-10-28_temario-desarrollo-sw-con-ia.md`. Title: *Temario: Desarrollo de Software con IA*.
52 h, ~30-40% theory / 60-70% guided practice, everything chains into a final project. Audience: developers, tech leads, architects
(Git, one backend/frontend language, agile teamwork). Teams of 3-5 in Module 3.

| Module | Unit (hours) |
|---|---|
| **1. Herramientas de IA (20 h)** | 1.1 Diseño (4) · 1.2 Herramientas de desarrollo (4) · 1.3 Agentes y Skills (4) · 1.4 Harness Engineering — Claude Code / Devin / Codex (6) · 1.5 MCPs (2) |
| **2. Metodologías adaptadas a la IA (18 h)** | 2.1 Spec (4) · 2.2 Estimación, impacto y planning (4) · 2.3 Implementation: Full AI vs Human-in-the-loop (4) · 2.4 Herramientas para SDD — Spec Kit, Kiro, BMAD, OpenSpec, Tessl (6) |
| **3. Ejecución de proyecto (14 h)** | 3.1 Presentación y entendimiento funcional (2) · 3.2 Specs (4) · 3.3 Planificación (2) · 3.4 Implementación (6) |

Assessment: skill + MCP server 15% · spec & plan of a feature 15% · project specs & plan 25% · working project + demo 35% · retrospective with metrics 10%.
Prerequisites: GitHub account, IDE, access to ≥1 harness (Claude Code or Codex); Devin and Kiro by demo if no licenses.
Arithmetic check (2026-10-30): every unit's blocks sum to the stated hours; modules 20+18+14 = 52; weights = 100%.

## Related assets (read-only unless authorized)
- `~/Documents/agentic_sdlc_implementation_consulting` — Fab's separate **method/IP** project (maturity model N0-N4, diagnostic).
  Not needed for this course (D-011). If you reuse its *research*, cite it as a source; its method is trade-secret-sensitive, so don't paste the method itself without asking Fab.
- `knowledge/01_projects/Agentic SDLC Proposal/Ideas.md` and `knowledge/01_projects/Shifta Partnership/` — vault notes on that method.
  Shifta is **NOT** involved in this course (Fab, 2026-10-30). The method repo is not needed here; its research may be used as an input (D-011).

## What we do NOT know yet
See `03-OPEN-QUESTIONS.md`. Relevant now: what "the workshop" is (Q-008), audience details (Q-002), Spanish register (Q-011). Deferred: consultancy name, schedule, licenses, commercial terms.
