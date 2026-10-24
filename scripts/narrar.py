#!/usr/bin/env python3
"""Gera a narração de um vídeo com o edge-tts (ESTRUTURA.md, seção 8).

Uso: python3 scripts/narrar.py videos/AAAA-MM-DD-slug
     python3 scripts/narrar.py --estimar videos/AAAA-MM-DD-slug

Lê   narracao/texto.txt  (blocos marcados com uma linha "[BLOCO N]")
Gera narracao/narracao.mp3  (o áudio do edge-tts como veio; o volume é ajustado na
                            composição pelo "normalize-audio" do HyperFrames)
     narracao/palavras.json (lista de {"palavra", "inicio", "fim", "bloco"}, em segundos)

--estimar: sem voz (quando o edge-tts não está disponível), gera só o palavras.json com
tempos estimados pelo tamanho das palavras e pela pontuação, e deixa a marca
narracao/ESTIMADO. A narração real substitui tudo e apaga a marca.
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path


def carregar_edge_tts():
    try:
        import edge_tts
    except ImportError:
        # Sem edge-tts neste Python: usa o ambiente virtual criado pelo scripts/instalar.sh.
        if sys.prefix == sys.base_prefix:
            raiz = Path(__file__).resolve().parent.parent
            for py in (raiz / ".venv" / "bin" / "python", raiz / ".venv" / "Scripts" / "python.exe"):
                if py.is_file():
                    os.execv(str(py), [str(py), *sys.argv])
        sys.exit("ERRO: edge-tts não instalado. Rode ./scripts/instalar.sh")
    return edge_tts


# Fixos por decisão do canal. Não mudar sem autorização.
VOZ = "pt-BR-AntonioNeural"
RITMO = "+10%"

TICKS_POR_SEGUNDO = 10_000_000  # o edge-tts informa tempos em unidades de 100 ns

# Ritmo da estimativa sem voz, perto do da voz fixa (calibrar com a primeira narração real).
INICIO_ESTIMADO = 0.15
SEGUNDOS_POR_PALAVRA = 0.06
SEGUNDOS_POR_LETRA = 0.045
INTERVALO_ENTRE_PALAVRAS = 0.02
PAUSAS = {",": 0.2, ";": 0.3, ":": 0.3, ".": 0.45, "?": 0.45, "!": 0.45}
PAUSA_ENTRE_BLOCOS = 0.35

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


def estimar(blocos):
    """Tempos de cada palavra sem voz: tamanho da palavra mais as pausas da pontuação."""
    palavras = []
    t = INICIO_ESTIMADO
    for numero, texto in blocos:
        for bruta in texto.split():
            palavra = bruta.strip(".,;:?!…\"'()")
            if not palavra:
                continue
            duracao = SEGUNDOS_POR_PALAVRA + SEGUNDOS_POR_LETRA * len(re.sub(r"\W", "", palavra))
            palavras.append({"palavra": palavra, "inicio": round(t, 2),
                             "fim": round(t + duracao, 2), "bloco": numero})
            t += duracao + INTERVALO_ENTRE_PALAVRAS + PAUSAS.get(bruta[-1], 0)
        t += PAUSA_ENTRE_BLOCOS
    return palavras


async def sintetizar(texto, destino):
    """Grava o MP3 bruto e retorna os eventos de limite de palavra."""
    edge_tts = carregar_edge_tts()
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


def main():
    argumentos = sys.argv[1:]
    sem_voz = "--estimar" in argumentos
    argumentos = [a for a in argumentos if a != "--estimar"]
    if len(argumentos) != 1:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    pasta = Path(argumentos[0]).resolve()
    narracao = pasta / "narracao"
    texto_txt = narracao / "texto.txt"
    if not texto_txt.is_file():
        erro(f"não encontrei {texto_txt}.")

    blocos = ler_blocos(texto_txt)
    for numero, texto in blocos:
        if re.search(r"\d", texto):
            print(f"AVISO: o bloco {numero} tem algarismos. Se a voz puder ler errado, "
                  "escreva o número por extenso.", file=sys.stderr)

    marca = narracao / "ESTIMADO"
    if sem_voz:
        if (narracao / "narracao.mp3").exists():
            erro("já existe narracao.mp3: tempos estimados ficariam fora de sincronia com ela.")
        palavras = estimar(blocos)
        (narracao / "palavras.json").write_text(
            json.dumps(palavras, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        marca.write_text("Tempos estimados, sem voz (narrar.py --estimar). "
                         "Rode o narrar.py sem --estimar para gerar a narração real.\n", encoding="utf-8")
        print(f"Tempos ESTIMADOS (sem voz) para {len(palavras)} palavras: "
              f"{palavras[-1]['fim']:.1f} s de fala.")
        return

    texto_completo = " ".join(texto for _, texto in blocos)

    # Grava ao lado e só troca no fim, para uma falha não deixar meia narração.
    provisorio = narracao / "narracao.mp3.parcial"
    eventos = asyncio.run(sintetizar(texto_completo, provisorio))
    if not eventos:
        provisorio.unlink()
        erro("o edge-tts não devolveu limites de palavra.")
    palavras = associar_blocos(eventos, blocos, texto_completo)
    os.replace(provisorio, narracao / "narracao.mp3")
    marca.unlink(missing_ok=True)

    (narracao / "palavras.json").write_text(
        json.dumps(palavras, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Voz: {VOZ}, ritmo {RITMO}, {len(palavras)} palavras.")
    for numero, _ in blocos:
        do_bloco = [p for p in palavras if p["bloco"] == numero]
        print(f"  Bloco {numero}: {do_bloco[0]['inicio']:.2f}s a {do_bloco[-1]['fim']:.2f}s "
              f"({len(do_bloco)} palavras)")


if __name__ == "__main__":
    main()
