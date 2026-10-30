#!/usr/bin/env bash
# Fetch a Drive file (docx / Google Doc) with gog (READ-ONLY) and convert it to Markdown.
# Usage: scripts/drive-fetch.sh <fileId> <short-name> [subdir under sources/]
#   -> sources/<subdir>/<YYYY-MM-DD>_<short-name>.docx  +  .md   (date = Drive modifiedTime, UTC->local date)
# Default subdir: max-docs. Existing files are never overwritten: a new modifiedTime gives a new dated file (= version history).
# Native Google Docs are exported as docx first (gog exports via Drive). The fileId is the bit after /d/ in the URL.
set -euo pipefail
source "$(dirname "$0")/env.sh"
[ "$#" -ge 2 ] || { echo "usage: $0 <fileId> <short-name> [subdir]" >&2; exit 2; }
ID="$1"; NAME="$2"; SUB="${3:-max-docs}"
DEST="$PROJECT_DIR/sources/$SUB"; mkdir -p "$DEST"

META="$(gog --readonly -a "$GOG_ACCOUNT" drive get "$ID" -j)"
MIME="$(python3 -c 'import sys,json; print(json.load(sys.stdin)["file"]["mimeType"])' <<<"$META")"
MOD="$(python3 -c 'import sys,json,datetime as d; t=json.load(sys.stdin)["file"]["modifiedTime"]; print(d.datetime.fromisoformat(t.replace("Z","+00:00")).astimezone().strftime("%Y-%m-%d"))' <<<"$META")"
TITLE="$(python3 -c 'import sys,json; print(json.load(sys.stdin)["file"]["name"])' <<<"$META")"
BASE="$DEST/${MOD}_${NAME}"

FMT=()
case "$MIME" in application/vnd.google-apps.document) FMT=(--format docx);; esac
gog --readonly -a "$GOG_ACCOUNT" drive download "$ID" ${FMT[@]+"${FMT[@]}"} --out "$BASE.docx"   # ${arr[@]+...}: macOS bash 3.2 + set -u
pandoc -t gfm --wrap=none "$BASE.docx" -o "$BASE.md"
echo "title: $TITLE | mime: $MIME | modified(local date): $MOD"
echo "wrote: $BASE.docx  $BASE.md"
