#!/usr/bin/env python3
"""Lê resolução, fps, codecs e duração de um MP4 direto do cabeçalho, sem ferramentas externas.

Uso: python3 scripts/mp4info.py arquivo.mp4   (imprime JSON)
"""

import json
import struct
import sys
from fractions import Fraction

CODECS = {b"avc1": "h264", b"avc3": "h264", b"hvc1": "h265", b"hev1": "h265", b"mp4a": "aac"}


def caixas(dados, inicio=0, fim=None):
    """Percorre as caixas (boxes) de um trecho: devolve (tipo, inicio_do_conteudo, fim)."""
    fim = len(dados) if fim is None else fim
    pos = inicio
    while pos + 8 <= fim:
        tamanho, tipo = struct.unpack(">I4s", dados[pos:pos + 8])
        cabecalho = 8
        if tamanho == 1:
            tamanho = struct.unpack(">Q", dados[pos + 8:pos + 16])[0]
            cabecalho = 16
        elif tamanho == 0:
            tamanho = fim - pos
        if tamanho < cabecalho:
            break
        yield tipo, pos + cabecalho, pos + tamanho
        pos += tamanho


def filho(dados, inicio, fim, tipo):
    return next(((i, f) for t, i, f in caixas(dados, inicio, fim) if t == tipo), None)


def escala_e_duracao(dados, inicio):
    """mvhd e mdhd têm o mesmo começo: versão, datas, escala de tempo e duração."""
    if dados[inicio] == 1:
        return struct.unpack(">IQ", dados[inicio + 20:inicio + 32])
    return struct.unpack(">II", dados[inicio + 12:inicio + 20])


def ler_moov(caminho):
    with open(caminho, "rb") as arquivo:
        while True:
            cabecalho = arquivo.read(8)
            if len(cabecalho) < 8:
                raise ValueError("arquivo sem caixa moov (não é um MP4 completo)")
            tamanho, tipo = struct.unpack(">I4s", cabecalho)
            lido = 8
            if tamanho == 1:
                tamanho = struct.unpack(">Q", arquivo.read(8))[0]
                lido = 16
            if tipo == b"moov":
                return arquivo.read(tamanho - lido)
            if tamanho == 0:
                raise ValueError("arquivo sem caixa moov (não é um MP4 completo)")
            arquivo.seek(tamanho - lido, 1)


def info(caminho):
    moov = ler_moov(caminho)
    mvhd = filho(moov, 0, len(moov), b"mvhd")
    escala, duracao = escala_e_duracao(moov, mvhd[0])
    resultado = {"duracao": round(duracao / escala, 3), "video": None, "audio": None}

    for tipo, inicio, fim in caixas(moov):
        if tipo != b"trak":
            continue
        mdia = filho(moov, inicio, fim, b"mdia")
        hdlr = filho(moov, *mdia, b"hdlr")
        tipo_trilha = moov[hdlr[0] + 8:hdlr[0] + 12]
        minf = filho(moov, *mdia, b"minf")
        stbl = filho(moov, *minf, b"stbl")
        stsd = filho(moov, *stbl, b"stsd")
        codec = moov[stsd[0] + 12:stsd[0] + 16]
        nome = CODECS.get(codec, codec.decode("latin-1"))

        if tipo_trilha == b"vide":
            tkhd = filho(moov, inicio, fim, b"tkhd")
            largura, altura = struct.unpack(">II", moov[tkhd[1] - 8:tkhd[1]])
            escala_trilha, duracao_trilha = escala_e_duracao(moov, filho(moov, *mdia, b"mdhd")[0])
            stts = filho(moov, *stbl, b"stts")
            entradas = struct.unpack(">I", moov[stts[0] + 4:stts[0] + 8])[0]
            quadros, deltas = 0, set()
            for k in range(entradas):
                n, delta = struct.unpack(">II", moov[stts[0] + 8 + 8 * k:stts[0] + 16 + 8 * k])
                quadros += n
                deltas.add(delta)
            fps = (Fraction(escala_trilha, deltas.pop()) if len(deltas) == 1
                   else Fraction(quadros * escala_trilha, duracao_trilha).limit_denominator(1001))
            resultado["video"] = {
                "codec": nome,
                "largura": largura >> 16,
                "altura": altura >> 16,
                "fps": f"{fps.numerator}/{fps.denominator}",
                "quadros": quadros,
            }
        elif tipo_trilha == b"soun":
            resultado["audio"] = {"codec": nome}

    return resultado


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    print(json.dumps(info(sys.argv[1]), ensure_ascii=False))
