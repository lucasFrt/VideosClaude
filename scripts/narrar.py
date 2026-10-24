#!/usr/bin/env python3
"""Gera a narração de um vídeo com o edge-tts (ESTRUTURA.md, seção 8).

Uso: python3 scripts/narrar.py videos/AAAA-MM-DD-slug

Lê   narracao/texto.txt  (blocos marcados com uma linha "[BLOCO N]")
Gera narracao/narracao.mp3  (normalizada em -14 LUFS)
     narracao/palavras.json (lista de {"palavra", "inicio", "fim", "bloco"}, em segundos)
"""

import asyncio
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import edge_tts

# Fixos por decisão do canal. Não mudar sem autorização.
VOZ = "pt-BR-AntonioNeural"
RITMO = "+10%"

LUFS_ALVO = -14.0
PICO_MAXIMO = -1.5  # dBTP
TICKS_POR_SEGUNDO = 10_000_000  # o edge-tts informa tempos em unidades de 100 ns

MARCA_BLOCO = re.compile(r"^\[BLOCO (\d+)\]$")


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def ler_blocos(caminho):
    """Retorna [(numero_do_bloco, texto)] na ordem do arquivo."""
    blocos = []
    for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
        linha = linha.strip()
        if not linha:
            continue
        marca = MARCA_BLOCO.match(linha)
        if marca:
            blocos.append((int(marca.group(1)), []))
        elif not blocos:
            erro(f"{caminho}:{n}: texto antes do primeiro [BLOCO N].")
        else:
            blocos[-1][1].append(linha)

    if not blocos:
        erro(f"{caminho}: nenhum [BLOCO N] encontrado.")
    numeros = [b[0] for b in blocos]
    if numeros != list(range(1, len(blocos) + 1)):
        erro(f"{caminho}: os blocos precisam ser 1, 2, 3... em ordem; encontrei {numeros}.")
    for numero, linhas in blocos:
        if not linhas:
            erro(f"{caminho}: o [BLOCO {numero}] está vazio.")
    return [(numero, " ".join(linhas)) for numero, linhas in blocos]


async def sintetizar(texto, destino):
    """Grava o MP3 bruto e retorna os eventos de limite de palavra."""
    comunicacao = edge_tts.Communicate(
        texto,
        VOZ,
        rate=RITMO,
        boundary="WordBoundary",
        proxy=os.environ.get("HTTPS_PROXY") or None,
    )
    eventos = []
    with open(destino, "wb") as audio:
        async for parte in comunicacao.stream():
            if parte["type"] == "audio":
                audio.write(parte["data"])
            elif parte["type"] == "WordBoundary":
                eventos.append(parte)
    return eventos


def associar_blocos(eventos, blocos, texto_completo):
    """Descobre o bloco de cada palavra pela posição dela no texto enviado à voz."""
    limites = []  # (inicio_no_texto, fim_no_texto, numero_do_bloco)
    pos = 0
    for numero, texto in blocos:
        limites.append((pos, pos + len(texto), numero))
        pos += len(texto) + 1  # +1 pelo espaço que une os blocos

    palavras = []
    cursor = 0
    bloco_atual = blocos[0][0]
    for evento in eventos:
        palavra = evento["text"]
        achado = texto_completo.find(palavra, cursor)
        if achado >= 0:
            cursor = achado + len(palavra)
            bloco_atual = next(n for ini, fim, n in limites if achado < fim + 1)
        else:
            print(f"AVISO: não localizei '{palavra}' no texto; ficou no bloco {bloco_atual}.",
                  file=sys.stderr)
        inicio = evento["offset"] / TICKS_POR_SEGUNDO
        fim = (evento["offset"] + evento["duration"]) / TICKS_POR_SEGUNDO
        palavras.append({
            "palavra": palavra,
            "inicio": round(inicio, 2),
            "fim": round(fim, 2),
            "bloco": bloco_atual,
        })

    faltando = {n for n, _ in blocos} - {p["bloco"] for p in palavras}
    if faltando:
        erro(f"nenhuma palavra associada aos blocos {sorted(faltando)}.")
    return palavras


def normalizar(origem, destino):
    """Loudnorm em duas passagens (modo linear): só muda o ganho, não o tempo."""
    medicao = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(origem), "-af",
         f"loudnorm=I={LUFS_ALVO}:TP={PICO_MAXIMO}:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    m = json.loads(medicao[medicao.rindex("{"):medicao.rindex("}") + 1])
    filtro = (
        f"loudnorm=I={LUFS_ALVO}:TP={PICO_MAXIMO}:LRA=11"
        f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
        f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
        f":offset={m['target_offset']}:linear=true"
    )
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(origem),
         "-af", filtro, "-ar", "48000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k",
         str(destino)],
        check=True,
    )


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    pasta = Path(sys.argv[1]).resolve()
    narracao = pasta / "narracao"
    texto_txt = narracao / "texto.txt"
    if not texto_txt.is_file():
        erro(f"não encontrei {texto_txt}.")

    blocos = ler_blocos(texto_txt)
    for numero, texto in blocos:
        if re.search(r"\d", texto):
            print(f"AVISO: o bloco {numero} tem algarismos. Se a voz puder ler errado, "
                  "escreva o número por extenso.", file=sys.stderr)

    texto_completo = " ".join(texto for _, texto in blocos)

    with tempfile.TemporaryDirectory() as tmp:
        bruto = Path(tmp) / "bruto.mp3"
        eventos = asyncio.run(sintetizar(texto_completo, bruto))
        if not eventos:
            erro("o edge-tts não devolveu limites de palavra.")
        palavras = associar_blocos(eventos, blocos, texto_completo)
        normalizar(bruto, narracao / "narracao.mp3")

    (narracao / "palavras.json").write_text(
        json.dumps(palavras, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Voz: {VOZ}, ritmo {RITMO}, {len(palavras)} palavras.")
    for numero, _ in blocos:
        do_bloco = [p for p in palavras if p["bloco"] == numero]
        print(f"  Bloco {numero}: {do_bloco[0]['inicio']:.2f}s a {do_bloco[-1]['fim']:.2f}s "
              f"({len(do_bloco)} palavras)")


if __name__ == "__main__":
    main()
