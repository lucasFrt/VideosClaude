#!/usr/bin/env bash
# Checagens técnicas do final.mp4 de um vídeo (ESTRUTURA.md, seção 8).
# Uso: ./scripts/verificar.sh [--teste] videos/AAAA-MM-DD-slug
#   --teste  aceita duração de 10 a 20 s (vídeo de teste, seção 10) em vez de 45 a 60 s.
#
# Também gera 6 quadros em amostras/ e uma assinatura (MD5 dos quadros e do áudio
# decodificados) em amostras/assinatura.txt. Se já houver uma assinatura de um
# render anterior, diz se o novo render saiu idêntico (teste de determinismo).
set -euo pipefail

DURACAO_MIN=45
DURACAO_MAX=60
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

exec python3 - "$PASTA" "$DURACAO_MIN" "$DURACAO_MAX" <<'PY'
import json
import math
import re
import subprocess
import sys
from pathlib import Path

pasta = Path(sys.argv[1])
duracao_min, duracao_max = float(sys.argv[2]), float(sys.argv[3])
video = pasta / "final.mp4"
amostras = pasta / "amostras"

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


def ffmpeg_stderr(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                          capture_output=True, text=True, check=True).stderr


def rms_db(inicio, duracao):
    """Nível RMS (dBFS) do áudio do vídeo no intervalo dado."""
    saida = ffmpeg_stderr("-ss", f"{inicio:.3f}", "-t", f"{duracao:.3f}", "-i", str(video),
                          "-map", "0:a:0", "-af", "astats=metadata=0", "-f", "null", "-")
    niveis = re.findall(r"RMS level dB: (\S+)", saida)
    return float(niveis[-1]) if niveis and niveis[-1] != "-inf" else -math.inf


print(f"Verificando {video}")

info = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)],
    capture_output=True, text=True, check=True).stdout)
v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
duracao = float(info["format"]["duration"])

# Resolução, fps e codecs
if v is None:
    falha("o arquivo não tem trilha de vídeo")
else:
    if (v["width"], v["height"]) == (1080, 1920):
        ok("resolução 1080x1920")
    else:
        falha(f"resolução {v['width']}x{v['height']} (esperado 1080x1920)")
    if v["avg_frame_rate"] == "30/1" and v["r_frame_rate"] == "30/1":
        ok("30 fps")
    else:
        falha(f"fps {v['avg_frame_rate']} (esperado 30/1)")
    if v["codec_name"] == "h264":
        ok("vídeo H.264")
    else:
        falha(f"vídeo em {v['codec_name']} (esperado h264)")

# Duração
if duracao_min <= duracao <= duracao_max:
    ok(f"duração {duracao:.2f} s (entre {duracao_min:g} e {duracao_max:g} s)")
else:
    falha(f"duração {duracao:.2f} s (esperado entre {duracao_min:g} e {duracao_max:g} s)")

# Áudio
palavras_json = pasta / "narracao" / "palavras.json"
palavras = json.loads(palavras_json.read_text(encoding="utf-8")) if palavras_json.is_file() else []
if a is None:
    falha("o arquivo não tem trilha de áudio")
else:
    ok(f"trilha de áudio ({a['codec_name']})")
    if a["codec_name"] != "aac":
        falha(f"áudio em {a['codec_name']} (esperado aac)")

    if not palavras:
        falha(f"não encontrei {palavras_json} para conferir o fim da narração")
    else:
        ultima = palavras[-1]["fim"]
        fim_audio = float(a.get("duration", duracao))
        if ultima + FOLGA_FINAL <= min(duracao, fim_audio):
            ok(f"narração termina em {ultima:.2f} s, antes do fim do vídeo ({duracao:.2f} s)")
        else:
            falha(f"narração cortada: a última palavra termina em {ultima:.2f} s, "
                  f"e o vídeo/áudio acaba em {min(duracao, fim_audio):.2f} s")

    medicao = ffmpeg_stderr("-i", str(video), "-map", "0:a:0", "-af",
                            "loudnorm=print_format=json", "-f", "null", "-")
    lufs = float(json.loads(medicao[medicao.rindex("{"):medicao.rindex("}") + 1])["input_i"])
    if abs(lufs - LUFS_ALVO) <= LUFS_TOLERANCIA:
        ok(f"volume {lufs:.1f} LUFS (alvo {LUFS_ALVO:g} ± {LUFS_TOLERANCIA:g})")
    else:
        falha(f"volume {lufs:.1f} LUFS (alvo {LUFS_ALVO:g} ± {LUFS_TOLERANCIA:g})")

    # Trilha de fundo: mede as pausas entre palavras (e o final) contra o trecho falado.
    if palavras:
        pausas = []
        for anterior, seguinte in zip(palavras, palavras[1:]):
            if seguinte["inicio"] - anterior["fim"] >= 0.6:
                pausas.append((anterior["fim"] + 0.15, seguinte["inicio"] - 0.15))
        pausas.append((palavras[-1]["fim"] + 0.5, duracao - 0.05))
        pausas = [(i, f) for i, f in pausas if f - i >= 0.3]
        voz = rms_db(palavras[0]["inicio"], palavras[-1]["fim"] - palavras[0]["inicio"])
        if not pausas:
            aviso("sem pausas longas para medir a trilha de fundo")
        else:
            fundo = max(rms_db(i, f - i) for i, f in pausas)
            if fundo <= SILENCIO:
                ok("sem trilha de fundo audível nas pausas")
            elif voz - fundo >= TRILHA_ABAIXO_DA_VOZ:
                ok(f"trilha de fundo {voz - fundo:.1f} dB abaixo da voz")
            else:
                falha(f"trilha de fundo só {voz - fundo:.1f} dB abaixo da voz "
                      f"(mínimo {TRILHA_ABAIXO_DA_VOZ:g} dB)")

# Quadros de amostra
amostras.mkdir(exist_ok=True)
for antiga in amostras.glob("amostra-*.png"):
    antiga.unlink()
for k in range(1, 7):
    t = duracao * (2 * k - 1) / 12
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.3f}",
                    "-i", str(video), "-frames:v", "1", str(amostras / f"amostra-{k}.png")],
                   check=True)
ok(f"6 quadros de amostra em {amostras}")

# Assinatura do conteúdo decodificado (independe de metadados do contêiner)
def md5(mapa):
    return subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
                           "-map", mapa, "-f", "md5", "-"],
                          capture_output=True, text=True, check=True).stdout.strip()

assinatura = f"video {md5('0:v:0')}\naudio {md5('0:a:0') if a else 'sem-audio'}\n"
arquivo_assinatura = amostras / "assinatura.txt"
if arquivo_assinatura.is_file():
    if arquivo_assinatura.read_text() == assinatura:
        ok("render idêntico ao anterior (mesma assinatura)")
    else:
        aviso("render DIFERENTE do anterior (assinatura mudou; esperado só se a composição mudou)")
arquivo_assinatura.write_text(assinatura)

print()
if falhas:
    print(f"{len(falhas)} falha(s).")
    sys.exit(1)
print("Tudo certo.")
PY
