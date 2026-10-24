#!/usr/bin/env python3
"""Monta a composição do vídeo a partir do roteiro e dos tempos da narração (ESTRUTURA.md, seção 8).

Uso: python3 scripts/montar.py videos/AAAA-MM-DD-slug

Lê   03-roteiro.toml, 02-fontes.md e narracao/palavras.json
Gera de novo a cada execução (não edite à mão):
     composicao/index.html               cenas nos tempos certos, sobreposições, legendas e narração
     composicao/tempos.js                tempos de cada bloco e frase para as cenas (window.TEMPOS)
     composicao/cenas/legendas.html      legendas de 1 a 4 palavras, sincronizadas
     composicao/cenas/sobreposicoes.html selo de IA e rodapés de fonte
Escritas à mão (o montar.py só cria um modelo simples quando falta):
     composicao/cenas/bloco-N.html       a cena de cada bloco do roteiro

Como tudo o que depende de tempo sai do palavras.json, trocar a narração (por exemplo, dos
tempos estimados para a voz real) é só rodar o montar.py de novo.
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roteiro as rot  # noqa: E402

FOLGA_FINAL = 1.5            # s depois da última palavra (ESTRUTURA.md, regra 6.6)
MAX_PALAVRAS = 4             # por legenda
MAX_LETRAS = 24              # por legenda, para caber em até duas linhas
PAUSA_QUE_QUEBRA = 0.15      # s de silêncio que começam uma legenda nova
LEGENDA_SEGURA = 0.35        # s que a legenda fica depois da última palavra, se não vier outra
TEXTO, DESTAQUE = "#FFFFFF", "#FFC93C"


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def letras(texto):
    return len(re.sub(r"[\W_]", "", texto))


def distribuir(frases, palavras):
    """Divide as palavras faladas de um bloco entre as frases, pela quantidade de letras.
    Funciona mesmo quando a voz separa as palavras de um jeito diferente do texto."""
    alvos = [letras(rot.falado(f)) for f in frases]
    escala = sum(letras(p["palavra"]) for p in palavras) / max(1, sum(alvos))
    resultado, i, acumulado, limite = [], 0, 0, 0
    for k, (frase, alvo) in enumerate(zip(frases, alvos)):
        limite += alvo * escala
        grupo = []
        ultima = k == len(frases) - 1
        while i < len(palavras) and (ultima or acumulado + letras(palavras[i]["palavra"]) / 2 <= limite):
            acumulado += letras(palavras[i]["palavra"])
            grupo.append(palavras[i])
            i += 1
        if not grupo:
            grupo = [palavras[min(i, len(palavras) - 1)]]
        resultado.append({
            "inicio": grupo[0]["inicio"], "fim": grupo[-1]["fim"],
            "marcacao": frase["marcacao"], "fontes": frase.get("fontes", []), "tela": frase.get("tela"),
            "rodape": frase.get("rodape", frase.get("fontes", [])),
        })
    return resultado


def tempos(roteiro, palavras):
    blocos = roteiro["bloco"]
    por_bloco = {n: [p for p in palavras if p["bloco"] == n] for n in range(1, len(blocos) + 1)}
    vazios = [n for n, lista in por_bloco.items() if not lista]
    if vazios:
        erro(f"o palavras.json não tem palavras dos blocos {vazios}; rode o roteiro.py texto e o narrar.py de novo.")
    total = round(palavras[-1]["fim"] + FOLGA_FINAL, 2)
    # O bloco 1 começa em 0; os outros, na primeira palavra deles (ESTRUTURA.md, regra 6.6).
    inicios = [0.0] + [por_bloco[n][0]["inicio"] for n in range(2, len(blocos) + 1)] + [total]
    return [{
        "numero": n, "nome": bloco["nome"], "inicio": inicios[n - 1], "fim": inicios[n],
        "duracao": round(inicios[n] - inicios[n - 1], 2),
        "frases": distribuir(bloco["frase"], por_bloco[n]),
    } for n, bloco in enumerate(blocos, 1)], total


def grupos_de_legenda(palavras):
    grupos, atual = [], []
    for p in palavras:
        if atual and (len(atual) == MAX_PALAVRAS
                      or sum(len(x["palavra"]) + 1 for x in atual) + len(p["palavra"]) > MAX_LETRAS
                      or p["inicio"] - atual[-1]["fim"] >= PAUSA_QUE_QUEBRA
                      or p["bloco"] != atual[-1]["bloco"]):
            grupos.append(atual)
            atual = []
        atual.append(p)
    if atual:
        grupos.append(atual)
    return grupos


def segundos(x):
    return f"{x:.2f}"


def gerar_legendas(palavras, total):
    grupos = grupos_de_legenda(palavras)
    elementos, quadros = [], []
    for g, grupo in enumerate(grupos):
        inicio = grupo[0]["inicio"]
        proximo = grupos[g + 1][0]["inicio"] if g + 1 < len(grupos) else total
        fim = min(proximo, grupo[-1]["fim"] + LEGENDA_SEGURA)
        spans = " ".join(f'<span id="leg-{g}-{k}" class="palavra">{html.escape(p["palavra"])}</span>'
                         for k, p in enumerate(grupo))
        elementos.append(f'    <div id="leg-{g}" class="clip legenda" data-start="{segundos(inicio)}" '
                         f'data-duration="{segundos(max(0.05, fim - inicio))}">{spans}</div>')
        for k, p in enumerate(grupo):
            apaga = grupo[k + 1]["inicio"] if k + 1 < len(grupo) else p["fim"]
            quadros.append([f"leg-{g}-{k}", round(p["inicio"], 2), round(apaga, 2)])
    return f"""<!-- Gerado pelo scripts/montar.py a partir do palavras.json. Não edite. -->
<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
    }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{chr(10).join(elementos)}
  </div>
  <script>
    // Cada palavra só entra quando é falada (e o grupo se recentraliza), fica amarela enquanto
    // é falada e depois volta ao branco.
    const PALAVRAS = {json.dumps(quadros)};
    const tl = gsap.timeline({{ paused: true }});
    for (const [id, inicio, fim] of PALAVRAS) {{
      tl.fromTo("#" + id, {{ display: "none", opacity: 0, color: "{TEXTO}" }},
        {{ display: "inline-block", opacity: 1, color: "{DESTAQUE}", duration: 0.06 }}, inicio);
      tl.to("#" + id, {{ color: "{TEXTO}", duration: 0.08 }}, fim);
    }}
    window.__timelines["legendas"] = tl;
  </script>
</template>
"""


def gerar_sobreposicoes(blocos, fontes, total):
    elementos = [f'    <div id="sob-selo" class="clip selo-ia" data-start="0" data-duration="{segundos(total)}">'
                 "Feito com auxílio de IA</div>"]
    n = 0
    for bloco in blocos:
        for frase in bloco["frases"]:
            if not frase["tela"] or not frase["rodape"]:  # premissa na tela não tem rodapé
                continue
            n += 1
            # Fica visível da frase até o fim do bloco: o número continua na tela nesse tempo.
            elementos.append(f'    <div id="sob-fonte-{n}" class="clip rodape-fonte" data-start="{segundos(frase["inicio"])}" '
                             f'data-duration="{segundos(bloco["fim"] - frase["inicio"])}">'
                             f'{html.escape(rot.rodape(frase["rodape"], fontes))}</div>')
    return f"""<!-- Gerado pelo scripts/montar.py a partir do roteiro e do palavras.json. Não edite. -->
<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
    }}
  </style>
  <div id="root" data-composition-id="sobreposicoes" data-width="1080" data-height="1920">
{chr(10).join(elementos)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    for (let n = 1; n <= {n}; n++) {{
      const el = document.getElementById("sob-fonte-" + n);
      tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.3 }}, parseFloat(el.dataset.start));
    }}
    window.__timelines["sobreposicoes"] = tl;
  </script>
</template>
"""


def gerar_tempos_js(blocos, total, estimado):
    dados = {"duracao": total, "estimado": estimado, "blocos": blocos}
    return f"""// Gerado pelo scripts/montar.py a partir do palavras.json. Não edite.
// TEMPOS.bloco(n) devolve os tempos do bloco n com as frases em tempo local (0 = começo do bloco),
// que é o tempo da timeline da cena. Para o hf-seek, que traz o tempo do vídeo inteiro, use
// inicioAbsoluto (palco.aoBuscar já faz isso).
window.TEMPOS = {json.dumps(dados, ensure_ascii=False, indent=2)};
window.TEMPOS.bloco = function (n) {{
  const b = this.blocos[n - 1];
  const local = (x) => Math.round((x - b.inicio) * 1000) / 1000;
  return {{
    numero: b.numero,
    nome: b.nome,
    inicioAbsoluto: b.inicio,
    duracao: b.duracao,
    frases: b.frases.map((f) => ({{ ...f, inicio: local(f.inicio), fim: local(f.fim) }})),
  }};
}};
"""


def modelo_de_cena(bloco):
    n = bloco["numero"]
    return f"""<!-- Cena do bloco {n} ({bloco["nome"]}). Modelo criado pelo scripts/montar.py: substitua pela cena de verdade.
     Os tempos vêm de TEMPOS.bloco({n}); não escreva segundos fixos. -->
<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      background: var(--fundo);
    }}
    #b{n}-titulo {{
      position: absolute;
      top: 820px;
      left: 0;
      width: calc(var(--largura) - var(--seguro-direita));
      text-align: center;
      color: var(--texto);
      font-family: var(--fonte);
      font-weight: var(--peso-titulo);
      font-size: 72px;
    }}
  </style>
  <div id="root" data-composition-id="bloco-{n}" data-width="1080" data-height="1920">
    <div id="b{n}-titulo">{html.escape(bloco["nome"])}</div>
  </div>
  <script>
    const B = TEMPOS.bloco({n});
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#b{n}-titulo", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0);
    window.__timelines["bloco-{n}"] = tl;
  </script>
</template>
"""


def gerar_index(blocos, total, volume, com_narracao):
    hosts = []
    for b in blocos:
        n = b["numero"]
        hosts.append(f'      <div id="bloco-{n}" data-composition-id="bloco-{n}" data-composition-src="cenas/bloco-{n}.html" '
                     f'data-start="{segundos(b["inicio"])}" data-duration="{segundos(b["duracao"])}" '
                     f'data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" '
                     f'style="z-index: {n}"></div>')
    for nome, faixa, tipo, z in (("sobreposicoes", 2, "graphics", 20), ("legendas", 3, "captions", 30)):
        hosts.append(f'      <div id="{nome}" data-composition-id="{nome}" data-composition-src="cenas/{nome}.html" '
                     f'data-start="0" data-duration="{segundos(total)}" data-track-index="{faixa}" '
                     f'data-track-kind="{tipo}" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
    if com_narracao:
        hosts.append(f'      <audio id="narracao" src="narracao/narracao.mp3" data-start="0" '
                     f'data-volume="{volume}" data-track-index="4"></audio>')
    folhas = "\n".join(f'    <link rel="stylesheet" href="componentes/{c}" />' for c in (
        "tema.css", "legendas/legendas.css", "rodape-fonte/rodape-fonte.css", "selo-ia/selo-ia.css",
        "contador/contador.css", "cartoes/cartoes.css"))
    return f"""<!doctype html>
<!-- Gerado pelo scripts/montar.py a partir do roteiro e do palavras.json. Não edite: rode o montar.py de novo. -->
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
{folhas}
    <script src="assets/libs/gsap.min.js"></script>
    <script src="tempos.js"></script>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{segundos(total)}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    pasta = Path(sys.argv[1]).resolve()

    roteiro = rot.checar(pasta)
    if rot.erros:
        for e in rot.erros:
            print(f"  ERRO  {e}", file=sys.stderr)
        erro("o roteiro tem erros; corrija com o roteiro.py checar antes de montar.")
    arquivo_palavras = pasta / "narracao" / "palavras.json"
    if not arquivo_palavras.is_file():
        erro("falta o narracao/palavras.json; rode o roteiro.py texto e o narrar.py.")
    palavras = json.loads(arquivo_palavras.read_text(encoding="utf-8"))
    estimado = (pasta / "narracao" / "ESTIMADO").exists()
    com_narracao = (pasta / "narracao" / "narracao.mp3").is_file() and not estimado

    blocos, total = tempos(roteiro, palavras)
    comp = pasta / "composicao"
    (comp / "cenas").mkdir(parents=True, exist_ok=True)

    # Mantém o volume que o ajustar-volume.sh já acertou, se houver.
    volume = "1"
    index = comp / "index.html"
    if index.is_file():
        achado = re.search(r'id="narracao"[^>]*data-volume="([0-9.]+)"', index.read_text(encoding="utf-8"))
        if achado:
            volume = achado.group(1)

    criadas = []
    for b in blocos:
        cena = comp / "cenas" / f"bloco-{b['numero']}.html"
        if not cena.exists():
            cena.write_text(modelo_de_cena(b), encoding="utf-8")
            criadas.append(cena.name)

    index.write_text(gerar_index(blocos, total, volume, com_narracao), encoding="utf-8")
    (comp / "tempos.js").write_text(gerar_tempos_js(blocos, total, estimado), encoding="utf-8")
    (comp / "cenas" / "legendas.html").write_text(gerar_legendas(palavras, total), encoding="utf-8")
    (comp / "cenas" / "sobreposicoes.html").write_text(gerar_sobreposicoes(blocos, roteiro["_fontes"], total),
                                                       encoding="utf-8")

    print(f"Composição montada: {total:.1f} s, {len(blocos)} blocos.")
    for b in blocos:
        print(f"  Bloco {b['numero']} ({b['nome']}): {b['inicio']:.2f}–{b['fim']:.2f} s")
    if estimado:
        print("  AVISO tempos ESTIMADOS e sem narração: rode o narrar.py e o montar.py de novo quando houver voz.")
    elif com_narracao and volume == "1":
        print("  Próximo passo: ./scripts/ajustar-volume.sh para acertar o volume da narração.")
    if criadas:
        print(f"  Cenas criadas como modelo (substitua pelas de verdade): {', '.join(criadas)}")


if __name__ == "__main__":
    main()
