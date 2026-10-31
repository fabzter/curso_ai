# 00 — STATE (living; update at the end of EVERY session)

**Last updated:** 2026-10-30 18:45 CST · Antigravity (Gemini 4 Argon) · Phase: **P1, P2 & All 4 `.NET 10` Workshop + Capstone Packages Done (100% of Course Evaluation Spine Built) → Ready for Option C (Async Weekend Update Pack for Max)**

## One-line status
Completed the **P1 Syllabus Audit** (`curriculum/2026-10-30_syllabus-review-v1.md`), the **Proposed Temario v2 in Rioplatense Spanish** (`curriculum/2026-10-30_temario-v2-propuesta.md`), and **all four `.NET 10` Workshop & Capstone Packages covering 100% of the graded deliverables across Modules 1, 2, and 3** (`ws-m1-skills-mcp-dotnet`, `ws-m2-sdd-dotnet`, `ws-m2-harness-oracle-dotnet`, and `ws-m3-capstone-dotnet`), all with compilable & tested `starter/` and `solution/` projects.

## What we know (details: `01-CONTEXT.md`)
- Course: *Desarrollo de Software con IA*, 52 h, 3 modules, 13 units, in person. **Audience: members of a Buenos Aires software consultancy** (a friend of Max's; name unknown; not Shifta; not Disney staff).
- **WhatsApp update (2026-10-30 16:21–16:34, `S-01`):** Max said he'll work on the course over the weekend; Fab told him: *"Dale te paso update y explicación de lo que hice para que pueda ser async este fin"*.
- **Deliverables completed so far (all committed locally):**
  1. `research/2026-10-30_tooling-and-dotnet-azure-verification.md` — Primary-source verification of all tools/SDKs + .NET/Azure equivalents (`ModelContextProtocol` NuGet `v2.3.0`, `Microsoft.Extensions.AI` `v10.11.0`, `Microsoft.Agents.AI` `v1.27.0`, `NetArchTest.Rules` `v1.3.2`, `github/spec-kit` `v1.2.5`, `Fission-AI/OpenSpec` `v1.15.0`, etc.).
  2. `curriculum/2026-10-30_syllabus-review-v1.md` — Unit-by-unit audit of Max's Temario v1 (rebalancing practice from 36% to 62.5%–70%, adding learning objectives, .NET/Azure spine, and brownfield seed repo strategy).
  3. `curriculum/2026-10-30_temario-v2-propuesta.md` — Complete 52 h proposed v2 syllabus in **Rioplatense Spanish (voseo)**.
  4. `workshops/ws-m1-skills-mcp-dotnet/` — **Units 1.3 + 1.5 (Module 1 Graded Deliverable = 15% grade)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (2 passing tests) & `solution/` (`verify-minimal-api.sh` + 6 passing xUnit tests: `SKILL.md`, `ModelContextProtocol v2.3.0` C# MCP server with 3 tools, anti-injection sanitization, and `Microsoft.Extensions.AI v10.11.0` `SlaTriageAgent`).
  5. `workshops/ws-m2-sdd-dotnet/` — **Units 2.1 + 2.4 (Module 2 Graded Deliverable = 15% grade)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (2 passing tests + 1 intentional bug) & `solution/` (Spec Kit `v1.2.5` + OpenSpec `v1.15.0` artifacts and 4 passing `WebApplicationFactory` test suites).
  6. `workshops/ws-m2-harness-oracle-dotnet/` — **Units 1.4 + 2.3 (Harness Engineering, `NetArchTest` Oracle & HITL vs. Full AI in `git worktrees`)**:
     - `00-WORKSHOP-SPEC.md`, `01-GUIA-PASO-A-PASO.md`, `02-GUIA-FACILITADOR-Y-RUBRICA.md`
     - `starter/` (2 baseline tests + `LegacyVibeCodedHelper.cs` violation) & `solution/` (`post-edit-dotnet-hook.sh` + 7 passing xUnit tests: 3 `NetArchTest.Rules v1.3.2` + 4 `WebApplicationFactory`, plus `comparativa-hitl-vs-full-ai.md`).
  7. `workshops/ws-m3-capstone-dotnet/` — **Units 3.1–3.4 (Module 3 14-Hour Capstone Project = 70% of final grade: Entregables #3 [25%], #4 [35%], #5 [10%])**:
     - `00-WORKSHOP-SPEC.md`, `01-PLIEGO-CASO-Y-GUIA-EQUIPOS.md`, `02-GUIA-FACILITADOR-Y-RUBRICAS-M3.md`
     - `starter/` (`.NET 10` solution `GuardiaCloud.CommandCenter.sln`, `pliego-licitacion-cliente.md`, `plantilla-retrospectiva-metricas.md`, `BUG-301` seeded, 3 passing baseline tests)
     - `solution/` (`.NET 10` reference solution with `specs/command-center-v2/{spec,plan,tasks}.md`, `retrospectiva-metricas-equipo-referencia.md`, and **8 passing xUnit tests** in 545 ms covering `NetArchTest`, `BUG-301`, `FEAT-301`, `FEAT-302`, and `FEAT-303`).

## Verified access (2026-10-30, `./scripts/check-access.sh` → 15/15)
gog (Drive, `faboster@gmail.com`, readonly) · WhatsApp bridge DBs + REST download · local ASR (Nemotron 3.5 + Parakeet v3 via transcribe.cpp) · ffmpeg/pandoc · vault `knowledge` (read) · firecrawl + web search · `.NET SDK 10.0.402`.

## NEXT ACTIONS (ordered)
1. Re-check for news from Max at session start (`./scripts/wa-max-chat.sh | tail -20`; S-03 `modifiedTime`).
2. **Ask Fab (`Q-017`) whether to proceed now with Option C:**
   - Build the **Async Weekend Update & Walkthrough Pack for Max** (`curriculum/2026-10-30_update-async-para-max.md` + a paste-ready WhatsApp message for Fab to review/send at his discretion) explaining the changes from *Temario v1* $\rightarrow$ *Temario v2* and walking through the 4 completed `.NET 10` workshop/capstone packages, OR build any remaining unit-specific labs first (e.g., Unit 1.1/1.2 UI + IDE flows).

## Do-not-do list for the next agent
No sends/edits/shares · no vault/Drive writes without OK · never touch Luca anything · don't ingest Max chat before 2026-10-13 · don't state unverified tool facts · don't push git.

## Paste-ready handoff prompt (for a fresh session / another agent)
```
You are continuing a long-horizon project in ~/Documents/curso_ai (course "Desarrollo de Software con IA", Fab + Max Déboli).
Read AGENTS.md, then docs/00-STATE.md, docs/03-OPEN-QUESTIONS.md, docs/02-DECISIONS.md. Run ./scripts/check-access.sh.
Check for new WhatsApp from Max (./scripts/wa-max-chat.sh | tail -20) and whether the Drive docx changed (see docs/04-SOURCES.md S-03).
Completed so far:
- P1 Audit & Proposed Temario v2 (.NET + Azure, Rioplatense): curriculum/2026-10-30_syllabus-review-v1.md & curriculum/2026-10-30_temario-v2-propuesta.md
- All 4 .NET 10 Workshop & Capstone Packages (all with compilable & tested starter/ and solution/):
  1. workshops/ws-m1-skills-mcp-dotnet/ (Units 1.3 + 1.5, 15% grade)
  2. workshops/ws-m2-sdd-dotnet/ (Units 2.1 + 2.4, 15% grade)
  3. workshops/ws-m2-harness-oracle-dotnet/ (Units 1.4 + 2.3, Harness + NetArchTest + HITL vs. Full AI)
  4. workshops/ws-m3-capstone-dotnet/ (Units 3.1-3.4, 14h Capstone = 70% grade)
Follow the session start/end protocols in AGENTS.md. Tell Fab in 3-5 lines what's new and ask Q-017 (build the Async Weekend Update Pack for Max now vs. additional unit labs).
```
