#!/usr/bin/env bash
# Da narração à prévia em um comando (ESTRUTURA.md, seção 11, passos 5 a 7), para quando o
# roteiro já foi aprovado e as cenas (composicao/cenas/bloco-N.html) existem.
# Uso: ./scripts/previa.sh [--estimar] videos/AAAA-MM-DD-slug
#   --estimar  sem voz: tempos estimados (quando o edge-tts não alcança a internet)
#
# Passos: texto da narração (roteiro.py) → narração e tempos (narrar.py) → composição
# (montar.py) → volume (ajustar-volume.sh) → check do HyperFrames → previa.mp4.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ESTIMAR=""
if [ "${1:-}" = "--estimar" ]; then
  ESTIMAR="--estimar"
  shift
fi
if [ $# -ne 1 ] || [ ! -d "$1" ]; then
  echo "Uso: $0 [--estimar] videos/AAAA-MM-DD-slug" >&2
  exit 1
fi
PASTA="$(cd "$1" && pwd)"
cd "$RAIZ"

PY=""
for candidato in python3 python; do
  if command -v "$candidato" >/dev/null 2>&1 &&
     "$candidato" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
    PY="$candidato"
    break
  fi
done
[ -n "$PY" ] || { echo "Python 3.11+ não encontrado." >&2; exit 1; }

passo() { printf '\n== %s\n' "$*"; }

passo "1. Texto da narração"
"$PY" scripts/roteiro.py texto "$PASTA"

passo "2. Narração ${ESTIMAR:+(tempos estimados, sem voz)}"
"$PY" scripts/narrar.py $ESTIMAR "$PASTA"

passo "3. Composição"
"$PY" scripts/montar.py "$PASTA"

if [ -z "$ESTIMAR" ]; then
  passo "4. Volume da narração"
  ./scripts/ajustar-volume.sh "$PASTA"
fi

passo "5. Check do HyperFrames"
./scripts/hf.sh "$PASTA" check --json 2>/dev/null >"$PASTA/composicao/.check.json" || true
node -e '
  const r = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
  for (const v of Object.values(r)) {
    for (const f of (v && v.findings) || []) {
      if (f.severity === "error") console.log(`  ERRO  ${f.code}: ${f.message}`);
    }
  }
  process.exit(r.ok ? 0 : 1);
' "$PASTA/composicao/.check.json" || { echo "O check reprovou a composição (erros acima)." >&2; exit 1; }
rm -f "$PASTA/composicao/.check.json"
echo "  OK"

passo "6. Prévia"
./scripts/hf.sh "$PASTA" render --quality draft --output ../previa.mp4
echo
echo "Pronto: ${PASTA#"$RAIZ"/}/previa.mp4"
