#!/usr/bin/env bash
# Preflight: verifies every external dependency this project needs. Run at the start of each session.
# Read-only. Exit code = number of failed checks.
set -uo pipefail
source "$(dirname "$0")/env.sh"

fail=0
ok()   { printf '  [ OK ] %s\n' "$1"; }
bad()  { printf '  [FAIL] %s\n' "$1"; fail=$((fail+1)); }
chk()  { if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

echo "== gog (Google Drive/Docs)"
chk "gog binary"                          "command -v gog"
chk "gog account $GOG_ACCOUNT authorized" "gog auth list 2>&1 | grep -q '$GOG_ACCOUNT'"
chk "Drive reachable (readonly about)"    "gog --readonly -a $GOG_ACCOUNT drive ls --max 1"

echo "== WhatsApp bridge"
chk "bridge launchd service running"      "launchctl print gui/$(id -u)/com.fabzter.whatsapp-mcp-bridge | grep -q 'state = running'"
chk "messages.db readable"                "sqlite3 '$WA_MSG_DB' 'select count(*) from messages'"
chk "Max chat present ($MAX_CHAT_JID)"    "[ \"\$(sqlite3 '$WA_MSG_DB' \"select count(*) from messages where chat_jid='$MAX_CHAT_JID'\")\" -gt 0 ]"
chk "bridge REST answers on :8080"        "curl -s -m 3 -o /dev/null -w '%{http_code}' -X POST $WA_API/api/download -H 'Content-Type: application/json' -d '{}' | grep -qE '^(200|400|500)'"

echo "== Local ASR"
chk "transcribe-cli built"                "[ -x '$ASR_CLI' ]"
chk "Nemotron 3.5 streaming GGUF present" "[ -f '$ASR_NEMOTRON' ]"
chk "Parakeet TDT 0.6B v3 GGUF present"   "[ -f '$ASR_PARAKEET' ]"
chk "ffmpeg"                              "command -v ffmpeg"

echo "== Docs tooling"
chk "pandoc (docx -> md)"                 "command -v pandoc"
chk "firecrawl CLI (web research)"        "command -v firecrawl"

echo "== Knowledge vault (read-only)"
chk "vault dir readable"                  "ls '$VAULT_DIR/05_people' | grep -q 'Max'"
chk "obsidian-cli default vault = knowledge" "obsidian-cli print-default | grep -q 'knowledge$'"

echo
[ "$fail" -eq 0 ] && echo "ALL CHECKS PASSED" || echo "$fail CHECK(S) FAILED — see docs/05-TOOLING.md troubleshooting"
exit "$fail"
