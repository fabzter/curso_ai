# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 16:54 CST · Antigravity (Gemini 4 Argon) · Phase: **P1, P2 & First Full Workshop (`ws-m2-sdd-dotnet`) Done → Ready for Next Workshop or Sync with Max**

## One-line status
Completed the **P1 Syllabus Audit** (`curriculum/2026-10-30_syllabus-review-v1.md`), the **Proposed Temario v2 in Rioplatense Spanish** (`curriculum/2026-10-30_temario-v2-propuesta.md`), and the **First Complete Workshop Package (`workshops/ws-m2-sdd-dotnet/`)** covering **Units 2.1 + 2.4 (SDD on .NET 10 with EARS, GitHub Spec Kit `v1.2.5`, and OpenSpec `v1.15.0`)**, including compilable & tested `starter/` (2 green tests) and `solution/` (4 green integration test suites) in C#/.NET 10.

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, 13 units, in person. **Audience: members of a Buenos Aires software consultancy** (a friend of Max's; name unknown; not Shifta; not Disney staff).
- **Deliverables completed so far (ready to show Max or continue expanding):**
  1. `research/2026-10-30_tooling-and-dotnet-azure-verification.md` — Primary-source verification of all tools/SDKs + .NET/Azure equivalents (`ModelContextProtocol` NuGet `v2.3.0`, `Microsoft.Extensions.AI` `v10.11.0`, `Microsoft.Agents.AI` `v1.27.0`, `github/spec-kit` `v1.2.5`, `Fission-AI/OpenSpec` `v1.15.0`, etc.).
  2. `curriculum/2026-10-30_syllabus-review-v1.md` — Unit-by-unit audit of Max's Temario v1 (rebalancing practice from 36% to 62.5%–70%, adding learning objectives, .NET/Azure spine, and brownfield seed repo strategy).
  3. `curriculum/2026-10-30_temario-v2-propuesta.md` — Complete 52 h proposed v2 syllabus in **Rioplatense Spanish (voseo)**.
  4. `workshops/ws-m2-sdd-dotnet/` — Complete 3h45m Workshop Package (`D-015`, `D-017`) for **Units 2.1 + 2.4 (Spec-Driven Development on .NET)**:
     - `00-WORKSHOP-SPEC.md` (objectives, agenda, prerequisites, structure)
     - `01-GUIA-PASO-A-PASO.md` (student step-by-step hands-on guide in Rioplatense Spanish)
     - `02-GUIA-FACILITADOR-Y-RUBRICA.md` (facilitator runbook, role-play answer sheet for the 7 hidden ambiguities, troubleshooting, 100-pt rubric = 15% course grade)
     - `starter/` (`.NET 10` Minimal APIs solution `GuardiaCloud.Sla.sln`, `AGENTS.md`/`CLAUDE.md`, `brief-cliente-ambiguo.md`, baseline `openspec/specs/sla-tracking/spec.md`, 2 passing integration tests + 1 intentional bug in `SlaCalculator` for `/speckit-bug-assess`)
     - `solution/` (`.NET 10` reference solution with `.specify/memory/constitution.md`, `.specify/bugs/resolved-sla-breach-drift/report.md`, `specs/001-sla-pause-windows/{spec,plan,tasks}.md`, `openspec/changes/archive/2026-10-30-cap-p1-pause-budget/*`, merged `openspec/specs/sla-tracking/spec.md`, and 4 passing `WebApplicationFactory` + `FakeTimeProvider` test suites).

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search · `.NET SDK 10.0.402`.

## NEXT ACTIONS (ordered)
1. Re-check for news from Max at session start (`./scripts/wa-max-chat.sh | tail -20`; S-03 `modifiedTime`).
2. **Ask Fab whether to:**
   - **(a)** Build the **Module 1 Graded Deliverable Workshop (`ws-m1-skills-mcp-dotnet`, Units 1.3 + 1.5)**: Team Skill (`SKILL.md`) + Official C# MCP Server (`ModelContextProtocol` NuGet `v2.3.0`) + `Microsoft.Extensions.AI` mini-agent exposing `GuardiaCloud.Sla` tools; OR
   - **(b)** Build the **Units 1.4 + 2.3 Harness & Verification Oracle Workshop** (`AGENTS.md` + `.NET` CLI hooks + `NetArchTest` + Full AI vs. HITL in parallel `git worktrees`); OR
   - **(c)** Prepare a **compact executive summary / presentation artifact** of *Temario v2 + Workshop M2* for the upcoming call with Max.

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
Completed so far:
- P1 Audit & Proposed Temario v2 (.NET + Azure, Rioplatense): curriculum/2026-10-30_syllabus-review-v1.md & curriculum/2026-10-30_temario-v2-propuesta.md
- First Full Workshop Package (Units 2.1 + 2.4, SDD on .NET 10 with Spec Kit v1.2.5 & OpenSpec v1.15.0): workshops/ws-m2-sdd-dotnet/ (starter/ and solution/ both compile and pass dotnet test).
Follow the session start/end protocols in AGENTS.md. Tell Fab in 3-5 lines what's new and ask whether to build the Module 1 Workshop next (Units 1.3+1.5: SKILL.md + C# MCP Server in .NET 10) or prepare the sync package for Max.
```
