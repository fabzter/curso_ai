# 01 — Context

> Facts below are tagged by source (see `04-SOURCES.md`). Anything not sourced is marked **(inference)** or **(unknown)**.

## The project in one paragraph
Fab and Max are designing an in-person course (with workshops) on AI-assisted software development for a software consultancy
and its client's dev teams. On 2026-10-13 Max told Fab he was exploring, with a third person he calls "el 5" (**unidentified**),
giving an "AI for development" course to **Disney teams in Argentina**, and invited Fab to build it with him
(his reasoning: Fab had just left his job and might have time). Fab said yes. After an initial proposal was sent to the client,
Max reported on 2026-10-28 that **the client liked it and will give the go**; start date is still undefined. Max then shared a
**new draft syllabus** (docx, Drive, produced by prompting Claude) as the base for joint work. They planned a working session for **Friday 2026-10-30**.

## People
| Who | Role here | Notes |
|---|---|---|
| **Fab** (Fabrizio Hernández) | Co-author, user | Software architect/EM, CDMX. Account `faboster@gmail.com`. Has a separate method/IP project (see below). |
| **Max Déboli** | Co-author, brings the client channel | Sr Software Eng. Manager @ Mercado Libre (Argentine, based in CDMX), ex-Lagash Chief Architect/Delivery Manager. Writes in Rioplatense Spanish. Vault note: `knowledge/05_people/Max Déboli.md` (read-only; contains unrelated sensitive context: do not copy). |
| **"El 5"** | Unknown third party Max is working the Disney opportunity with | **(unknown)** — ask. Possibly at the consultancy. |
| **Client** | Disney teams, Argentina | Per Max, WhatsApp 2026-10-13. Team count/size/stack/seniority **(unknown)**. |
| **Consultancy firm** | The "software consultancy firm" Fab mentioned | **(unknown which one)**. Do not assume Shifta or Lagash without confirmation (see Q-001). |

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
| **2026-10-30 (today)** | Friday working session with Max — **status unknown** (Q-005) | — |

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
- `~/Documents/agentic_sdlc_implementation_consulting` — Fab's separate **method/IP** project (maturity model N0-N4, diagnostic, "Shifta Partnership").
  **IP boundary unresolved** (Q-007): do NOT import its content into course material without Fab's explicit decision; the method relies on trade-secret protection (NDA before sharing).
- `knowledge/01_projects/Agentic SDLC Proposal/Ideas.md` and `knowledge/01_projects/Shifta Partnership/` — vault notes on that method. Shifta is a Buenos Aires software house (Disney is in its public portfolio) —
  **a possible but UNCONFIRMED link to this course.**

## What we do NOT know yet
See `03-OPEN-QUESTIONS.md`. Biggest: who the consultancy is, commercial/IP terms, client constraints (tools allowed, licenses), schedule/format, what exactly was sent to the client.
