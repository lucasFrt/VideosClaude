# Ambiente comum aos scripts que chamam o HyperFrames. Uso: source scripts/ambiente.sh
#
# - Telemetria e atualizações automáticas desligadas (ESTRUTURA.md, seção 12).
# - O FFmpeg é o motor interno do HyperFrames: vem pelo npm (ffmpeg-static e
#   @ffprobe-installer/ffprobe, versões fixas no package.json) e ninguém o usa
#   diretamente. Estas variáveis só dizem ao HyperFrames onde ele está.

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HF="$RAIZ/node_modules/.bin/hyperframes"

export HYPERFRAMES_NO_TELEMETRY=1
export HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_SKIP_SKILLS=1

if [ -e "$HF" ]; then
  HYPERFRAMES_FFMPEG_PATH="$(cd "$RAIZ" && node -p 'require("ffmpeg-static")')"
  HYPERFRAMES_FFPROBE_PATH="$(cd "$RAIZ" && node -p 'require("@ffprobe-installer/ffprobe").path')"
  export HYPERFRAMES_FFMPEG_PATH HYPERFRAMES_FFPROBE_PATH
fi
