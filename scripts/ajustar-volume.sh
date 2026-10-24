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

# O normalize-audio não sobe o ganho além do que os picos permitem (limitedBy: true-peak);
# nesse caso o vídeo sai mais baixo que −14 LUFS e o verificar.sh vai reprovar o final.
"$RAIZ/scripts/hf.sh" "$PASTA" normalize-audio --target narracao --lufs="$ALVO" --write --json 2>/dev/null |
  node -e '
    const r = JSON.parse(require("fs").readFileSync(0, "utf8"));
    if (!r.ok) { console.error("O normalize-audio falhou:", JSON.stringify(r)); process.exit(1); }
    const final = r.projectedLufs + (Number(process.argv[1]) === 1 ? 3 : 0);
    console.log(`Narração: ganho ${r.gainDb.toFixed(1)} dB, volume ${r.volume.toFixed(3)}, ` +
                `deve sair em ${final.toFixed(1)} LUFS no vídeo.`);
    if (r.limitedBy === "true-peak" && final < -15) {
      console.log("Aviso: os picos da narração limitaram o ganho; o vídeo vai sair abaixo de −14 LUFS " +
                  "(ok para prévia; para o final, a narração precisa de menos picos).");
    }
  ' "$CANAIS"
