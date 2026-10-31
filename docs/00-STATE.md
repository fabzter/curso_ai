# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 18:36 CST · Antigravity (Gemini 4 Argon) · Phase: **P1, P2 & Three Complete `.NET 10` Workshops Done (`ws-m2-sdd-dotnet`, `ws-m1-skills-mcp-dotnet`, `ws-m2-harness-oracle-dotnet`) → Ready for Max Async Pack (Option C) or Module 3 Capstone**

## One-line status
Completed the **P1 Syllabus Audit** (`curriculum/2026-10-30_syllabus-review-v1.md`), the **Proposed Temario v2 in Rioplatense Spanish** (`curriculum/2026-10-30_temario-v2-propuesta.md`), and **three complete `.NET 10` Workshop Packages** covering Modules 1 and 2 (`ws-m2-sdd-dotnet`, `ws-m1-skills-mcp-dotnet`, `ws-m2-harness-oracle-dotnet`), all with compilable & tested `starter/` and `solution/` projects. Also ingested the 2026-10-30 16:21–16:34 WhatsApp messages where Fab and Max agreed to handle the review via an **async weekend update**.

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, 13 units, in person. **Audience: members of a Buenos Aires software consultancy** (a friend of Max's; name unknown; not Shifta; not Disney staff).
- **WhatsApp update (2026-10-30 16:21–16:34, `S-01`):** Max said he'll work on the course over the weekend; Fab told him: *"Dale te paso update y explicación de lo que hice para que pueda ser async este fin"*.
- **Deliverables completed so far (all committed locally):**
  1. `research/2026-10-30_tooling-and-dotnet-azure-verification.md` — Primary-source verification of all tools/SDKs + .NET/Azure equivalents (`ModelContextProtocol` NuGet `v2.3.0`, `Microsoft.Extensions.AI` `v10.11.0`, `Microsoft.Agents.AI` `v1.27.0`, `NetArchTest.Rules` `v1.3.2`, `github/spec-kit` `v1.2.5`, `Fission-AI/OpenSpec` `v1.15.0`, etc.).
  2. `curriculum/2026-10-30_syllabus-review-v1.md` — Unit-by-unit audit of Max's Temario v1 (rebalancing practice from 36% to 62.5%–70%, adding learning objectives, .NET/Azure spine, and brownfield seed repo strategy).
  3. `curriculum/2026-10-30_temario-v2-propuesta.md` — Complete 52 h proposed v2 syllabus in **Rioplatense Spanish (voseo)**.
  4. `workshops/ws-m2-sdd-dotnet/` — **Units 2.1 + 2.4 (Spec-Driven Development on .NET, Module 2 Graded Deliverable = 15% grade)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (`.NET 10` Minimal APIs solution `GuardiaCloud.Sla.sln`, 2 passing tests + 1 intentional bug in `SlaCalculator`)
     - `solution/` (`.NET 10` reference solution with Spec Kit `v1.2.5` + OpenSpec `v1.15.0` artifacts and 4 passing `WebApplicationFactory` test suites).
  5. `workshops/ws-m1-skills-mcp-dotnet/` — **Units 1.3 + 1.5 (Agent Skills, Official C# MCP Server & `Microsoft.Extensions.AI` Agent, Module 1 Graded Deliverable = 15% grade)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (`.NET 10` solution `GuardiaCloud.Sla.McpWorkshop.sln`, incomplete `SKILL.md` with `verify-minimal-api.sh`, baseline `get_client_sla_policy` MCP tool, 2 passing tests)
     - `solution/` (`.NET 10` reference solution passing `verify-minimal-api.sh` + 6 xUnit tests: 3 C# MCP tools with `ModelContextProtocol v2.3.0`, `ReadOnlyHint` annotations, indirect prompt-injection sanitization, and `SlaTriageAgent` using `Microsoft.Extensions.AI v10.11.0`).
  6. `workshops/ws-m2-harness-oracle-dotnet/` — **Units 1.4 + 2.3 (Harness Engineering, `NetArchTest` Architectural Oracle & HITL vs. Full AI in `git worktrees`)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (`.NET 10` solution `GuardiaCloud.Sla.HarnessLab.sln`, bloated `AGENTS.md` anti-pattern, `.claude/settings.json.example`, `scripts/post-edit-dotnet-hook.sh`, `LegacyVibeCodedHelper.cs` architectural violation in `Domain`, 2 baseline tests)
     - `solution/` (`.NET 10` reference solution passing `./scripts/post-edit-dotnet-hook.sh` + 7 xUnit tests: 3 `NetArchTest.Rules v1.3.2` fitness functions + 4 `WebApplicationFactory` tests for Tarea A [HITL financial credit engine] and Tarea B [Full AI shift export summary], plus `comparativa-hitl-vs-full-ai.md`).

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search · `.NET SDK 10.0.402`.

## NEXT ACTIONS (ordered)
1. Re-check for news from Max at session start (`./scripts/wa-max-chat.sh | tail -20`; S-03 `modifiedTime`).
2. **Ask Fab (`Q-016`) whether to:**
   - **(a) [Option C from earlier, kept in mind for the weekend async handoff]** Build the **Async Update & Walkthrough Pack for Max** (`curriculum/2026-10-30_update-async-para-max.md` + paste-ready WhatsApp summary message) explaining all improvements from *Temario v1* $\rightarrow$ *Temario v2* and walking through the 3 completed `.NET 10` workshops; OR
   - **(b)** Build the **Module 3 Capstone Specification & Seed Package (`workshops/ws-m3-capstone-dotnet/`, Units 3.1–3.4, 40% of final grade)** first so the entire evaluation spine (Modules 1, 2, and 3) is complete before packaging the update for Max.

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
Completed so far:
- P1 Audit & Proposed Temario v2 (.NET + Azure, Rioplatense): curriculum/2026-10-30_syllabus-review-v1.md & curriculum/2026-10-30_temario-v2-propuesta.md
- 3 Complete .NET 10 Workshop Packages (with compilable & tested starter/ and solution/):
  1. workshops/ws-m2-sdd-dotnet/ (Units 2.1 + 2.4: SDD with Spec Kit v1.2.5 & OpenSpec v1.15.0)
  2. workshops/ws-m1-skills-mcp-dotnet/ (Units 1.3 + 1.5: SKILL.md + C# MCP Server ModelContextProtocol v2.3.0 + Microsoft.Extensions.AI v10.11.0)
  3. workshops/ws-m2-harness-oracle-dotnet/ (Units 1.4 + 2.3: Harness Engineering + NetArchTest.Rules v1.3.2 Oracle + HITL vs. Full AI in git worktrees)
Follow the session start/end protocols in AGENTS.md. Tell Fab in 3-5 lines what's new and ask Q-016 (build the Async Update Pack for Max vs. Module 3 Capstone Spec).
```
