#!/usr/bin/env bash
# Download + transcribe WhatsApp voice notes locally (no cloud).
# Usage: scripts/wa-transcribe.sh <message_id> [<message_id> ...]
# Chat is fixed to the Max chat. Raw audio stays in the bridge store (never copied into this repo).
# Output: sources/whatsapp/voice/<audio-filename>.{nemotron,parakeet}.txt  (+ printed to stdout)
#
# Model policy (verified 2026-10-30 on 5 clips; the models are COMPLEMENTARY, always run both and reconcile):
#   * Nemotron 3.5 ASR streaming: far better on Max's 48 s Rioplatense clip (voseo, "go", "call").
#                                 Weak at clip start: dropped/garbled first words on Fab's short clips
#                                 ("¿Qué onda, bro?" -> "Que donde habló"; "link please" -> "link lis").
#   * Parakeet TDT 0.6B v3:       better on short clips and English words, but FABRICATED English on the 48 s
#                                 Max clip ("It's very good to have a reunion this violence").
#   Rule: if they diverge on anything that matters (names, numbers, dates, decisions), flag it in the
#   source note; do not pick one silently. Transcripts are evidence, not ground truth.
set -euo pipefail
source "$(dirname "$0")/env.sh"
[ "$#" -ge 1 ] || { echo "usage: $0 <message_id>..." >&2; exit 2; }

OUT="$PROJECT_DIR/sources/whatsapp/voice"; TMP="${TMPDIR:-/tmp}/curso_ai_asr"
mkdir -p "$OUT" "$TMP"

for id in "$@"; do
  [[ "$id" =~ ^[A-Za-z0-9]+$ ]] || { echo "bad message id: $id" >&2; exit 2; }
  row="$(sqlite3 -separator '|' "$WA_MSG_DB" "SELECT filename, timestamp, is_from_me FROM messages WHERE id='$id' AND chat_jid='$MAX_CHAT_JID' AND media_type='audio'")"
  [ -n "$row" ] || { echo "no audio message $id in Max chat" >&2; continue; }
  IFS='|' read -r fname ts me <<<"$row"
  who=$([ "$me" = 1 ] && echo FAB || echo MAX)

  # Media download via the bridge's own documented REST endpoint (CDN tokens expire: do this early).
  src="$WA_STORE/$MAX_CHAT_JID/$fname"
  if [ ! -f "$src" ]; then
    resp="$(curl -s -m 90 -X POST "$WA_API/api/download" -H 'Content-Type: application/json' \
            -d "{\"message_id\":\"$id\",\"chat_jid\":\"$MAX_CHAT_JID\"}")"
    echo "$resp" | grep -q '"success":true' || { echo "download failed for $id: $resp" >&2; continue; }
  fi

  base="${fname%.*}"
  ffmpeg -y -loglevel error -i "$src" -ar 16000 -ac 1 "$TMP/$base.wav"
  # -o writes only the transcript text; more reliable than scraping stdout.
  "$ASR_CLI" -m "$ASR_NEMOTRON" -o "$OUT/$base.nemotron.txt" "$TMP/$base.wav" >/dev/null 2>&1
  "$ASR_CLI" -m "$ASR_PARAKEET" -o "$OUT/$base.parakeet.txt" "$TMP/$base.wav" >/dev/null 2>&1

  echo "### $ts  $who  ($id)"
  echo "NEMOTRON: $(cat "$OUT/$base.nemotron.txt")"
  echo "PARAKEET: $(cat "$OUT/$base.parakeet.txt")"
  echo
done
