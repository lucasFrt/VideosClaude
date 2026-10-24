#!/usr/bin/env bash
# Cria a pasta de um vídeo novo a partir de modelos/ (ESTRUTURA.md, seção 8).
# Uso: ./scripts/novo-video.sh <slug>
#   ex.: ./scripts/novo-video.sh parar-de-imprimir-dinheiro
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FUSO="America/Sao_Paulo"

if [ $# -ne 1 ]; then
  echo "Uso: $0 <slug>" >&2
  exit 1
fi

SLUG="$1"
# Slug curto, em minúsculas, sem acentos e com hífens.
if ! [[ "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Slug inválido: '$SLUG'. Use só letras minúsculas sem acento, números e hífens (ex.: parar-de-imprimir-dinheiro)." >&2
  exit 1
fi

# Horário de Brasília quando o sistema conhece o fuso; senão, o relógio local
# (o Git Bash do Windows não traz a base de fusos).
if [ -e "/usr/share/zoneinfo/$FUSO" ]; then export TZ="$FUSO"; fi
HOJE="$(date +%F)"
AGORA="$(date '+%F %H:%M')"
PASTA="$RAIZ/videos/$HOJE-$SLUG"

if [ -e "$PASTA" ]; then
  echo "Já existe: $PASTA" >&2
  exit 1
fi

mkdir -p "$PASTA/narracao" "$PASTA/composicao/cenas"
cp "$RAIZ/modelos/01-ideia.md" "$RAIZ/modelos/02-fontes.md" \
   "$RAIZ/modelos/03-roteiro.toml" "$RAIZ/modelos/04-revisoes.md" "$PASTA/"
sed -e "s/^etapa_atual: .*/etapa_atual: onda-1/" \
    -e "s/^ultima_atualizacao: .*/ultima_atualizacao: $AGORA/" \
    -e "s/^  - AAAA-MM-DD HH:MM onda-1$/  - $AGORA onda-1/" \
    "$RAIZ/modelos/status.md" > "$PASTA/status.md"

echo "Criado: ${PASTA#"$RAIZ"/}"
