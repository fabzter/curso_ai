#!/usr/bin/env bash
# Wrapper for the bidirectional course material pipeline:
#   ./scripts/course-sync.sh build          -> Regenerate all .md, .docx, and .pptx deliverables
#   ./scripts/course-sync.sh publish-vault  -> Publish all notes & .docx/.pptx attachments to the Obsidian `knowledge` vault
#   ./scripts/course-sync.sh status         -> Check if any .docx, .pptx, or Vault note was edited
#   ./scripts/course-sync.sh ingest         -> Extract diffs from edited .docx, .pptx, or Vault notes into curriculum/.ingested/
#   ./scripts/course-sync.sh ingest --apply -> Retroactively apply edits back into the repo's canonical documentation
#   ./scripts/course-sync.sh all            -> Run `build` + `publish-vault`
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CMD="${1:-status}"
shift || true

if [[ "$CMD" == "all" ]]; then
  python3 "$ROOT/scripts/course-pipeline.py" build
  python3 "$ROOT/scripts/course-pipeline.py" publish-vault
else
  python3 "$ROOT/scripts/course-pipeline.py" "$CMD" "$@"
fi
