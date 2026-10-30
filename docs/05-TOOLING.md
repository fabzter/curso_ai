# 05 — Tooling: verified access paths (all verified 2026-10-30 by `scripts/check-access.sh`, 15/15 OK)

Run `./scripts/check-access.sh` first. Paths/IDs live in `scripts/env.sh`. Rule: don't call a path broken from one failed probe.

## 1. Google Drive / Docs — `gog` (v0.46.0, Homebrew `/opt/homebrew/bin/gog`)
- Only authorized account: **`faboster@gmail.com`** (Drive, Docs, Sheets, Gmail, Calendar, … scopes). Keychain backend. No Luca account exists (purged; **never re-auth**).
- Always: `gog --readonly -a faboster@gmail.com …`. Metadata: `gog --readonly -a faboster@gmail.com drive get <fileId> -j`.
- Download: `gog … drive download <fileId> --out <path>` (native Google Docs need `--format docx|pdf|…`). Wrapper: `scripts/drive-fetch.sh`.
- Max's file is a **.docx in Drive**, so `gog docs cat` is not the right tool; Drive download + `pandoc -t gfm` is.
- Need a Google REST surface gog doesn't wrap (tab-scoped Docs edits…)? `~/.agents/skills/gog-api-token/bin/gog-token.sh` mints a token. Its SKILL.md mentions `~/.Codex/skills/…`: **that path doesn't exist**; use the `~/.agents/skills/…` path. Writes need Fab's approval.
- If `gog` fails with `invalid_grant`, report scoped ("faboster@gmail.com: invalid_grant"), see `~/.codex/skills/gog-oauth-refresh-token-expiry` and ask Fab; don't browser-automate his desktop.

## 2. WhatsApp — local bridge (personal account; fragile; read-only for us)
- Service: launchd `com.fabzter.whatsapp-mcp-bridge` (check: `whatsapp-mcp-status`; restart: `whatsapp-mcp-restart`). Repo `~/src/whatsapp-mcp` (branch `local/whatsmeow-compat`).
- DBs: `~/src/whatsapp-mcp/whatsapp-bridge/store/messages.db` (chats/messages/reactions) and `whatsapp.db` (contacts, `whatsmeow_lid_map`).
- **This Antigravity session has no WhatsApp MCP tools**; use SQL + the bridge REST API. Other agents (Claude Desktop, Cursor, Codex, Hermes) have the MCP server wired in, but per the skill the MCP lookup tools often return empty: **SQL first**.
- Max = `52399205003325@lid` (device store also has phone-JID rows; a second "Max Deboli" contact `250800454512767@lid` has 1 unrelated msg; "Maxx/Alberto" is a different person). Don't take the first LIKE hit; pick the JID with the active conversation.
- `messages.timestamp` is **ISO TEXT with -06:00**, not epoch. Filter with ISO strings. `is_from_me=1` = Fab.
- MCP/UI labels are useless for attribution (owner LID shown everywhere); filter by `chat_jid`.
- Media: `POST http://localhost:8080/api/download {"message_id","chat_jid"}` → file lands in `store/<jid>/`. Recent media works; old CDN tokens expire (download voice notes promptly). Never call `/api/send`.
- Skills: `~/.hermes/skills/mcp/whatsapp-mcp-local-bridge/SKILL.md` (authoritative), `~/.hermes/skills/whatsapp-chat-export/` (HTML export if ever needed).

## 3. Local speech-to-text (requested: Nemotron Streaming 3.5 or Parakeet TDT 0.6B v3)
- Both models are on disk as GGUF (HF cache, from `handy-computer/*-gguf`, Q8_0; also used by the Handy app). Runtime: **`transcribe.cpp`** built from source on 2026-10-30:
  `~/src/transcribe.cpp/build/bin/transcribe-cli` (commit `5700f12`, Metal backend, 14-89× realtime on this Mac). No cloud.
- Use `scripts/wa-transcribe.sh <message_id>…` (downloads, converts to 16 kHz mono wav, runs **both** models, writes `sources/whatsapp/voice/*.{nemotron,parakeet}.txt`).
- Manual: `ffmpeg -i x.ogg -ar 16000 -ac 1 x.wav && transcribe-cli -m <model.gguf> -o out.txt x.wav` (`-o` writes just the text; `-q` + stdout scraping was unreliable with Nemotron).
- **Quality finding (5 clips):** complementary. Nemotron far better on Max's 48 s clip (Rioplatense, voseo, "go"/"call"); Parakeet hallucinated English there but is better on Fab's short clips and Nemotron garbles the first words of short clips. Always run both and reconcile; flag divergences on names/numbers/dates.
- An extra Nemotron ONNX copy exists inside another app's data dir (`corespeechd`); we don't use it.
- Fallback: `whisper-cli` + `~/.cache/whisper/ggml-large-v3-turbo.bin` (see `~/.hermes/skills/media/local-audio-enhance-transcribe`).

## 4. Knowledge vault (Obsidian, PARA) — READ-ONLY by default
- **One live vault: `knowledge`** → `~/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge` (folders `00_inbox … 06_maps, 99_attachments`). Plain `ls`/`cat` work today.
- ⚠️ **STALE SKILL:** `~/.agents/skills/obsidian-cli/SKILL.md` (and the `~/.claude/skills` copy) describe the purged `knowledge_luca` vault. Do not follow it. Current guidance: `~/.hermes/skills/note-taking/obsidian-cli/SKILL.md` + `~/.hermes/skills/personal-vault-para`.
- Two binaries are named `obsidian-cli`: Homebrew legacy v0.2.3 (default vault verified = `knowledge`) and the official app-bundled one; legacy `create` truncates content at `&` and may be a silent no-op. If a vault write is ever authorized: use the official CLI, avoid `&` in names, and verify by readback.
- Proposed (needs Fab's OK, Q-009): a project note under `01_projects/` linking to this repo.

## 5. Web research
- `search_web` (built into this agent), `firecrawl` CLI (`/Users/fabzter/.nvm/versions/node/v20.20.2/bin/firecrawl`; skills `~/.agents/skills/firecrawl-*`), `curl` for public pages (HF model cards worked).
- Search-engine summaries can be wrong: for tool docs/model cards, fetch the primary page. (Example: a web summary of how to run the GGUF models was vague; the HF model card gave the real runtime.)

## 6. Other
- `pandoc` (docx→md), `ffmpeg`, `sqlite3`, `uv`, Go, cmake present. `herdr` (terminal multiplexer; env `HERDR_*` set) — only use if Fab asks (skill: `~/.agents/skills/herdr`).

## Troubleshooting quick table
| Symptom | First check |
|---|---|
| Bridge not running / no new messages | `whatsapp-mcp-status`, `whatsapp-mcp-qr 40` (re-pair needs Fab's phone), log `~/Library/Logs/whatsapp-mcp-bridge.*.log` |
| `download` HTTP 403 | Old media (expired token) or the known URL-query bug; see skill §"download_media fails with HTTP 403" |
| gog `invalid_grant` | Re-auth is Fab's action; report which account |
| Vault `Operation not permitted`/`deadlock avoided` | macOS TCC / Drive materialization, see Hermes obsidian-cli skill; read by absolute path |
| ASR empty output | use `-o file`; ensure 16 kHz mono wav; models: `ls ~/.cache/huggingface/hub/models--handy-computer--*` |
