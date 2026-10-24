#!/usr/bin/env bash
# Roda o HyperFrames (ESTRUTURA.md, seção 6).
# Uso: ./scripts/hf.sh videos/AAAA-MM-DD-slug <comando> [opções...]   na composição de um vídeo
#      ./scripts/hf.sh <comando> [opções...]                          comandos gerais (doctor, browser, docs)
#   ex.: ./scripts/hf.sh videos/2026-10-26-teste check --json
#        ./scripts/hf.sh videos/2026-10-26-teste render --quality draft --output ../previa.mp4
#        ./scripts/hf.sh doctor
#
# O HyperFrames só enxerga arquivos a partir da pasta da composição, então antes de
# cada comando este script liga dentro de composicao/ as pastas compartilhadas:
#   assets/ e componentes/ (do projeto) e narracao/ (do vídeo).
# No Windows sem permissão para links simbólicos, ele copia as pastas e refaz a cópia
# a cada execução (marcadas com .copia-gerada). Nunca edite essas cópias.
#
# Usa sempre o CLI e o FFmpeg nas versões fixas do package.json (scripts/ambiente.sh).
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/ambiente.sh"

erro() {
  echo "ERRO: $*" >&2
  exit 1
}

if [ $# -lt 1 ]; then
  echo "Uso: $0 [videos/AAAA-MM-DD-slug] <comando> [opções...]" >&2
  exit 1
fi

[ -e "$HF" ] || erro "HyperFrames não instalado. Rode ./scripts/instalar.sh"

PASTA=""
if [ -d "$1" ]; then
  PASTA="$(cd "$1" && pwd)"
  shift
  [ $# -ge 1 ] || erro "falta o comando do HyperFrames depois da pasta do vídeo."
elif [[ "$1" == */* ]]; then
  erro "pasta do vídeo não encontrada: $1"
fi

# Comandos que publicam, usam nuvem ou conta, mandam dados para fora ou mudam
# versões fixas: fora das regras do canal (ESTRUTURA.md, seção 12).
case "$1" in
  publish | cloud | lambda | cloudrun | auth | feedback | usage | upgrade | skills | telemetry | open | catch-up | capture)
    erro "'hyperframes $1' não é usado neste projeto (ESTRUTURA.md, seção 12)." ;;
esac

if [ -z "$PASTA" ]; then
  cd "$RAIZ"
  exec "$HF" "$@"
fi

COMP="$PASTA/composicao"
mkdir -p "$COMP/cenas" "$PASTA/narracao"

# ligar <nome dentro de composicao/> <caminho relativo a composicao/>
ligar() {
  local nome="$1" alvo="$2" destino="$COMP/$1"
  [ -L "$destino" ] && return 0
  if [ -e "$destino" ]; then
    [ -f "$destino/.copia-gerada" ] || erro "$destino já existe e não foi criado por este script; mova ou apague à mão."
    rm -rf "$destino"
  fi
  (cd "$COMP" && MSYS=winsymlinks:nativestrict ln -s "$alvo" "$nome" 2>/dev/null) || true
  if [ ! -L "$destino" ]; then
    cp -R "$COMP/$alvo" "$destino"
    touch "$destino/.copia-gerada"
  fi
}

ligar assets ../../../assets
ligar componentes ../../../componentes
ligar narracao ../narracao

cd "$COMP"
exec "$HF" "$@"
