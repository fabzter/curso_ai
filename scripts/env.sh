#!/usr/bin/env bash
# Shared paths/config for the curso_ai helper scripts. Source this; do not execute.
# Every path here was verified on 2026-10-30. If something moved, fix it HERE only.

export PROJECT_DIR="${PROJECT_DIR:-$HOME/Documents/curso_ai}"

# --- Google (gog CLI). Personal account only. Luca accounts were purged: never re-auth them.
export GOG_ACCOUNT="faboster@gmail.com"

# --- WhatsApp local bridge (lharries/whatsapp-mcp fork, launchd service com.fabzter.whatsapp-mcp-bridge)
export WA_STORE="$HOME/src/whatsapp-mcp/whatsapp-bridge/store"
export WA_MSG_DB="$WA_STORE/messages.db"      # chats, messages, reactions
export WA_DEV_DB="$WA_STORE/whatsapp.db"      # whatsmeow_contacts, whatsmeow_lid_map
export WA_API="http://localhost:8080"         # bridge REST (POST /api/download). NEVER use /api/send from this project.
export MAX_CHAT_JID="52399205003325@lid"      # Max Deboli 1:1 chat (resolved 2026-10-30). Decoy: 250800454512767@lid (1 msg only).
export COURSE_WINDOW_START="2026-10-13 00:00:00-06:00"  # chat before this date is unrelated/personal: do not ingest.

# --- Local ASR (transcribe.cpp, built 2026-10-30 at commit 5700f12)
export ASR_CLI="$HOME/src/transcribe.cpp/build/bin/transcribe-cli"
export ASR_NEMOTRON="$(ls "$HOME"/.cache/huggingface/hub/models--handy-computer--nemotron-3.5-asr-streaming-0.6b-gguf/snapshots/*/*.gguf 2>/dev/null | head -1)"
export ASR_PARAKEET="$(ls "$HOME"/.cache/huggingface/hub/models--handy-computer--parakeet-tdt-0.6b-v3-gguf/snapshots/*/*.gguf 2>/dev/null | head -1)"

# --- Knowledge vault (Obsidian, PARA). READ-ONLY unless Fab explicitly authorizes a write.
export VAULT_DIR="$HOME/Library/CloudStorage/GoogleDrive-faboster@gmail.com/My Drive/knowledge"
