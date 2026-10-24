#!/usr/bin/env bash
# Checagens técnicas do final.mp4 de um vídeo (ESTRUTURA.md, seção 8).
# Uso: ./scripts/verificar.sh [--teste] videos/AAAA-MM-DD-slug
#   --teste  aceita duração de 10 a 20 s (vídeo de teste, seção 10) em vez de 45 a 90 s.
#
# Tudo pelo HyperFrames (áudio e quadros) e pelo scripts/mp4info.py (cabeçalho do MP4),
# sem chamar o FFmpeg diretamente. Também grava em amostras/ 6 quadros do final.mp4
# (ref-*.png), lado a lado com a composição (pair-*.jpg), e a assinatura SHA-256 do
# arquivo. Se já houver uma assinatura de um render anterior, diz se o novo render
# saiu idêntico (teste de determinismo).
set -euo pipefail

DURACAO_MIN=45
DURACAO_MAX=90
if [ "${1:-}" = "--teste" ]; then
  DURACAO_MIN=10
  DURACAO_MAX=20
  shift
fi

if [ $# -ne 1 ]; then
  echo "Uso: $0 [--teste] videos/AAAA-MM-DD-slug" >&2
  exit 1
fi

PASTA="${1%/}"
if [ ! -f "$PASTA/final.mp4" ]; then
  echo "Não encontrei $PASTA/final.mp4" >&2
  exit 1
fi

PY=""
for candidato in python3 python; do
  if command -v "$candidato" >/dev/null 2>&1 &&
     "$candidato" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
    PY="$candidato"
    break
  fi
done
[ -n "$PY" ] || { echo "Python 3.10+ não encontrado." >&2; exit 1; }

SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$PY" - "$PASTA" "$DURACAO_MIN" "$DURACAO_MAX" "$SCRIPTS" <<'PY'
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

pasta = Path(sys.argv[1]).resolve()
duracao_min, duracao_max = float(sys.argv[2]), float(sys.argv[3])
scripts = Path(sys.argv[4])
sys.path.insert(0, str(scripts))
import mp4info  # noqa: E402

video = pasta / "final.mp4"
amostras = pasta / "amostras"
hf = str(scripts / "hf.sh")

LUFS_ALVO, LUFS_TOLERANCIA = -14.0, 1.0
TRILHA_ABAIXO_DA_VOZ = 15.0  # dB: quanto a trilha precisa ficar abaixo da voz
SILENCIO = -60.0             # dBFS: abaixo disso, considera que não há trilha
FOLGA_FINAL = 0.3            # s: tempo mínimo entre a última palavra e o fim do vídeo

falhas = []


def ok(msg):
    print(f"  OK    {msg}")


def falha(msg):
    print(f"  FALHA {msg}")
    falhas.append(msg)


def aviso(msg):
    print(f"  AVISO {msg}")


def hyperframes_json(*args):
    saida = subprocess.run([hf, *args, "--json"], capture_output=True, text=True, check=True).stdout
    return json.loads(saida)


def nivel(envelope, inicio, fim):
    """Nível médio (dB, média de potência) do envelope do HyperFrames entre inicio e fim."""
    passo = envelope["hopMs"] / 1000
    potencias = []
    for k, valor in enumerate(envelope["values"]):
        t = envelope["startsAt"] + k * passo
        if inicio <= t < fim and valor is not None:
            potencias.append(10 ** (max(valor, -120) / 10))
    if not potencias:
        return -math.inf
    return 10 * math.log10(sum(potencias) / len(potencias))


print(f"Verificando {video}")

# Cabeçalho do MP4: resolução, fps, codecs e duração
cabecalho = mp4info.info(video)
v, a = cabecalho["video"], cabecalho["audio"]
duracao = cabecalho["duracao"]
if v is None:
    falha("o arquivo não tem trilha de vídeo")
else:
    if (v["largura"], v["altura"]) == (1080, 1920):
        ok("resolução 1080x1920")
    else:
        falha(f"resolução {v['largura']}x{v['altura']} (esperado 1080x1920)")
    if v["fps"] == "30/1":
        ok("30 fps")
    else:
        falha(f"fps {v['fps']} (esperado 30/1)")
    if v["codec"] == "h264":
        ok("vídeo H.264")
    else:
        falha(f"vídeo em {v['codec']} (esperado h264)")

if duracao_min <= duracao <= duracao_max:
    ok(f"duração {duracao:.2f} s (entre {duracao_min:g} e {duracao_max:g} s)")
else:
    falha(f"duração {duracao:.2f} s (esperado entre {duracao_min:g} e {duracao_max:g} s)")

# Áudio, medido pelo HyperFrames
palavras_json = pasta / "narracao" / "palavras.json"
palavras = json.loads(palavras_json.read_text(encoding="utf-8")) if palavras_json.is_file() else []
if a is None:
    falha("o arquivo não tem trilha de áudio")
else:
    ok(f"trilha de áudio ({a['codec']})")
    if a["codec"] != "aac":
        falha(f"áudio em {a['codec']} (esperado aac)")

    som = hyperframes_json("audio", str(video))["items"][0]
    volume = som["loudness"]

    if not palavras:
        falha(f"não encontrei {palavras_json} para conferir o fim da narração")
    else:
        ultima = palavras[-1]["fim"]
        fim_audio = min(duracao, som["duration"])
        if ultima + FOLGA_FINAL <= fim_audio:
            ok(f"narração termina em {ultima:.2f} s, antes do fim do vídeo ({duracao:.2f} s)")
        else:
            falha(f"narração cortada: a última palavra termina em {ultima:.2f} s, "
                  f"e o áudio acaba em {fim_audio:.2f} s")

    lufs = volume["lufsIntegrated"]
    if abs(lufs - LUFS_ALVO) <= LUFS_TOLERANCIA:
        ok(f"volume {lufs:.1f} LUFS (alvo {LUFS_ALVO:g} ± {LUFS_TOLERANCIA:g})")
    else:
        falha(f"volume {lufs:.1f} LUFS (alvo {LUFS_ALVO:g} ± {LUFS_TOLERANCIA:g}); "
              "rode ./scripts/ajustar-volume.sh e renderize de novo")
    if volume["clipping"]["count"]:
        falha(f"áudio estourado (clipping) a partir de {volume['clipping']['firstAt']} s")

    # Trilha de fundo: mede as pausas entre palavras (e o final) contra o trecho falado.
    if palavras:
        envelope = som["envelope"]
        pausas = []
        for anterior, seguinte in zip(palavras, palavras[1:]):
            if seguinte["inicio"] - anterior["fim"] >= 0.6:
                pausas.append((anterior["fim"] + 0.15, seguinte["inicio"] - 0.15))
        pausas.append((palavras[-1]["fim"] + 0.5, duracao - 0.05))
        pausas = [(i, f) for i, f in pausas if f - i >= 0.3]
        voz = nivel(envelope, palavras[0]["inicio"], palavras[-1]["fim"])
        if not pausas:
            aviso("sem pausas longas para medir a trilha de fundo")
        else:
            fundo = max(nivel(envelope, i, f) for i, f in pausas)
            if fundo <= SILENCIO:
                ok("sem trilha de fundo audível nas pausas")
            elif voz - fundo >= TRILHA_ABAIXO_DA_VOZ:
                ok(f"trilha de fundo {voz - fundo:.1f} dB abaixo da voz")
            else:
                falha(f"trilha de fundo só {voz - fundo:.1f} dB abaixo da voz "
                      f"(mínimo {TRILHA_ABAIXO_DA_VOZ:g} dB)")

# O snapshot limpa amostras/: guarda antes a assinatura do render anterior.
arquivo_assinatura = amostras / "assinatura.txt"
anterior = arquivo_assinatura.read_text().strip() if arquivo_assinatura.is_file() else None

# Quadros de amostra: snapshot do HyperFrames com o final.mp4 como referência
tempos = ",".join(f"{duracao * (2 * k - 1) / 12:.2f}" for k in range(1, 7))
subprocess.run([hf, str(pasta), "snapshot", "--at", tempos, "--no-end",
                "--against", "../final.mp4", "-o", "../amostras", "--json"],
               capture_output=True, text=True, check=True)
ok(f"6 quadros de amostra em {amostras} (ref-*.png: final.mp4; pair-*.jpg: composição | final)")

# Assinatura do arquivo (dois renders da mesma composição saem com os mesmos bytes)
sha = hashlib.sha256(video.read_bytes()).hexdigest()
if anterior:
    if anterior == sha:
        ok("render idêntico ao anterior (mesma assinatura)")
    else:
        aviso("render DIFERENTE do anterior (assinatura mudou; esperado só se a composição mudou)")
arquivo_assinatura.write_text(sha + "\n")

print()
if falhas:
    print(f"{len(falhas)} falha(s).")
    sys.exit(1)
print("Tudo certo.")
PY
