#!/usr/bin/env bash
# Ajusta o volume da narração na composição para o vídeo final sair em −14 LUFS
# (ESTRUTURA.md, seção 8). Rode depois de montar a composição e antes da prévia.
# Uso: ./scripts/ajustar-volume.sh videos/AAAA-MM-DD-slug
#
# Usa o "normalize-audio" do HyperFrames, que grava o ganho no data-volume do
# <audio id="narracao"> do index.html. O edge-tts gera narração mono e o HyperFrames
# a toca nos dois canais, o que soma 3 dB no vídeo final; por isso, para narração
# mono, o alvo passado ao normalize-audio é −17 LUFS (medido: sai −14,1 no final).
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/ambiente.sh"

if [ $# -ne 1 ] || [ ! -d "$1" ]; then
  echo "Uso: $0 videos/AAAA-MM-DD-slug" >&2
  exit 1
fi
PASTA="$(cd "$1" && pwd)"
NARRACAO="$PASTA/narracao/narracao.mp3"
[ -f "$NARRACAO" ] || { echo "Não encontrei $NARRACAO" >&2; exit 1; }
grep -q 'id="narracao"' "$PASTA/composicao/index.html" 2>/dev/null ||
  { echo "O index.html precisa de <audio id=\"narracao\" src=\"narracao/narracao.mp3\" ...>" >&2; exit 1; }

CANAIS="$("$RAIZ/scripts/hf.sh" audio "$NARRACAO" --json 2>/dev/null |
  node -e 'console.log(JSON.parse(require("fs").readFileSync(0, "utf8")).items[0].channels)')"
ALVO=-14
[ "$CANAIS" = 1 ] && ALVO=-17

exec "$RAIZ/scripts/hf.sh" "$PASTA" normalize-audio --target narracao --lufs="$ALVO" --write
