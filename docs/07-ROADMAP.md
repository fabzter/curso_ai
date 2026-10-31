# 07 — Roadmap, research backlog, first-read of the syllabus

> Phases are a **proposal** (not yet agreed with Fab/Max). Adjust freely, but log changes in `02-DECISIONS.md`.

## Phases
| Phase | Goal | Exit criteria | Status |
|---|---|---|---|
| P0 Foundation | Repo, access, sources ingested, long-horizon scaffolding | `check-access.sh` green; S-01..S-03 ingested; AGENTS/STATE written | **Done 2026-10-30** |
| P1 Syllabus review (Fab solo, D-009/D-013) | Review and improve Max's Temario v1 unit by unit: verify claims, fix gaps and pacing, adapt to .NET/Azure, rewrite in Rioplatense. Output: `curriculum/` review + proposed v2 syllabus | Review doc + v2 draft ready to show Max; Q-013 ready to pick | **Done 2026-10-30** |
| P2 Research | Verify the tooling landscape per unit, with dated sources; benchmark comparable courses | Baseline verification note in `research/2026-10-30_tooling-and-dotnet-azure-verification.md`; deepen per workshop in P3 | **Baseline Done 2026-10-30** |
| P3 Design | Pick ONE unit (`Q-013`) and build its full workshop (`D-015` package), then additional workshops / Module-3 case | `ws-m1-skills-mcp-dotnet` (M1), `ws-m2-sdd-dotnet` (M2), `ws-m2-harness-oracle-dotnet` (M1/M2), `ws-m3-capstone-dotnet` (M3 Capstone), and `2026-10-30_update-async-para-max.md` **All Done 2026-10-30** | **Done 2026-10-30 (4 Complete `.NET 10` Packages + Max Async Pack)** |
| P4 Build | Slides/handouts, exercise repos & templates, instructor guide, facilitator notes | Dry-run-ready package | Not started |
| P5 Pilot & revise | Dry run (internal), fix timing/difficulty, freeze version for client | Signed-off v1.0 | Not started |

## Research backlog (all tool facts must be re-verified; "today" matters)
1. **Per-unit landscape check** of every tool named in the draft: Figma Make, v0, Lovable, Google Stitch; Cursor, Windsurf, Copilot, JetBrains AI; Claude Code, Codex (CLI + cloud), Devin (Knowledge/Playbooks/DeepWiki); Claude Agent SDK, OpenAI Agents SDK; MCP spec/transports/auth; GitHub Spec Kit, Kiro, BMAD, OpenSpec, Tessl. For each: current version/date, pricing/licensing model, enterprise/privacy posture, what changed in the last 90 days.
2. **Skills / AGENTS.md / CLAUDE.md** as cross-tool standards: what is portable across harnesses today, what isn't (this very repo is a worked example).
3. **Evidence on productivity & quality** of AI-assisted dev (RCTs, industry surveys) to anchor 2.2 "estimación en la era de agentes" and the metrics block; flag conflicting studies.
4. ~~Enterprise constraints~~ **Deprioritized** (D-011): client policy/licensing is out of scope for now. Keep the security/IP *teaching* content from the syllabus.
4b. **.NET + Azure fit** (D-014): for each tool in the draft, how well it works with .NET/Azure (e.g. IDE support in Visual Studio/Rider/VS Code, Azure DevOps/GitHub integration, Azure-hosted model access, a C#/.NET MCP SDK, .NET agent frameworks). All of this is *to verify* with dated sources; nothing here is established.
5. **Comparable courses/workshops** (e.g. the LIDR multi-agent workshop, vendor academies): structure, duration, price, hands-on ratio, what learners ask (Fab's stated interest).
6. **Module 3 case**: candidate "client" scenarios that are completable in 6 h of implementation by teams of 3-5 with agents, with a seeded repo and automated acceptance tests.
7. **Environment logistics**: accounts, license fallbacks (Devin/Kiro by demo), offline/network constraints, sandbox repos.

## First-read observations on Temario v1 (Antigravity, 2026-10-30; hypotheses to discuss with Max, NOT conclusions)
- **Internally consistent:** all unit/module hours add up (52 h) and assessment weights = 100%.
- **Module 3 is tight:** 6 h of implementation (two 2 h sprints + checkpoint + QA + demo) to deliver a "working project" with specs, CI, tests and MCPs per team; needs a heavily scaffolded seed repo and a very scoped case, or the 35% grade becomes a lottery.
- **Claimed 60-70% practice** isn't measured in the doc; several blocks read as lecture. Audit the actual ratio per unit.
- **Perishable content:** 1.4 (6 h on three vendor harnesses) and 2.4 (6 h on five SDD tools) are the most time-sensitive; schedule them last in prep and verify close to the delivery date.
- **License/access risk:** hands-on Claude Code/Codex for everyone, Devin/Kiro "by demo": depends on Q-004; the grading of "skill + MCP server" (15%) presumes working access at the end of Module 1.
- **Possible gaps to evaluate (inference, may be intentionally out of scope):** evaluating/observing agent output beyond "tests as oracle"; working in legacy/brownfield code; cost control & governance; team adoption/change management; security review of agent-generated changes beyond 1.2/1.5 touchpoints.
- **Authoring provenance:** produced by prompting Claude → expect plausible-but-unverified feature claims (e.g., exact capabilities of Kiro hooks/steering, Tessl, Devin DeepWiki, SDK names). Verify each before it appears on a slide.
- **Audience unknown** (Q-002) → all depth/pacing decisions are provisional.
