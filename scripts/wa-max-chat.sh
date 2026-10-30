#!/usr/bin/env bash
# Print the Max Deboli chat (course window only by default), oldest -> newest.
# Usage: scripts/wa-max-chat.sh [since 'YYYY-MM-DD HH:MM:SS-06:00']
#   Default start = $COURSE_WINDOW_START (earlier messages are unrelated personal chat; do not ingest).
# Columns: timestamp | FAB/MAX | media_type | filename | message_id | content
# Voice notes show media_type=audio and empty content -> transcribe with scripts/wa-transcribe.sh <message_id>.
# NOTE: timestamps are ISO TEXT with -06:00 offset. Compare with ISO strings, never epoch.
set -euo pipefail
source "$(dirname "$0")/env.sh"
SINCE="${1:-$COURSE_WINDOW_START}"
sqlite3 -separator ' | ' "$WA_MSG_DB" \
  "SELECT timestamp,
          CASE is_from_me WHEN 1 THEN 'FAB' ELSE 'MAX' END,
          COALESCE(media_type,''), COALESCE(filename,''), id,
          replace(COALESCE(content,''), char(10), ' ⏎ ')
   FROM messages
   WHERE chat_jid='$MAX_CHAT_JID' AND timestamp >= '$SINCE'
   ORDER BY timestamp ASC;"
