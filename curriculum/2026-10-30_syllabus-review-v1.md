# P1 Syllabus Audit — Review of Max's *Temario v1* & Blueprint for *v2*

- **Date:** 2026-10-30
- **Author:** Antigravity (for Fab)
- **Input audited:** `sources/max-docs/2026-10-28_temario-desarrollo-sw-con-ia.md` (*Temario: Desarrollo de Software con IA*, 52 h, 3 modules, 13 units)
- **Evidence base:** `research/2026-10-30_tooling-and-dotnet-azure-verification.md`
- **Target constraints (`D-009`..`D-016`):** Audience = Buenos Aires software consultancy engineers, tech leads, and architects; Primary stack = **.NET + Azure**; Deliverable register = **Rioplatense Spanish (voseo)**; Workshop format = 2–4 h hands-on package inside each unit.

---

## 1. Executive Summary: What Works vs. 7 Structural Gaps in *Temario v1*

### What works well in Max's v1 (Keep)
1. **Macro-progression (Tooling $\rightarrow$ Methodology/SDD $\rightarrow$ Capstone Execution):** Moving from understanding the agent/harness (Module 1) to disciplining it via Spec-Driven Development (Module 2) and proving it in a team project (Module 3) is pedagogically sound.
2. **Focus on Harness Engineering (1.4) & SDD (Module 2):** Positioning `AGENTS.md`/`CLAUDE.md`, hooks, MCPs, and Spec-Driven Development as the core engineering discipline (rather than "prompt engineering tricks") aligns with the Oct 2026 state of the art.
3. **Arithmetic & Evaluation structure:** The 20 h + 18 h + 14 h = 52 h split and the 5-part deliverable grading table (15% + 15% + 25% + 35% + 10% = 100%) are clean and well-proportioned.

### 7 Gaps to Fix in *Temario v2*
1. **Practice Ratio Mismatch (36% actual vs. 60–70% promised):**
   - *Finding:* The v1 header states *"cada unidad combina 30–40% de teoría y 60–70% de práctica guiada"*. However, adding up the blocks explicitly labeled as practice across Module 1 (20 h) and Module 2 (18 h) yields only **~11–13.75 h out of 38 h (29%–36%)**. Units 2.2 and 2.3 have only 45 minutes of practice in a 4-hour session (**18.75%**).
   - *Fix:* Compress passive theory blocks into 20–30 min conceptual framing + live instructor walkthroughs, and turn the core of every unit into a **2.0 to 3.5 h structured Workshop (`D-015`)**, bringing Modules 1–2 to **62.5% real practice** (and **70% across the 52 h course**).
2. **Missing .NET + Azure Ecosystem (`D-014`):**
   - *Finding:* Because Max generated v1 via generic Claude prompting, the draft defaults to Python/TypeScript ecosystems:
     - **Unit 1.2** mentions multiple IDEs without settling on a focused standard set for the classroom: we simplify and standardize the course IDEs on **VS Code (with GitHub Copilot), Cursor, and Windsurf** (`D-024`), while allowing developers to use their own habitual IDE if they prefer.
     - **Unit 1.3** teaches *only* `Claude Agent SDK` and `OpenAI Agents SDK` (Python/TS), ignoring **`Microsoft.Extensions.AI` (`v10.11.0`)**, **Microsoft Agent Framework (`Microsoft.Agents.AI` `v1.27.0`, unifying Semantic Kernel & AutoGen)**, and **Azure AI Foundry Agent Service**.
     - **Unit 1.5 (MCP)** explicitly tells students to build an MCP server *"con el SDK de TypeScript o Python"*, overlooking the official Microsoft-co-maintained **C# MCP SDK (`ModelContextProtocol` NuGet `v2.3.0` and `ModelContextProtocol.AspNetCore`)** and the official **Azure MCP Server (`microsoft/mcp`)**.
   - *Fix:* Make **.NET (C# 13 / .NET 9–10, ASP.NET Core Minimal APIs, EF Core, xUnit, Testcontainers, NetArchTest) + Azure** the primary spine of every workshop.
3. **Outdated / Imprecise Tool Commands in Unit 2.4 (SDD):**
   - *Finding:* Unit 2.4 lists GitHub Spec Kit commands as *"specify, plan, tasks e implement"*. As of **Spec Kit `v1.2.5` (Oct 2026)**, the CLI is `specify` (`specify init --integration ...`), the agent skills are `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, and **`/speckit-converge`** (which verifies implementation against the spec), plus bundled extensions for **Bug fixing** (`specify extension add bug`) and **Idea assessment**.
   - *Finding:* OpenSpec (`v1.15.0`) is mentioned in passing, without highlighting its main value for a consultancy: **brownfield delta specs** (`/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`).
4. **Cross-Harness Interoperability Gotcha (`AGENTS.md` vs. `CLAUDE.md`):**
   - *Finding:* Unit 1.4 treats `CLAUDE.md` and `AGENTS.md` as interchangeable, and encourages generating instruction files without warning about bloat.
   - *Fix:* Teach the verified interoperability pattern (`AGENTS.md` is read natively by Codex, Copilot, Cursor, Windsurf; Claude Code requires `CLAUDE.md` importing `@AGENTS.md`, per issue `#34235`) AND cite the **ETH Zurich study (`arXiv:2602.11988`)** showing that LLM-generated `AGENTS.md` files reduce accuracy by 0.5–2% and increase token cost by 20–23%, whereas short human-curated files improve results.
5. **No Measurable Learning Objectives per Unit:**
   - *Finding:* Modules have a 1-sentence goal, but the 13 units have zero observable learning objectives or concrete output artifacts.
   - *Fix:* Add explicit learning objectives and a **chained deliverable artifact** to every single unit.
6. **Disconnected Practice vs. Module 3 Time Crunch (6 hours for a full project):**
   - *Finding:* Module 3 gives teams only **6 hours of implementation (Unit 3.4)** to set up CI, configure MCPs, build the base project, run 2 sprints, integrate, QA, and demo. If teams start from `dotnet new` in Unit 3.4, they will spend 4 hours fighting boilerplate, Docker, and EF migrations.
   - *Fix (The "Hilo Conductor" Seed Repo):* Introduce a single **Enterprise .NET + Azure Seed Repository** in Unit 1.2 that students use across Units 1.2 $\rightarrow$ 2.4 to build their `AGENTS.md`, C# Architecture/Testing Skills, C# MCP Server, and SDD pipeline. In Module 3, teams build a major multi-feature evolution on top of a **pre-scaffolded brownfield .NET + Azure solution** (with CI, Testcontainers, and OpenAPI already wired) so all 6 hours of Unit 3.4 go into agentic feature delivery.
7. **Missing Verification Oracle & Architectural Drift Guardrails in .NET:**
   - *Finding:* Units 2.1–2.3 mention "tests como oráculo", but don't specify how to make architecture machine-checkable so agents don't violate layering.
   - *Fix:* Introduce **Architectural Fitness Functions (`NetArchTest.Rules` / `ArchUnitNET`)** + **Integration Testing (`WebApplicationFactory` + `Testcontainers`)** + **OpenAPI Contract Testing** as the deterministic oracle that lets "Full AI" agents self-correct in loop.

---

## 2. Practice vs. Theory Ratio Audit (v1 vs. Proposed v2)

| Unit | Total Hours | v1 Explicit Practice | v1 Practice % | v2 Workshop / Guided Practice | v2 Practice % |
|---|---:|---:|---:|---:|---:|
| **1.1 Diseño** | 4.0 h | 1.25 h (1:15) | 31% | **2.50 h (2:30)** | **62.5%** |
| **1.2 Herramientas de desarrollo** | 4.0 h | 1.00 h (1:00) | 25% | **2.50 h (2:30)** | **62.5%** |
| **1.3 Agentes y Skills** | 4.0 h | 1.00 h (1:00) | 25% | **2.50 h (2:30)** | **62.5%** |
| **1.4 Harness Engineering** | 6.0 h | ~2.00 h (mixed) | 33% | **3.75 h (3:45)** | **62.5%** |
| **1.5 MCPs** | 2.0 h | 0.75 h (0:45) | 37.5% | **1.25 h (1:15)** | **62.5%** |
| **2.1 Spec** | 4.0 h | 1.00 h (1:00) | 25% | **2.50 h (2:30)** | **62.5%** |
| **2.2 Estimación, impacto y planning** | 4.0 h | 0.75 h (0:45) | 18.75% | **2.50 h (2:30)** | **62.5%** |
| **2.3 Implementation (Full AI vs HITL)** | 4.0 h | 0.75 h (0:45) | 18.75% | **2.50 h (2:30)** | **62.5%** |
| **2.4 Herramientas para SDD** | 6.0 h | ~2.25 h (mixed) | 37.5% | **3.75 h (3:45)** | **62.5%** |
| **3.1–3.4 Módulo 3 (Proyecto)** | 14.0 h | ~12.50 h | 89% | **12.50 h (12:30)** | **89.3%** |
| **COURSE TOTAL** | **52.0 h** | **~23.25 h** | **~44.7%** | **36.25 h** | **69.7%** |

---

## 3. Unit-by-Unit Audit & .NET/Azure Adaptation

### Unit 1.1 — Diseño (4 hs)
- **Claim Audit:**
  - *Verified:* Figma Make, v0, Lovable, Google Stitch (`stitch.withgoogle.com`), Claude Artifacts all exist and match the stated use cases.
  - *Nuance to add:* All five generate React/Tailwind or HTML/CSS by default, not native Blazor/Razor.
- **Learning Objectives (New):**
  1. Generate a multi-screen clickable flow from a structured domain prompt + visual reference using Google Stitch, v0, or Figma Make.
  2. Extract design tokens (colors, typography, spacing) and component rules into a machine-readable design system file that coding agents respect.
  3. Execute a clean ** Design-to-.NET Handoff**: connect generated React/Tailwind UI to an ASP.NET Core OpenAPI contract OR convert generated HTML/Tailwind components into strongly-typed Blazor `.razor` components.
- **Workshop Rebalance (1:15 $\rightarrow$ 2:30 hands-on):**
  - Merge passive tool overview + prompting rules into a 1:00 interactive block, 0:30 on Design Systems & .NET Handoff, and **2:30 Workshop** where students design a 3–4 screen flow for the course's reference domain, extract tokens, and produce the frontend handoff package.

### Unit 1.2 — Herramientas de Desarrollo (4 hs)
- **Claim Audit:**
  - *Verified:* VS Code + GitHub Copilot, Cursor, Windsurf, Claude Code, Codex.
  - *Simplification (`D-024`):* Standardize the classroom IDE coverage on **VS Code (with GitHub Copilot), Cursor, and Windsurf**, letting developers use their own habitual IDE if they want rather than expanding into Visual Studio or JetBrains Rider/Junie.
  - *Empirical anchor added:* METR Jul 2025 RCT (19% slowdown vs. 20% perceived speedup) and DORA 2025 to frame why undisciplined IDE chat ("vibe coding") creates rework.
- **Learning Objectives (New):**
  1. Configure an AI-assisted IDE (**VS Code + GitHub Copilot, Cursor, or Windsurf**, or the developer's habitual IDE) with workspace rules (`.github/copilot-instructions.md` / `.cursor/rules` / `.windsurfrules` / `AGENTS.md`) and solution-level context.
  2. Execute 5 high-ROI daily engineering workflows on a brownfield .NET solution: legacy code comprehension, Roslyn-safe refactoring, xUnit + FluentAssertions/Verify test generation, exception/dump debugging, and PR security/quality review.
  3. Detect and prevent hallucinated NuGet packages (slopsquatting), hardcoded secrets, and subtle async/EF Core anti-patterns (`N+1`, sync-over-async, missing `CancellationToken`).
- **Workshop Rebalance (1:00 $\rightarrow$ 2:30 hands-on):**
  - Introduce the **Course Seed Repository (.NET 9/10 + Azure)** here. Students spend 2.5 hours running the 5 daily workflows on real C# projects and measuring verification time.

### Unit 1.3 — Agentes y Skills (4 hs)
- **Claim Audit:**
  - *Verified:* Agent loop, Anthropic/open `SKILL.md` standard (`agentskills.io`, progressive disclosure of `SKILL.md` + `scripts/` + `references/`).
  - *Critical Gap Fixed:* Replace the Python/TS-only SDK bias (*"Claude Agent SDK y OpenAI Agents SDK"*) with **`.NET Agent SDKs first`**: **`Microsoft.Extensions.AI` (`v10.11.0`, `IChatClient`, `AIFunctionFactory`)** and **Microsoft Agent Framework (`Microsoft.Agents.AI` `v1.27.0` + Azure AI Foundry Agent Service)**, while keeping Claude Agent SDK and OpenAI Agents SDK as a 15-minute architectural comparison.
- **Learning Objectives (New):**
  1. Distinguish deterministic workflows from autonomous tool-using agents and select the minimal pattern (chaining, routing, orchestrator-workers, evaluator-optimizer) that solves a problem.
  2. Author, test, and package a portable **Team Skill (`SKILL.md` + validation script)** that enforces .NET API conventions (ProblemDetails RFC 9457, FluentValidation, EF Core projection rules, or PR review checklist).
  3. Build a minimal programmatic agent in C# using `Microsoft.Extensions.AI` (`IChatClient`) and `Microsoft.Agents.AI` connected to Azure AI Foundry / Azure OpenAI.
- **Workshop Rebalance (1:00 $\rightarrow$ 2:30 hands-on):**
  - 1:45 building and testing a reusable `.NET Team Skill` (`SKILL.md` + `dotnet` verification script) + 0:45 hands-on lab wiring a C# agent with `Microsoft.Extensions.AI` and `Microsoft.Agents.AI`.

### Unit 1.4 — Harness Engineering (6 hs)
- **Claim Audit:**
  - *Verified:* Claude Code (`v2.1.314`), OpenAI Codex (`rust-v0.166.0`), Devin (Sessions, Knowledge, Playbooks, DeepWiki).
  - *Corrections added:*
    1. Explicit `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`) cross-harness setup so Copilot, Codex, Cursor, and Claude Code read the exact same rules.
    2. ETH Zurich study (`arXiv:2602.11988`) warning against bloated auto-generated `AGENTS.md` files (+20–23% token cost, lower accuracy).
    3. Concrete **.NET Harness Hooks**: configuring `PreToolUse` / `PostToolUse` hooks that run `dotnet build --no-restore`, `dotnet format --verify-no-changes`, and targeted `dotnet test --filter` as automatic feedback loops.
- **Learning Objectives (New):**
  1. Design a lean, high-signal `AGENTS.md` + `CLAUDE.md` hierarchy for a multi-project .NET solution without bloating the context window.
  2. Configure **Claude Code** (permissions, `/plan` mode, subagents, `PreToolUse`/`PostToolUse` hooks running `dotnet` CLI checks, and headless `claude -p` in GitHub Actions / Azure Pipelines).
  3. Operate **OpenAI Codex** (CLI sandbox modes, parallel task execution, cloud PR tasks) and evaluate when to delegate full tickets to **Devin** (using Knowledge & Playbooks).
- **Workshop Rebalance (~2:00 $\rightarrow$ 3:45 hands-on):**
  - Hands-on lab hardening the .NET seed repo's harness (curated `AGENTS.md`, `PostToolUse` `dotnet` build/test hook, custom slash command, and side-by-side solve of the same .NET ticket in Claude Code vs. Codex).

### Unit 1.5 — MCPs (2 hs)
- **Claim Audit:**
  - *Verified:* MCP client-server architecture, `tools`, `resources`, `prompts`, `stdio` and Streamable HTTP transports, OAuth/security risks.
  - *Critical Correction:* Change *"con el SDK de TypeScript o Python"* to **"con el SDK oficial de C# (`ModelContextProtocol` y `ModelContextProtocol.AspNetCore` en NuGet, v2.3.0)"** (mentioning TS/Python as alternatives). Add the official **Azure MCP Server (`microsoft/mcp`)** to the existing servers block.
- **Learning Objectives (New):**
  1. Connect existing MCP servers (GitHub / Azure DevOps, Azure MCP Server, PostgreSQL/SQL Server) to Claude Code, VS Code Copilot, or Cursor with least-privilege credentials.
  2. Build and test a custom **C# MCP Server** using the official `ModelContextProtocol` NuGet package (`[McpServerToolType]`, `[McpServerTool]`, DI with `IHostBuilder`) exposing internal .NET domain/telemetry operations to the coding agent.
- **Workshop Rebalance (0:45 $\rightarrow$ 1:15 hands-on):**
  - 0:45 concise architecture, security (prompt injection, tool poisoning, secret isolation), and Azure/DB MCP configuration + **1:15 hands-on C# MCP Server workshop** (graded as part of the 15% Module 1 deliverable alongside the Unit 1.3 Skill).

### Unit 2.1 — Spec (4 hs)
- **Claim Audit:**
  - *Verified:* Vision $\rightarrow$ Functional Spec $\rightarrow$ Technical Spec $\rightarrow$ Tasks hierarchy; Given/When/Then & EARS notation (`WHEN <trigger> WHILE <precondition> THE SYSTEM SHALL <response>`); ADRs; Project Constitution.
  - *Empirical anchor added:* Larbi et al. (`arXiv:2507.20439`: −20 to −40 pp Pass@1 drop from ambiguous/contradictory specs) and SWE-EVO (`arXiv:2512.18470`: >60% of agent failures are requirement misinterpretations).
- **Learning Objectives (New):**
  1. Transform an ambiguous stakeholder request into a structured **Functional Spec** using EARS and Given/When/Then acceptance criteria, using an AI agent as an adversarial ambiguity detector.
  2. Author a machine-actionable **.NET Technical Spec** specifying Minimal API / OpenAPI contracts (`ProblemDetails`), EF Core entity/migration boundaries, Azure service integration points, and architectural invariants (ADRs).
- **Workshop Rebalance (1:00 $\rightarrow$ 2:30 hands-on):**
  - 1:30 framing + anatomy of specs + **2:30 Workshop** drafting, stress-testing (via an adversarial "Spec Critic" prompt/skill), and peer-reviewing a complete Functional + Technical Spec for a feature in the .NET seed repo.

### Unit 2.2 — Estimación, Análisis de Impacto y Planning (4 hs)
- **Claim Audit:**
  - *Verified:* Impact analysis with agents, task decomposition, review/token cost variables, engineering metrics.
  - *Empirical anchor added:* AgenticFlict (27.67% merge conflict rate in parallel agent PRs), Faros AI / DORA review bottleneck data, and BetterUp/Stanford "Workslop" (~2 h rework per bad artifact).
- **Learning Objectives (New):**
  1. Use an agent in read-only/plan mode to generate a verified **Impact & Risk Report** across a brownfield .NET solution (mapping affected C# projects, EF Core migrations, OpenAPI breaking changes, and missing test coverage).
  2. Decompose a Technical Spec into a **DAG (Directed Acyclic Graph) of small, atomic, verifiable tasks** with explicit file-touch boundaries to prevent the 27.7% parallel-agent merge conflict trap.
  3. Estimate delivery effort by separating **generation time** (compressed by AI) from **verification, review, integration, and QA time** (which scales with diff size and risk).
- **Workshop Rebalance (0:45 $\rightarrow$ 2:30 hands-on):**
  - 1:30 concepts/metrics + **2:30 Workshop** taking the Spec from Unit 2.1, running automated impact analysis on the .NET solution, decomposing it into an ordered `tasks.md` DAG, and contrasting traditional vs. AI-assisted estimates.

### Unit 2.3 — Implementation: Full AI vs. Human-in-the-Loop (4 hs)
- **Claim Audit:**
  - *Verified:* Autonomy spectrum, Full AI (isolated sandbox + tests as oracle + CI), Human-in-the-Loop (checkpoints, plan approval, diff review), static analysis & security gates.
- **Learning Objectives (New):**
  1. Decide per task whether to execute in **Human-in-the-Loop (HITL)** mode or **Full AI (Autonomous)** mode based on domain criticality, blast radius, and oracle strength.
  2. Build a **deterministic .NET Verification Oracle** combining xUnit, `WebApplicationFactory`, `Testcontainers` (real SQL/Redis in Docker), `NetArchTest` architectural rules, and Roslyn analyzers (`TreatWarningsAsErrors`) so an autonomous agent cannot declare victory on broken or un-architectural code.
  3. Execute the same .NET feature task in both modes (HITL vs. Full AI in an isolated `git worktree`) and compare wall-clock time, token cost, diff cleanliness, and human review effort.
- **Workshop Rebalance (0:45 $\rightarrow$ 2:30 hands-on):**
  - 1:30 framing + oracle design + **2:30 Comparative Implementation Lab** (worktree A = HITL pair-programming; worktree B = Full AI against xUnit/Testcontainers/NetArchTest oracle; structured diff review & debrief).

### Unit 2.4 — Herramientas para SDD (6 hs)
- **Claim Audit:**
  - *Verified & Updated:*
    - Birgitta Böckeler / Martin Fowler taxonomy (*Spec-first*, *Spec-anchored*, *Spec-as-source*).
    - **GitHub Spec Kit (`v1.2.5`, Oct 2026):** `specify init`, `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, **`/speckit-converge`**, plus the `bug` extension (`/speckit-bug-assess`, `/speckit-bug-fix`, `/speckit-bug-test`).
    - **OpenSpec (`v1.15.0`, Oct 2026):** Highlight its **brownfield delta workflow** (`openspec/specs/` + `openspec/changes/`, `/opsx:explore` $\rightarrow$ `/opsx:propose` $\rightarrow$ `/opsx:apply` $\rightarrow$ `/opsx:archive`), which is often superior to Spec Kit when modifying existing enterprise .NET systems.
    - **AWS Kiro (`kiro.dev`):** `.kiro/specs/` (`requirements.md`, `design.md`, `tasks.md`), `.kiro/hooks/`, `.kiro/steering/`.
    - **BMAD Method (`v6.12.4` / `v7`)** & **Tessl (`tessl.io` Spec Registry tiles + framework)**.
- **Learning Objectives (New):**
  1. Classify SDD tools along the *Spec-first / Spec-anchored / Spec-as-source* spectrum and choose between **Greenfield SDD (GitHub Spec Kit)** and **Brownfield Delta SDD (OpenSpec)** for a given consultancy engagement.
  2. Execute a complete feature cycle in **GitHub Spec Kit (`v1.2.5`)** through `/speckit-converge` on a .NET project, and a brownfield change cycle in **OpenSpec (`v1.15.0`)**.
  3. Assemble a **Custom Team SDD Workflow** in the team's chosen harness combining `AGENTS.md`, `SKILL.md` templates, and `.NET` verification hooks, ready for Module 3.
- **Workshop Rebalance (~2:15 $\rightarrow$ 3:45 hands-on):**
  - Hands-on lab: (Part A, 1:30) GitHub Spec Kit end-to-end on .NET; (Part B, 1:00) OpenSpec brownfield delta lab + Kiro demo; (Part C, 1:15) building and locking the team's SDD workflow for Module 3.

### Module 3 — Ejecución de Proyecto de Desarrollo (14 hs: Units 3.1–3.4)
- **Audit & De-Risking Strategy:**
  - *Problem:* 14 hours total (2 h functional discovery + 4 h specs + 2 h planning + 6 h implementation) is realistic **only if** teams do not waste time on project scaffolding, infrastructure plumbing, or inventing a domain from scratch.
  - *Solution in v2:*
    1. **Pre-Built Brownfield .NET 9/10 + Azure Capstone Baseline:** Instructor provides a working multi-project .NET solution (e.g., an enterprise multi-tenant Order/Claims/Field-Service or Consultancy Operations platform with ASP.NET Core Minimal APIs, EF Core + SQLite/SQL Server via Testcontainers, OpenAPI, a basic React or Blazor UI, GitHub Actions CI, and 3 intentional bugs + 4 unbuilt business capabilities).
    2. **Unit 3.1 (2 h):** Teams use an AI discovery workflow to interview the instructor ("client"), audit the existing brownfield codebase with an agent, and produce a validated **Functional Understanding & Scope Document**.
    3. **Unit 3.2 (4 h):** Teams configure their repo Constitution (`AGENTS.md`/`CLAUDE.md`), UI prototype (Unit 1.1 tools), Functional Spec (EARS/GWT), and Technical Spec (OpenAPI + EF Core schema + ADRs), followed by **Cross-Team Adversarial Spec Review** (Team A's agent + humans audit Team B's spec for ambiguities).
    4. **Unit 3.3 (2 h):** Teams run agentic impact analysis, split work into a conflict-free `tasks.md` DAG across 3–5 team members (assigning which tasks run Full AI in parallel `git worktrees` vs. HITL), and lock their 6-hour execution board.
    5. **Unit 3.4 (6 h):**
       - **Sprint 1 (2:00):** Wire team's C# MCP server & skills from Module 1, write architectural/integration oracle tests first, and land core backend + DB vertical slices.
       - **Checkpoint (0:30):** Run `/speckit-converge` (or `/opsx:verify`) to detect spec drift early; unblock integration.
       - **Sprint 2 (2:00):** Parallel agent execution (`git worktrees`) for remaining vertical slices + UI integration + automated PR review.
       - **Integration & QA (0:45):** Cross-team acceptance testing strictly against the Unit 3.2 Spec criteria.
       - **Demo & Metrics Retrospective (0:45):** Live working demo + telemetry readout (lead time, % tasks Full AI vs. HITL, spec changes vs. code rework, merge conflicts).

---

## 4. Recommendation for `Q-013`: Which Workshop Should We Build First?

Now that the full syllabus is audited and the v2 proposal is ready, we need to pick **one 2–4 h workshop (`D-015`)** to build out completely (objectives, prep, step-by-step guide, starter .NET repo, reference solution, rubric, facilitator guide) before syncing with Max.

### Recommended Anchor Workshop: **Unit 1.5 + 1.3 Combined Deliverable Workshop — *"Construcción de una Skill de Equipo y un Servidor MCP en C# (.NET)"* (or Unit 2.3/2.4 SDD Workshop)**

Here are the top 3 options to choose from:

1. **Option A (Recommended — High Technical Differentiation for Max): Unit 1.3 + 1.5 (.NET Agent Skill + Official C# MCP Server, ~3.5 h combined lab / Module 1 Graded Deliverable)**
   - *Why:* It is the **graded capstone of Module 1 (15% of final grade)**, directly showcases the **.NET + Azure** upgrade (`ModelContextProtocol` NuGet v2.3.0 in C# + `SKILL.md` for .NET API conventions), is self-contained, and will immediately impress Max (who is a former Microsoft MVP in .NET!).
2. **Option B (Methodology Core): Unit 2.1 + 2.4 (Spec-Driven Development on .NET with GitHub Spec Kit v1.2.5 & OpenSpec v1.15.0, ~3.5 h)**
   - *Why:* It is the heart of Module 2 (15% graded deliverable) and proves how a vague requirement becomes a verified .NET Minimal API + xUnit/Testcontainers slice via `/speckit-specify` $\rightarrow$ `/speckit-converge`.
3. **Option C (Harness & Verification Oracle): Unit 1.4 + 2.3 (Harness Engineering & Full AI vs. HITL in .NET with xUnit, Testcontainers & NetArchTest, ~3.5 h)**
   - *Why:* Demonstrates `AGENTS.md`, `.NET` CLI hooks, and the deterministic test oracle that makes autonomous coding work in C#.
