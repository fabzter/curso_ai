#!/usr/bin/env bash
# Hook PostToolUse y verificador determinista del Harness (.NET 10)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> [Harness Hook] 1/3 Verificando interoperabilidad AGENTS.md + CLAUDE.md..."
if [[ ! -f "CLAUDE.md" ]] || ! grep -q "@AGENTS.md" "CLAUDE.md"; then
  echo "❌ ERROR: Falta CLAUDE.md con el puente '@AGENTS.md' (Unidad 1.4)." >&2
  exit 1
fi

if grep -q "TODO (Fase 1" "AGENTS.md"; then
  echo "❌ ERROR: AGENTS.md todavía contiene el borrador autogenerado con 'TODO (Fase 1'." >&2
  exit 1
fi

LINE_COUNT="$(wc -l < AGENTS.md | tr -d ' ')"
if (( LINE_COUNT > 100 )); then
  echo "❌ ERROR: AGENTS.md tiene $LINE_COUNT líneas (máximo permitido: 100 líneas para evitar degradación de contexto)." >&2
  exit 1
fi

echo "==> [Harness Hook] 2/3 Compilando solución con TreatWarningsAsErrors=true..."
dotnet build GuardiaCloud.Sla.HarnessLab.sln --nologo -v q

echo "==> [Harness Hook] 3/3 Ejecutando Oráculo de Arquitectura (NetArchTest) y Tests de Integración..."
dotnet test GuardiaCloud.Sla.HarnessLab.sln --no-build --nologo -v q

echo "✅ [Harness Hook] Compilación, Harness y Oráculo en verde."
