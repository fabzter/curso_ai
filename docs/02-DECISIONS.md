# 02 — Decision log (append-only)

Format: `D-### · date · decision · why · who · reversible?`. To reverse a decision, add a new entry that supersedes it; never edit history.

| ID | Date | Decision | Why | By | Status |
|---|---|---|---|---|---|
| D-001 | 2026-10-30 | Project home is `~/Documents/curso_ai`. `AGENTS.md` is the canonical entry point (`CLAUDE.md` just imports it). All state lives in `docs/`; chat memory is not relied on. | Long-horizon, multi-agent, multi-session; Fab prefers explicit SPEC/PLAN/TODO/CONTEXT files. | Fab (request) + Antigravity | Active |
| D-002 | 2026-10-30 | Authoritative sources, in order: (1) WhatsApp chat with Max, course window ≥ 2026-10-13; (2) the Drive docs Max sends (currently S-03). Other sources (vault, web) support, never override. | Fab's explicit instruction. | Fab | Active |
| D-003 | 2026-10-30 | Voice notes are transcribed locally with **both** Nemotron 3.5 streaming and Parakeet TDT 0.6B v3 (transcribe.cpp) and reconciled by hand. | Fab asked for these models; 5-clip test showed they're complementary and each fails differently. | Antigravity (tested) | Active |
| D-004 | 2026-10-30 | Google access via `gog` with `--readonly`, account `faboster@gmail.com` only. | Fab: "use gog"; personal account is the only authorized one; no outbound writes without permission. | Fab + Antigravity | Active |
| D-005 | 2026-10-30 | Max chat before 2026-10-13 is excluded from the repo. | Unrelated personal content. | Antigravity (privacy default) — Fab may override | Active |
| D-006 | 2026-10-30 | Agent-facing docs in English; course deliverables in Spanish (register TBD, Q-011). Agents address Fab in English or Mexican Spanish, never voseo. | Fab's standing preference; audience is Spanish-speaking. | Antigravity from Fab's prefs | Active |
| D-007 | 2026-10-30 | Max's Temario v1 (S-03) is a **baseline hypothesis**, not a spec: LLM-generated, "solo un draft". Every tool/product claim in it must be verified (dated, sourced) before it reaches course material. | Evidence rules; tools in scope change monthly. | Antigravity | Active |
| D-008 | 2026-10-30 | Vault, Drive, and other repos are read-only for agents unless Fab authorizes a specific write. The Luca vault/creds are permanently off limits. | Fab's standing rules (no modification without permission; Luca purge). | Fab | Active |
