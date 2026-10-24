#!/usr/bin/env python3
"""Confere o roteiro estruturado de um vídeo e gera os arquivos derivados (ESTRUTURA.md, seção 8).

Uso: python3 scripts/roteiro.py checar videos/AAAA-MM-DD-slug
         confere o 03-roteiro.toml contra as regras do canal e o 02-fontes.md,
         e gera o 03-roteiro.md para leitura
     python3 scripts/roteiro.py texto videos/AAAA-MM-DD-slug
         confere e, se não houver erro, gera o narracao/texto.txt para o narrar.py
"""

import re
import sys
import unicodedata
from pathlib import Path

if sys.version_info < (3, 11):
    sys.exit("ERRO: o roteiro.py precisa do Python 3.11 ou mais novo (usa o tomllib).")

import tomllib  # noqa: E402

BLOCOS = ["Gancho", "Contexto", "O que mudaria", "A balança", "Exemplo real", "Encerramento"]
OPCIONAIS = {"Exemplo real"}
MARCACOES = ["FATO", "PROJEÇÃO", "PREMISSA", "ARGUMENTO A FAVOR", "ARGUMENTO CONTRA", "TERMÔMETRO", "BORDÃO"]
SEM_FONTE = {"BORDÃO", "PREMISSA"}  # bordões e premissas do cenário (01-ideia.md) não citam dado

BORDAO_ABERTURA = re.compile(r"^E se .+\? Vamos imaginar\.$")
BORDAO_BALANCA = "Agora, vamos colocar na balança."
BORDAO_ENCERRAMENTO = "E aí, você toparia? Me conta nos comentários."

# Estimativa grosseira da voz (pt-BR-AntonioNeural a +10%); a duração real sai do palavras.json.
PALAVRAS_POR_SEGUNDO = 2.8
DURACAO_MIN, DURACAO_MAX = 45, 90
EQUILIBRIO_MIN, EQUILIBRIO_MAX = 0.8, 1.25  # razão de palavras entre os dois lados

erros = []
avisos = []


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def marcacao_canonica(valor):
    alvo = sem_acento(str(valor)).upper().strip()
    return next((m for m in MARCACOES if sem_acento(m) == alvo), None)


def palavras(texto):
    return len(re.findall(r"[\wÀ-ÿ$%]+", texto))


def falado(frase):
    return frase.get("voz") or frase.get("fala", "")


def ler_fontes(caminho):
    """Lê a tabela do 02-fontes.md: {código: {"link": ..., "acessado": ...}}."""
    fontes = {}
    if not caminho.is_file():
        return fontes
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) >= 7 and re.fullmatch(r"F\d+", celulas[0]):
            fontes[celulas[0]] = {"fonte": celulas[3], "link": celulas[4],
                                  "data": celulas[5], "acessado": celulas[6]}
    return fontes


def vazio(valor):
    return not valor or valor.strip() in {"...", "-", "—"}


def checar(pasta):
    toml = pasta / "03-roteiro.toml"
    if not toml.is_file():
        erros.append(f"não encontrei {toml}")
        return None
    try:
        roteiro = tomllib.loads(toml.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        erros.append(f"03-roteiro.toml não é um TOML válido: {e}")
        return None

    fontes = ler_fontes(pasta / "02-fontes.md")
    if not fontes:
        erros.append("02-fontes.md sem nenhuma fonte na tabela (| F1 | ... |)")

    if vazio(roteiro.get("titulo", "")) or "[" in roteiro.get("titulo", ""):
        erros.append("falta o título do roteiro")
    blocos = roteiro.get("bloco", [])

    # Blocos: nomes conhecidos, na ordem, com os obrigatórios presentes
    nomes = [b.get("nome", "") for b in blocos]
    desconhecidos = [n for n in nomes if n not in BLOCOS]
    if desconhecidos:
        erros.append(f"blocos com nome fora da lista {BLOCOS}: {desconhecidos}")
    elif nomes != [n for n in BLOCOS if n in nomes]:
        erros.append(f"blocos fora da ordem: {nomes}")
    faltando = [n for n in BLOCOS if n not in nomes and n not in OPCIONAIS]
    if faltando:
        erros.append(f"faltam os blocos: {faltando}")

    usadas = set()
    for numero, bloco in enumerate(blocos, 1):
        nome = bloco.get("nome", f"bloco {numero}")
        frases = bloco.get("frase", [])
        if not frases:
            erros.append(f"{nome}: nenhuma frase")
        for k, frase in enumerate(frases, 1):
            onde = f"{nome}, frase {k}"
            if vazio(frase.get("fala", "")):
                erros.append(f"{onde}: falta a fala")
            elif re.search(r"\[[^\]]+\]", frase["fala"]):
                erros.append(f"{onde}: ainda tem texto de modelo entre colchetes")
            marcacao = marcacao_canonica(frase.get("marcacao", ""))
            if marcacao is None:
                erros.append(f"{onde}: marcação '{frase.get('marcacao', '')}' inválida (use {MARCACOES})")
                continue
            frase["marcacao"] = marcacao
            codigos = frase.get("fontes", [])
            if marcacao not in SEM_FONTE and not codigos:
                erros.append(f"{onde}: [{marcacao}] precisa de fonte (códigos do 02-fontes.md)")
            for codigo in codigos:
                usadas.add(codigo)
                if codigo not in fontes:
                    erros.append(f"{onde}: fonte {codigo} não está no 02-fontes.md")
            if marcacao.startswith("ARGUMENTO") and nome != "A balança":
                erros.append(f"{onde}: argumentos de um lado só entram no bloco A balança")
            if marcacao == "TERMÔMETRO" and nome != "A balança":
                erros.append(f"{onde}: o termômetro fica no bloco A balança")
            if re.search(r"\d", frase.get("fala", "")) and not frase.get("voz"):
                avisos.append(f"{onde}: a fala tem algarismos e não tem 'voz'; "
                              "escreva como a voz deve ler, por extenso")
            if frase.get("tela") and not codigos:
                erros.append(f"{onde}: texto na tela sem fonte para o rodapé")
            # "rodape" escolhe, entre as fontes da frase, só as que sustentam o texto da tela.
            if "rodape" in frase:
                if not frase.get("tela"):
                    erros.append(f"{onde}: 'rodape' só serve para frase com 'tela'")
                elif not frase["rodape"] or not set(frase["rodape"]) <= set(codigos):
                    erros.append(f"{onde}: 'rodape' precisa ser parte das fontes da frase ({codigos})")

    for codigo in sorted(usadas):
        f = fontes.get(codigo)
        if f and (vazio(f["link"]) or vazio(f["acessado"])):
            erros.append(f"fonte {codigo}: falta link ou data de acesso no 02-fontes.md")
        elif f and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["acessado"]):
            # "Acessado em" só leva a data (AAAA-MM-DD): fonte não conferida não entra no vídeo.
            erros.append(f"fonte {codigo}: 'Acessado em' precisa ser só a data (AAAA-MM-DD), "
                         f"não '{f['acessado']}'; fonte não conferida fica de fora do roteiro")

    por_nome = {b.get("nome"): b.get("frase", []) for b in blocos}
    marcadas = lambda nome, m: [f for f in por_nome.get(nome, []) if f.get("marcacao") == m]  # noqa: E731

    # Bordões
    if not any(BORDAO_ABERTURA.match(f.get("fala", "")) for f in marcadas("Gancho", "BORDÃO")):
        erros.append('Gancho: falta o bordão "E se [tema]? Vamos imaginar." marcado como [BORDÃO]')
    if not any(f.get("fala") == BORDAO_BALANCA for f in marcadas("A balança", "BORDÃO")):
        erros.append(f'A balança: falta o bordão "{BORDAO_BALANCA}"')
    final = por_nome.get("Encerramento", [])
    if not final or final[-1].get("fala") != BORDAO_ENCERRAMENTO:
        erros.append(f'Encerramento: a última frase precisa ser o bordão "{BORDAO_ENCERRAMENTO}"')

    # Balança: mesmo número de frases, tamanho parecido e um termômetro
    a_favor = marcadas("A balança", "ARGUMENTO A FAVOR")
    contra = marcadas("A balança", "ARGUMENTO CONTRA")
    if "A balança" in por_nome:
        if not a_favor or not contra:
            erros.append("A balança: precisa de pelo menos um argumento a favor e um contra")
        elif len(a_favor) != len(contra):
            erros.append(f"A balança: {len(a_favor)} frase(s) a favor e {len(contra)} contra; "
                         "precisam ser iguais")
        else:
            pf = sum(palavras(falado(f)) for f in a_favor)
            pc = sum(palavras(falado(f)) for f in contra)
            if not EQUILIBRIO_MIN <= pf / pc <= EQUILIBRIO_MAX:
                erros.append(f"A balança: {pf} palavras a favor e {pc} contra; o tempo precisa ser parecido "
                             f"(razão entre {EQUILIBRIO_MIN} e {EQUILIBRIO_MAX})")
    termometros = [f for b in blocos for f in b.get("frase", []) if f.get("marcacao") == "TERMÔMETRO"]
    if len(termometros) != 1:
        erros.append(f"o roteiro precisa de exatamente um [TERMÔMETRO] (tem {len(termometros)})")

    # Duração estimada
    total = sum(palavras(falado(f)) for b in blocos for f in b.get("frase", []))
    estimativa = total / PALAVRAS_POR_SEGUNDO
    if not DURACAO_MIN <= estimativa <= DURACAO_MAX:
        avisos.append(f"duração estimada {estimativa:.0f} s fora de {DURACAO_MIN}–{DURACAO_MAX} s "
                      "(estimativa; a real sai da narração)")
    # CLAUDE.md, seção 3: o impacto nos primeiros 3 s (o bordão vem logo depois e leva ~3 s
    # sozinho) e o encerramento nos últimos 5 s. Limites com folga, porque são estimativas.
    gancho = por_nome.get("Gancho", [])
    if gancho:
        segundos = palavras(falado(gancho[0])) / PALAVRAS_POR_SEGUNDO
        if segundos > 4:
            avisos.append(f"Gancho: a primeira frase (o impacto) leva cerca de {segundos:.0f} s; "
                          "o ideal é até 3 s")
    for nome, limite in (("Gancho", 8), ("Encerramento", 6)):
        segundos = sum(palavras(falado(f)) for f in por_nome.get(nome, [])) / PALAVRAS_POR_SEGUNDO
        if segundos > limite:
            avisos.append(f"{nome}: cerca de {segundos:.0f} s de fala; o ideal é até {limite} s")

    roteiro["_fontes"] = fontes
    roteiro["_palavras"] = total
    return roteiro


def rodape(codigos, fontes):
    """Texto do rodapé de fonte ("Fonte: IBGE, 2025"), igual no 03-roteiro.md e no vídeo."""
    # A mesma fonte citada por vários códigos aparece uma vez só ("Banco Central, 2024, 2025").
    anos_por_fonte = {}
    for c in codigos:
        f = fontes.get(c, {})
        anos = anos_por_fonte.setdefault(f.get("fonte", c), [])
        ano = re.search(r"\d{4}(?:[–-]\d{4})?", f.get("data", ""))
        if ano and ano.group(0) not in anos:
            anos.append(ano.group(0))
    return "Fonte: " + "; ".join(", ".join([nome] + anos) for nome, anos in anos_por_fonte.items())


def gerar_md(pasta, roteiro):
    blocos = roteiro.get("bloco", [])
    total = roteiro["_palavras"]
    linhas = [
        "<!-- Gerado pelo scripts/roteiro.py a partir do 03-roteiro.toml. Não edite este arquivo. -->",
        f"# Roteiro — {roteiro.get('titulo', '')}",
        f"Versão: {roteiro.get('versao', '?')} · Duração estimada: ~{total / PALAVRAS_POR_SEGUNDO:.0f} s "
        f"({total} palavras faladas)",
        "",
    ]
    for numero, bloco in enumerate(blocos, 1):
        frases = bloco.get("frase", [])
        segundos = sum(palavras(falado(f)) for f in frases) / PALAVRAS_POR_SEGUNDO
        linhas += [f"## Bloco {numero} — {bloco.get('nome', '')} (~{segundos:.0f} s)",
                   f"Cena: {bloco.get('cena', '')}", ""]
        for frase in frases:
            codigos = frase.get("fontes", [])
            etiqueta = frase.get("marcacao", "?") + (f" · {', '.join(codigos)}" if codigos else "")
            linhas.append(f"- **[{etiqueta}]** {frase.get('fala', '')}")
            detalhes = []
            if frase.get("tela"):
                detalhes.append(f"Tela: {frase['tela']} "
                                f"(rodapé: {rodape(frase.get('rodape', codigos), roteiro['_fontes'])})")
            if frase.get("voz"):
                detalhes.append(f"Voz: \"{frase['voz']}\"")
            if detalhes:
                linhas.append(f"  - {' · '.join(detalhes)}")
        linhas.append("")
    balanca = next((b for b in blocos if b.get("nome") == "A balança"), {}).get("frase", [])
    lado = lambda m: [f for f in balanca if f.get("marcacao") == m]  # noqa: E731
    pf = sum(palavras(falado(f)) for f in lado("ARGUMENTO A FAVOR"))
    pc = sum(palavras(falado(f)) for f in lado("ARGUMENTO CONTRA"))
    linhas += ["## Equilíbrio da balança",
               f"- A favor: {len(lado('ARGUMENTO A FAVOR'))} frase(s), {pf} palavras",
               f"- Contra: {len(lado('ARGUMENTO CONTRA'))} frase(s), {pc} palavras", ""]
    (pasta / "03-roteiro.md").write_text("\n".join(linhas), encoding="utf-8")


def gerar_texto(pasta, roteiro):
    linhas = []
    for numero, bloco in enumerate(roteiro.get("bloco", []), 1):
        linhas.append(f"[BLOCO {numero}]")
        linhas += [falado(f) for f in bloco.get("frase", [])]
        linhas.append("")
    destino = pasta / "narracao" / "texto.txt"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")
    return destino


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in {"checar", "texto"}:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    comando, pasta = sys.argv[1], Path(sys.argv[2])

    roteiro = checar(pasta)
    if roteiro is not None:
        gerar_md(pasta, roteiro)
    for aviso in avisos:
        print(f"  AVISO {aviso}")
    for erro in erros:
        print(f"  ERRO  {erro}")
    if erros:
        print(f"\n{len(erros)} erro(s) no roteiro.")
        sys.exit(1)

    print(f"Roteiro ok: {roteiro['_palavras']} palavras, "
          f"~{roteiro['_palavras'] / PALAVRAS_POR_SEGUNDO:.0f} s estimados. 03-roteiro.md atualizado.")
    if comando == "texto":
        print(f"Gerado {gerar_texto(pasta, roteiro)}")


if __name__ == "__main__":
    main()
