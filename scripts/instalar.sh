#!/usr/bin/env bash
# Prepara esta máquina para produzir os vídeos (ESTRUTURA.md, seção 2).
# Uso: ./scripts/instalar.sh [--sem-voz]
#   --sem-voz  não testa a conexão com o serviço de voz do edge-tts
#
# Pode rodar quantas vezes quiser: instala só o que falta, confere os arquivos do
# projeto e no fim renderiza um teste de 3 s para provar que tudo funciona.
# No Windows, rode pelo Git Bash (o mesmo shell que o Claude Code usa).
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

TESTAR_VOZ=1
[ "${1:-}" = "--sem-voz" ] && TESTAR_VOZ=0

passo() { printf '\n== %s\n' "$*"; }
ok() { printf '  OK    %s\n' "$*"; }
aviso() { printf '  AVISO %s\n' "$*"; }
falha() {
  printf '  FALHA %s\n' "$*" >&2
  exit 1
}

case "$(uname -s)" in
  Darwin) SO=mac ;;
  MINGW* | MSYS* | CYGWIN*) SO=windows ;;
  *) SO=linux ;;
esac

# dica <mac> <linux> <windows>
dica() {
  case "$SO" in
    mac) echo "$1" ;;
    windows) echo "$3" ;;
    *) echo "$2" ;;
  esac
}

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"; else shasum -a 256 "$@"; fi
}

passo "1. Ferramentas"
command -v node >/dev/null 2>&1 ||
  falha "Node.js não encontrado. Instale o 22 ou mais novo: $(dica 'brew install node' 'https://nodejs.org' 'winget install OpenJS.NodeJS.LTS')"
[ "$(node -p 'process.versions.node.split(".")[0]')" -ge 22 ] ||
  falha "Node $(node -v) é antigo: o HyperFrames exige o 22 ou mais novo."
ok "Node $(node -v)"

PY=""
for candidato in python3 python; do
  if command -v "$candidato" >/dev/null 2>&1 &&
     "$candidato" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
    PY="$candidato"
    break
  fi
done
[ -n "$PY" ] ||
  falha "Python 3.11+ não encontrado: $(dica 'brew install python' 'sudo apt install python3 python3-venv' 'winget install Python.Python.3.12')"
ok "$("$PY" --version)"

passo "2. HyperFrames (versão fixa do package.json, com o FFmpeg que ele usa por dentro)"
npm ci --no-audit --no-fund
ok "hyperframes $(node -p 'require("./node_modules/hyperframes/package.json").version')"
source scripts/ambiente.sh
"$HF" browser ensure >/dev/null
ok "Chrome do HyperFrames: $("$HF" browser path | tail -1)"

passo "3. Narração (edge-tts em um Python só do projeto, em .venv/)"
[ -d .venv ] || "$PY" -m venv .venv
VPY=".venv/bin/python"
[ -e "$VPY" ] || VPY=".venv/Scripts/python.exe"
"$VPY" -m pip install --quiet --disable-pip-version-check -r requirements.txt
ok "edge-tts $("$VPY" -c 'import importlib.metadata as m; print(m.version("edge-tts"))')"

passo "4. Arquivos do projeto"
(cd assets && sha256 -c SHA256SUMS >/dev/null) ||
  falha "bibliotecas ou fontes em assets/ não batem com assets/SHA256SUMS"
ok "bibliotecas e fontes conferidas (assets/SHA256SUMS)"
for skill in hyperframes hyperframes-cli hyperframes-registry media-use; do
  [ -f ".claude/skills/$skill/SKILL.md" ] || falha "skill $skill ausente em .claude/skills/"
done
ok "skills do HyperFrames em .claude/skills/"

passo "5. Diagnóstico do HyperFrames"
"$HF" doctor --json | node -e '
  const r = JSON.parse(require("fs").readFileSync(0, "utf8"));
  const precisa = ["FFmpeg", "FFprobe", "Chrome"];
  let falhou = false;
  for (const nome of precisa) {
    const c = (r.checks || []).find((x) => x.name === nome);
    const certo = c && c.ok;
    console.log(`  ${certo ? "OK   " : "FALHA"} ${nome}${c && c.detail ? ": " + c.detail : ""}`);
    if (!certo) falhou = true;
  }
  process.exit(falhou ? 1 : 0);
' || falha "rode './scripts/hf.sh doctor' para ver o detalhe"

passo "6. Teste de render (3 s com GSAP, Three.js, fonte e áudio)"
T="videos/.teste-ambiente"
mkdir -p "$T/composicao" "$T/narracao"
rm -rf "$T/composicao/cenas"
cp -R scripts/teste-ambiente/composicao/. "$T/composicao/"
cp scripts/teste-ambiente/narracao/narracao.mp3 "$T/narracao/"
./scripts/hf.sh "$T" check --json 2>/dev/null >"$T/check.json" || true
node -e '
  const r = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
  if (!r.ok) { console.error(JSON.stringify(r, null, 2)); process.exit(1); }
' "$T/check.json" || falha "o check do HyperFrames reprovou a composição de teste (detalhes acima)"
ok "check do HyperFrames"
./scripts/hf.sh "$T" render --quality draft --output ../teste.mp4 >"$T/render.log" 2>&1 ||
  falha "o render falhou; veja $T/render.log"
INFO="$("$PY" scripts/mp4info.py "$T/teste.mp4")"
case "$INFO" in
  *'"codec": "h264", "largura": 1080, "altura": 1920, "fps": "30/1"'*'"audio": {"codec": "aac"}'*)
    ok "render: $T/teste.mp4 (H.264 1080x1920 30 fps, áudio AAC)" ;;
  *) falha "render saiu fora do padrão: $INFO" ;;
esac

passo "7. Voz (edge-tts)"
if [ "$TESTAR_VOZ" = 1 ]; then
  if "$VPY" -c '
import asyncio, sys, edge_tts
async def main():
    await edge_tts.Communicate("Teste.", "pt-BR-AntonioNeural", rate="+10%").save(sys.argv[1])
asyncio.run(main())
' "$T/voz.mp3" 2>/dev/null; then
    ok "pt-BR-AntonioNeural respondeu ($T/voz.mp3)"
  else
    aviso "não consegui falar com o serviço de voz do edge-tts. Sem internet (ou com a rede bloqueando WebSocket), o narrar.py não funciona."
  fi
else
  aviso "teste de voz pulado (--sem-voz)"
fi

printf '\nTudo pronto. Próximo passo: o vídeo de teste da seção 10 do ESTRUTURA.md.\n'
