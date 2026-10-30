# Tooling, SDD & .NET/Azure Ecosystem Verification (P1 Research)

- **Date:** 2026-10-30
- **Author:** Antigravity
- **Scope:** Fact-check every tool, SDK, protocol, and methodology claim in Max's *Temario v1* (`sources/max-docs/2026-10-28_temario-desarrollo-sw-con-ia.md`), verify **.NET + Azure** first-class equivalents (`D-014`), and anchor the methodology units in empirical evidence (`D-011`).
- **Evidence Tagging Convention (`AGENTS.md`):**
  `claim · source URL · accessed YYYY-MM-DD · version/date of the tool · confidence (high/med/low)`
  Every section separates **Fact** (sourced), **Inference** (ours), and **Open** (unknown).

---

## 1. Empirical Evidence Base (Why Ad-Hoc Prompting Fails & Why SDD Matters)

> Cross-referenced from verified primary sources in `~/Documents/agentic_sdlc_implementation_consulting/docs/01-investigacion.md` (audited 2026-08-18, re-verified 2026-10-30). Use these in Units **1.2**, **2.1**, **2.2**, and **2.3** so estimation and quality discussions rest on data rather than hype.

### Facts (Sourced)
1. **Experienced developers slowed down by 19% in ad-hoc AI use while believing they were 20% faster (39-point perception gap):** Randomized Controlled Trial (RCT) of 16 experienced open-source developers across 246 real tasks on their own repositories using Cursor Pro + Claude 3.5/3.7 Sonnet · `https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/` · accessed 2026-10-30 · METR Study (Jul 2025) · **confidence: high**.
2. **AI acts as an amplifier: it increases throughput AND increases delivery instability/rework when guardrails and specs are absent:** DORA 2025 report on AI-assisted software development · `https://dora.dev/dora-report-2025/` · accessed 2026-10-30 · DORA (2025) · **confidence: high**.
3. **Specification clarity directly predicts LLM code generation success (degrading problem statement clarity alone drops Pass@1 by 20 to 40 percentage points):** Controlled experiment keeping reference code constant while introducing ambiguity (−25 to −30 pp), incompleteness (−20 to −25 pp), or contradictions (up to −40 pp; GPT-4 drops from 73.8% to 6.7%) · `https://arxiv.org/abs/2507.20439` · accessed 2026-10-30 · Larbi et al. (Jul 2025) · **confidence: high**.
4. **Over 60% of long-horizon agent failures stem from instruction-following / misinterpreting requirements rather than syntax or technical errors:** SWE-EVO benchmark on realistic software evolution tasks · `https://arxiv.org/abs/2512.18470` · accessed 2026-10-30 · Le et al. (Dec 2025 / 2026) · **confidence: high**.
5. **LLM-generated `AGENTS.md` files slightly degrade task success (−0.5% to −2%) while increasing token/inference cost (+20% to +23%); human-written curated convention files yield +4%:** Evaluation on SWE-bench Lite (300 tasks) and AGENTbench (138 tasks) · `https://arxiv.org/abs/2602.11988` · accessed 2026-10-30 · Gloaguen et al., ETH Zurich / LogicStar (Feb 2026) · **confidence: high**.
6. **Agentic PRs exhibit a 27.67% merge conflict rate across 142K agentic PRs in 59K repositories:** Large-scale empirical study of parallel agentic pull requests · `https://arxiv.org/abs/2605.01160` / AgenticFlict · accessed 2026-10-30 · 2026 · **confidence: high**.
7. **"Workslop" (AI-generated output that looks complete but requires ~2 hours of human rework per instance):** Coined by BetterUp Labs + Stanford Social Media Lab; 41% of knowledge workers report receiving it · `https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity` · accessed 2026-10-30 · Harvard Business Review (Sep 2025) · **confidence: high**.

### Inference
- **Pedagogical impact on Units 1.4, 2.1, and 2.2:**
  - The ETH Zurich paper (`arXiv:2602.11988`) is a crucial counter-intuitive teaching point for **Unit 1.4 (Harness Engineering)**: running `/init` to auto-generate a bloated `CLAUDE.md` or `AGENTS.md` wastes 20%+ tokens and hurts accuracy. Context files must be **short, human-curated, and restricted to non-obvious build/test/architecture invariants**.
  - The METR RCT + Larbi et al. + AgenticFlict numbers anchor **Unit 2.2 (Estimación, impacto y planning)**: coding speed is not delivery speed; review time, integration conflicts (when running parallel agents), and specification clarity dominate total lead time.

---

## 2. Module 1 Tooling & .NET/Azure Verification

### 2.1 Unit 1.1 — Diseño (UI Prototyping & Design Systems)
#### Facts (Sourced)
- **Figma Make (`figma.com/make`):** Figma's prompt-to-app / design-to-functional-prototype tool inside Figma · `https://www.figma.com/make/` · accessed 2026-10-30 · active 2025–2026 · **confidence: high**.
- **Vercel v0 (`v0.dev` / `v0.app`):** Generative UI system outputting React/Next.js + Tailwind + shadcn/ui components · `https://v0.dev/` · accessed 2026-10-30 · active 2026 · **confidence: high**.
- **Lovable (`lovable.dev`):** Full-stack prompt-to-UI/app builder (React/Vite/Tailwind + Supabase integration, GitHub two-way sync) · `https://lovable.dev/` · accessed 2026-10-30 · active 2026 · **confidence: high**.
- **Google Stitch (`stitch.withgoogle.com`):** Google Labs tool (launched at Google I/O 2025, powered by Gemini) that generates UI designs and frontend code from text prompts, sketches, or screenshots, with export to Figma and code · `https://stitch.withgoogle.com/` · accessed 2026-10-30 · active 2025–2026 · **confidence: high**.
- **Claude Artifacts:** Interactive HTML/React/SVG/Mermaid rendering side-by-side in Claude · `https://support.anthropic.com/` · accessed 2026-10-30 · active 2026 · **confidence: high**.

#### Inference (.NET + Azure Fit)
- Every tool in Unit 1.1 outputs **HTML/Tailwind or React/TypeScript**, **not** native Blazor Razor (`.razor`) or XAML/MAUI out of the box.
- In a **.NET + Azure** consultancy, there are two realistic production patterns to teach in the Unit 1.1 handoff block:
  1. **SPA + ASP.NET Core Web API:** Keep the React/Next.js/Tailwind output from v0/Lovable/Stitch and bind it to an ASP.NET Core Minimal API via a generated OpenAPI client.
  2. **Design System / HTML-to-Blazor Conversion:** Export clean HTML + CSS/Tailwind design tokens from Stitch/v0/Figma MCP and use the coding agent (Unit 1.2/1.4) to translate the markup into reusable **Blazor Server / Blazor WebAssembly (`.razor`)** components or Razor Pages.
- Failing to warn .NET developers that UI generators speak React/Tailwind by default causes friction in the workshop; making the **OpenAPI contract + Blazor/React handoff** explicit turns it into a strength.

---

### 2.2 Unit 1.2 — Herramientas de Desarrollo (IDEs & Coding Assistants)
#### Facts (Sourced)
- **GitHub Copilot in Visual Studio & VS Code (C# Dev Kit):** First-class Microsoft integration for .NET, including Copilot Edits / Agent Mode in Visual Studio 2022 (17.13+) & VS Code, slash commands, `#file`/`#solution` context, custom instructions (`.github/copilot-instructions.md`), and .NET profiler/debugger assistance · `https://learn.microsoft.com/en-us/visualstudio/ide/visual-studio-github-copilot-chat` · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.
- **JetBrains Rider (AI Assistant & Junie):** JetBrains Rider is a leading cross-platform .NET IDE; includes JetBrains AI Assistant and **Junie** (JetBrains' coding agent), plus support for GitHub Copilot and Claude Agent plugins · `https://www.jetbrains.com/rider/` and `https://www.jetbrains.com/junie/` · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.
- **Cursor (`cursor.com`) & Windsurf (`windsurf.com`):** VS Code forks supporting C# via OpenVSX / Muhammadsammy C# / DotRush extensions, `.cursor/rules/*.mdc`, and multi-file agent mode · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.

#### Inference (.NET + Azure Fit)
- **Critical correction to Max's v1:** Max's Unit 1.2 lists *"Cursor, Windsurf, GitHub Copilot, JetBrains AI, Claude Code, Codex"*, without mentioning **Visual Studio** or **JetBrains Rider** vs. VS Codeforks. In a .NET consultancy, many senior backend engineers live in **Visual Studio** or **JetBrains Rider** because of Roslyn refactoring, solution-wide analysis, and MSBuild/NuGet debugging, whereas Cursor/Windsurf cannot legally run the proprietary Microsoft `ms-dotnettools.csdevkit` extension (they rely on open-source LSP alternatives like DotRush or OmniSharp).
- Unit 1.2 must explicitly compare the **.NET IDE trade-off**: Visual Studio + Copilot Agent Mode vs. Rider + AI/Copilot vs. VS Code / Cursor + CLI Harness (Claude Code / Codex).

---

### 2.3 Unit 1.3 — Agentes, Skills y SDKs en .NET / Azure
#### Facts (Sourced)
- **Agent Skills Open Standard (`SKILL.md`):** Originated by Anthropic (`anthropics/skills`, 185.2k stars, pushed 2026-10-28) and standardized at `agentskills/agentskills` (`https://github.com/agentskills/agentskills`, 26.8k stars, specification at `https://agentskills.io`). A skill is a folder containing `SKILL.md` (YAML frontmatter `name`, `description` + Markdown instructions) plus optional `scripts/`, `references/`, `assets/` loaded on demand (progressive disclosure) · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.
- **Spec Kit & MCP C# SDK now natively consume `SKILL.md`:** Verified in `github/spec-kit` v1.2.5 README (uses agent skills syntax) and `modelcontextprotocol/csharp-sdk` v2.3.0 README (`ModelContextProtocol.Extensions.Skills` NuGet package for serving/consuming Agent Skills with verifiable file manifests) · `https://github.com/modelcontextprotocol/csharp-sdk` · accessed 2026-10-30 · v2.3.0 (2026-10-20) · **confidence: high**.
- **`Microsoft.Extensions.AI` (NuGet):** Official .NET unified abstraction library (`IChatClient`, `IEmbeddingGenerator`, `AIFunctionFactory`, middleware/telemetry pipeline) across Azure OpenAI, OpenAI, Ollama, and Anthropic connectors. Part of `dotnet/extensions` · `https://www.nuget.org/packages/Microsoft.Extensions.AI` and `https://github.com/dotnet/extensions` · accessed 2026-10-30 · **v10.11.0 (released 2026-10-15)** · **confidence: high**.
- **Microsoft Agent Framework (`Microsoft.Agents.AI` on NuGet):** Microsoft's official open-source agent and multi-agent workflow framework for **.NET and Python** (`microsoft/agent-framework`, 14.4k stars, pushed 2026-10-30), unifying **Semantic Kernel** (`Microsoft.SemanticKernel` v1.81.0) and **AutoGen** into a single production SDK with native support for **Azure AI Foundry Agent Service**, MCP, and Agent-to-Agent (A2A) · `https://github.com/microsoft/agent-framework` and `https://www.nuget.org/packages/Microsoft.Agents.AI` · accessed 2026-10-30 · **NuGet `Microsoft.Agents.AI` v1.27.0 (Oct 2026)** · **confidence: high**.
- **Claude Agent SDK & OpenAI Agents SDK:**
  - `anthropics/claude-agent-sdk-python` (`v0.2.175`, 2026-10-30, 8.4k stars) and TypeScript equivalent.
  - `openai/openai-agents-python` (`v0.24.0`, 2026-10-15, 30.4k stars) and JS equivalent.
  - Neither provides a first-party C# Agent SDK (though both expose standard REST/OpenAI-compatible or C# client SDKs for raw model calls).

#### Inference (.NET + Azure Fit)
- **Major gap in Max's v1 Unit 1.3:** The final block of 1.3 says *"Introducción a Claude Agent SDK y OpenAI Agents SDK para agentes propios."* For a **.NET + Azure** audience (`D-014`), teaching only Python/TS SDKs while omitting **`Microsoft.Extensions.AI` (`IChatClient`)**, **Microsoft Agent Framework (`Microsoft.Agents.AI`)**, and **Azure AI Foundry Agent Service** is a critical mismatch.
- **Fix for v2:** Reframe the SDK block around **`Microsoft.Extensions.AI` + `Microsoft.Agents.AI` (with Azure AI Foundry)** as the primary .NET implementation, while contrasting it with Claude Agent SDK and OpenAI Agents SDK for polyglot/Python services.

---

### 2.4 Unit 1.4 — Harness Engineering (Claude Code, Codex, Devin)
#### Facts (Sourced)
- **Claude Code (`anthropics/claude-code`):** Terminal, IDE (VS Code / JetBrains), Desktop, and Web/Cloud coding harness; supports `CLAUDE.md`, auto-memory, slash commands, subagents, `SKILL.md` skills, lifecycle hooks (`PreToolUse`, `PostToolUse`, `Stop`, etc.), permission modes, Plan Mode, and headless CI (`claude -p`) · `https://github.com/anthropics/claude-code` · accessed 2026-10-30 · **v2.1.314 (released 2026-10-30, 154.0k stars)** · **confidence: high**.
- **OpenAI Codex (`openai/codex`):** Open-source Rust-based local CLI (`codex`) + Codex Cloud asynchronous software engineering agent; reads `AGENTS.md` natively, supports sandboxed execution (Seatbelt on macOS, Landlock/seccomp/containers on Linux), approval levels, parallel tasks, and GitHub PR review · `https://github.com/openai/codex` · accessed 2026-10-30 · **rust-v0.166.0 (released 2026-10-29, 131.9k stars)** · **confidence: high**.
- **Devin (`devin.ai`):** Cloud autonomous agent by Cognition; provides isolated cloud VM sessions, Knowledge (auto-recalled repo tips), Playbooks (reusable macros/workflows), Slack/Jira/Linear/GitHub/Azure DevOps integrations, and **DeepWiki** (`deepwiki.com` / internal repo wiki indexing) · `https://docs.devin.ai/` · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.
- **`AGENTS.md` vs. `CLAUDE.md` Interoperability Gotcha:** `AGENTS.md` is stewarded by the Agentic AI Foundation under the Linux Foundation (Dec 2025, `https://agents.md/`) and read natively by Codex, GitHub Copilot, Cursor, Windsurf, Gemini CLI, and Amp. **Claude Code does NOT read `AGENTS.md` natively** (tracked in `https://github.com/anthropics/claude-code/issues/34235`); cross-harness repos must place the canonical rules in `AGENTS.md` and create a 1-line `CLAUDE.md` containing `@AGENTS.md` (or a symlink) · accessed 2026-10-30 · **confidence: high**.

#### Inference (.NET + Azure Fit)
- In a .NET repository, **Harness Engineering** becomes concrete when hooks and verification loops invoke the .NET CLI:
  - `PostToolUse` hook running `dotnet format --verify-no-changes` or `dotnet build --no-restore -v q` on edited `.cs` files.
  - Giving the agent deterministic CLI test feedback (`dotnet test --filter FullyQualifiedName~... --no-build`) so it doesn't recompile the entire solution on every turn.
  - Documenting the `@AGENTS.md` pattern in `CLAUDE.md` so a team where half the developers use GitHub Copilot/Codex and half use Claude Code shares a single source of truth.

---

### 2.5 Unit 1.5 — Model Context Protocol (MCP) in .NET & Azure
#### Facts (Sourced)
- **Official MCP C# SDK (`modelcontextprotocol/csharp-sdk`):** Co-maintained with Microsoft. Provides NuGet packages:
  - `ModelContextProtocol` (stdio servers/clients, DI & `Microsoft.Extensions.Hosting` integration, `[McpServerToolType]` and `[McpServerTool]` attributes)
  - `ModelContextProtocol.AspNetCore` (Streamable HTTP servers hosted in ASP.NET Core)
  - `ModelContextProtocol.Core` (low-level minimal dependencies)
  - `ModelContextProtocol.Extensions.Apps`, `ModelContextProtocol.Extensions.Skills`, `ModelContextProtocol.Extensions.Tasks`
  · `https://github.com/modelcontextprotocol/csharp-sdk` and `https://www.nuget.org/packages/ModelContextProtocol` · accessed 2026-10-30 · **v2.3.0 (released 2026-10-20, 4.6k stars)** · **confidence: high**.
- **Official Microsoft & Azure MCP Servers (`microsoft/mcp` & `Azure/azure-mcp`):** Official catalog and implementation of Azure MCP servers (exposing Azure Resource Manager, Azure Storage, Cosmos DB, Azure Monitor/App Insights, Azure DevOps, etc. to MCP clients) · `https://github.com/microsoft/mcp` (3.8k stars, pushed 2026-10-30) and `https://github.com/Azure/azure-mcp` · accessed 2026-10-30 · **confidence: high**.

#### Inference (.NET + Azure Fit)
- **Critical correction to Max's v1 Unit 1.5:** Max's draft states: *"Crear un servidor MCP simple que exponga una API interna, con el SDK de TypeScript o Python."*
  - Why force a .NET consultancy to switch to Python or TypeScript when **`ModelContextProtocol` v2.3.0 on NuGet** lets them build a stdio or ASP.NET Core MCP server in ~25 lines of C# using standard `Host.CreateApplicationBuilder` and `[McpServerTool]` attributes?
  - Furthermore, in Unit 1.5's "existing MCP servers" block, we should add the **Azure MCP Server** (`microsoft/mcp`) and **Azure DevOps / GitHub MCP** alongside DB and browser MCPs.

---

## 3. Module 2 SDD Taxonomy & Frameworks Verification

### Facts (Sourced)
1. **SDD Taxonomy (*Spec-first*, *Spec-anchored*, *Spec-as-source*):** Defined by Birgitta Böckeler (Thoughtworks Distinguished Engineer) on Martin Fowler's site in *"Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"* · `https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html` · accessed 2026-10-30 · Oct 2025 · **confidence: high**.
   - *Spec-first:* Spec written before coding a task, then discarded or allowed to drift.
   - *Spec-anchored:* Spec lives in the repo alongside code and evolves across features (the realistic enterprise sweet spot).
   - *Spec-as-source:* Humans only edit the spec; code is treated strictly as a generated build artifact (explored by Tessl; high friction for complex brownfield systems).
2. **GitHub Spec Kit (`github/spec-kit`):** Official GitHub open-source SDD toolkit. Installed via `uv tool install specify-cli` and initialized with `specify init <project> --integration <copilot|claude|codex|...>`.
   - Core SDD skills invoked in the agent chat: `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, `/speckit-converge` (plus `/speckit-clarify`, `/speckit-analyze`, `/speckit-checklist`).
   - Also bundles extensions for **Bug fixing** (`specify extension add bug` -> `/speckit-bug-assess`, `/speckit-bug-fix`, `/speckit-bug-test`) and **Idea assessment** (`specify extension add assess`).
   - Supports **Presets**, **Extensions**, **Workflows**, and **Catalogs** for organizational standards.
   · `https://github.com/github/spec-kit` · accessed 2026-10-30 · **v1.2.5 (released 2026-10-28, 144.1k stars)** · **confidence: high**.
3. **OpenSpec (`Fission-AI/OpenSpec`):** Lightweight, **brownfield-first** SDD framework (`npm install -g @fission-ai/openspec@latest` or `brew install openspec`; `openspec init`).
   - Separates current system truth (`openspec/specs/`) from proposed delta changes (`openspec/changes/<change-name>/` containing `proposal.md`, delta `specs/` with `ADDED/MODIFIED/REMOVED Requirements`, `design.md`, and `tasks.md`).
   - Commands: `/opsx:explore`, `/opsx:propose <name>`, `/opsx:apply`, `/opsx:archive` (merges deltas into `openspec/specs/`). Also supports multi-repo **Stores** (beta).
   · `https://github.com/Fission-AI/OpenSpec` · accessed 2026-10-30 · **v1.15.0 (released 2026-10-24, 73.5k stars)** · **confidence: high**.
4. **AWS Kiro (`kiro.dev`):** Agentic IDE and CLI built on Code OSS by AWS. Structures work into `.kiro/specs/<feature>/` (`requirements.md` using EARS notation `WHEN... THE SYSTEM SHALL...`, `design.md`, `tasks.md`), event-driven **Agent Hooks** (`.kiro/hooks/`), and **Steering** files (`.kiro/steering/`) · `https://kiro.dev/` · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.
5. **BMAD Method (`bmad-code-org/BMAD-METHOD`):** Role-based agile AI-driven development framework (Analyst, PM, Architect, Scrum Master, Dev, QA personas + workflows). Ships stable **v6.12.4** (2026-10-14) and preview **v7** · `https://github.com/bmad-code-org/BMAD-METHOD` · accessed 2026-10-30 · **v6.12.4 (54.8k stars)** · **confidence: high**.
6. **Tessl (`tessl.io`):** Spec-centric platform combining the **Tessl Framework** (spec-anchored / spec-as-source) and the **Tessl Spec Registry** (`tessl.io/registry`), a package manager of versioned library/framework usage specs ("tiles") exposed via MCP to prevent API hallucinations · `https://tessl.io/` · accessed 2026-10-30 · current Oct 2026 · **confidence: high**.

### Inference (Corrections & Improvements for Unit 2.4)
- **Correction 1 (Spec Kit commands):** Max's v1 lists *"comandos specify, plan, tasks e implement"*. In Spec Kit v1.2.5, the CLI binary is `specify` (`specify init`, `specify check`, `specify extension`), while the agent chat skills are `/speckit-constitution`, `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, and `/speckit-converge` (plus the `bug` extension). Adding `/speckit-converge` (which audits implementation drift against the spec) and `specify extension add bug` makes the lesson current and practical.
- **Correction 2 (Greenfield vs. Brownfield decision criterion):** Consultancy engineers spend 80%+ of their billable hours in **existing (brownfield)** enterprise .NET systems, not greenfield toys.
  - **GitHub Spec Kit** shines for structured greenfield features or full module builds (and now hasPresets/Catalogs for enterprise governance).
  - **OpenSpec** (`/opsx:explore` -> `/opsx:propose` -> `/opsx:apply` -> `/opsx:archive`) shines for **brownfield iterative changes** because it models *deltas* (`ADDED/MODIFIED/REMOVED`) and merges them back into living specs on archive.
  - Giving teams a crisp decision matrix (**Spec Kit vs. OpenSpec vs. Kiro vs. BMAD vs. Tessl**) grounded in greenfield vs. brownfield and IDE constraints makes Unit 2.4 immediately actionable for Module 3.

---

## 4. Open Items (Unknowns)
- Whether the target Buenos Aires consultancy uses **GitHub Enterprise** or **Azure DevOps** as its primary ALM/CI platform (`Q-002`). Until known, examples should show GitHub Actions / GitHub Spec Kit as primary with explicit Azure DevOps (Work Items / Pipelines / `az boards`) callouts.
- Which frontend stack the consultancy pairs most often with .NET (`Blazor`, `React`, or `Angular`). Both React+ASP.NET Core OpenAPI and Blazor are supported in our v2 design.
