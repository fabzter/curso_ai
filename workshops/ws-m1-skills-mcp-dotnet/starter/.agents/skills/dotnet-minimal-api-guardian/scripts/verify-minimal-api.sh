#!/usr/bin/env bash
# Verificador determinista de la Skill dotnet-minimal-api-guardian
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
SKILL_FILE="$ROOT_DIR/.agents/skills/dotnet-minimal-api-guardian/SKILL.md"
REF_FILE="$ROOT_DIR/.agents/skills/dotnet-minimal-api-guardian/references/rfc9457-catalogo-errores.md"

echo "==> Auditando Skill: $SKILL_FILE"

if [[ ! -f "$SKILL_FILE" ]]; then
  echo "❌ ERROR: No existe $SKILL_FILE" >&2
  exit 1
fi

if [[ ! -f "$REF_FILE" ]]; then
  echo "❌ ERROR: No existe el archivo de referencia $REF_FILE" >&2
  exit 1
fi

if grep -q "TODO (Fase 1" "$SKILL_FILE"; then
  echo "❌ ERROR: SKILL.md todavía contiene marcadores 'TODO (Fase 1'. Completá el frontmatter y las reglas en la Fase 1." >&2
  exit 1
fi

for required_term in "RFC 9457" "ProblemDetails" "errorCode" "TimeProvider" "references/rfc9457-catalogo-errores.md" "validate_rfc9457_contract"; do
  if ! grep -q "$required_term" "$SKILL_FILE"; then
    echo "❌ ERROR: SKILL.md no menciona el término obligatorio '$required_term'." >&2
    exit 1
  fi
done

echo "✅ SKILL.md cumple todas las invariantes de progressive disclosure y trazabilidad RFC 9457."
