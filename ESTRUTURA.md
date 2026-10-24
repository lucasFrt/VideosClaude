# ESTRUTURA.md — Guia técnico de execução

Este arquivo é o manual técnico do projeto. O `CLAUDE.md` define **o que** o canal é (tom, visual, ondas de revisão); este arquivo define **como** construir: pastas, skills, componentes, scripts, comandos e verificações. Em caso de conflito, o `CLAUDE.md` vale para conteúdo e este arquivo vale para técnica.

Regra geral: **não improvise o que já está definido aqui.** Se algo aqui estiver errado ou impossível na prática, não contorne em silêncio: registre o problema em `docs/aprendizados.md`, proponha a correção e me avise.

---

## 1. Ferramentas (todas gratuitas)

| Ferramenta | Para quê | Observação |
|---|---|---|
| Node.js 20+ | Rodar o HyperFrames | Instalar se não existir |
| HyperFrames | Montar e renderizar o vídeo a partir de HTML | Código aberto, da HeyGen |
| Skills do HyperFrames | Ensinar o Claude Code a usar o framework | `npx skills add heygen-com/hyperframes` |
| GSAP | Animações 2D (textos, contadores, transições) | Copiar o arquivo para `assets/libs/` |
| Three.js | Cenas 3D (Zé, balança, cidade) | Copiar o arquivo para `assets/libs/` |
| Python 3.10+ e edge-tts | Narração em pt-BR com tempos de cada palavra | `pip install edge-tts` |
| FFmpeg | Codificação do vídeo | Já usado por baixo do HyperFrames |

Não use nenhum serviço pago, chave de API paga nem ferramenta que exija login. Se uma skill ou recurso do HyperFrames depender de serviço pago (por exemplo, voz sintética da HeyGen), não use: a narração é sempre feita pelo `scripts/narrar.py`.

---

## 2. Instalação inicial (executar uma única vez)

1. Verifique as versões: `node -v`, `python3 --version`, `ffmpeg -version`. Instale o que faltar.
2. Na raiz do projeto, instale as skills: `npx skills add heygen-com/hyperframes`.
3. Liste onde as skills foram instaladas e **leia o SKILL.md de cada uma antes de escrever qualquer composição**, principalmente `hyperframes`, `hyperframes-core` e `hyperframes-cli`.
4. Rode o diagnóstico do framework (`npx hyperframes doctor`) e corrija o que ele apontar.
5. Instale a narração: `pip install edge-tts`.
6. Baixe e salve localmente, com versão fixa: `three.min.js` e `gsap.min.js` em `assets/libs/`, e a fonte Montserrat (ExtraBold e SemiBold, licença OFL) em `assets/fontes/`. Registre as versões em `docs/versoes.md`.
7. Crie toda a estrutura de pastas da seção 3, com os arquivos-modelo da seção 7.
8. Construa os componentes da seção 5 e o vídeo de teste da seção 10 antes do primeiro vídeo real.

**Por que tudo local:** a renderização precisa ser determinística e funcionar offline. Nada de carregar bibliotecas, fontes ou imagens da internet durante o render.

---

## 3. Estrutura de pastas

```
meu-canal/
├── CLAUDE.md                  # identidade do canal e ondas de revisão
├── ESTRUTURA.md               # este arquivo
├── .claude/
│   ├── agents/
│   │   └── critico.md         # subagente das ondas 3 e 4
│   └── skills/                # skills do HyperFrames (instaladas pelo npx skills)
├── assets/
│   ├── libs/                  # three.min.js, gsap.min.js (versões fixas)
│   ├── fontes/                # Montserrat ExtraBold e SemiBold
│   └── sons/                  # efeitos e trilhas livres de direitos, com licença anotada
├── componentes/
│   ├── tema.css               # paleta, fontes, tamanhos e áreas seguras
│   ├── ze/                    # personagem 3D original
│   ├── balanca/               # balança 3D do bloco "A balança"
│   ├── cidade/                # cenário low-poly reutilizável
│   ├── legendas/              # legendas sincronizadas por palavra
│   ├── contador/              # números animados
│   ├── rodape-fonte/          # fonte do dado no canto da tela
│   └── selo-ia/               # aviso "Feito com auxílio de IA"
├── modelos/                   # modelos em branco de cada arquivo de vídeo
│   ├── 01-ideia.md
│   ├── 02-fontes.md
│   ├── 03-roteiro.md
│   ├── 04-revisoes.md
│   └── status.md
├── scripts/
│   ├── novo-video.sh          # cria a pasta de um vídeo a partir de modelos/
│   ├── narrar.py              # gera narração e palavras.json
│   └── verificar.sh           # checagens técnicas do vídeo final
├── videos/
│   └── AAAA-MM-DD-slug/       # uma pasta por vídeo (ver seção 4)
└── docs/
    ├── temas.md               # fila de ideias de temas
    ├── aprendizados.md        # o que deu errado e como foi resolvido
    └── versoes.md             # versões das ferramentas e bibliotecas
```

---

## 4. Pasta de cada vídeo

Nome: `videos/AAAA-MM-DD-slug/` (ex.: `videos/2026-10-26-parar-de-imprimir-dinheiro/`). O slug é curto, em minúsculas, sem acentos e com hífens.

```
videos/2026-10-26-parar-de-imprimir-dinheiro/
├── status.md                  # em que onda/etapa o vídeo está
├── 01-ideia.md                # onda 1
├── 02-fontes.md               # onda 2
├── 03-roteiro.md              # onda 2, atualizado nas ondas 4
├── 04-revisoes.md             # registro do debate das ondas 3 e 4
├── narracao/
│   ├── texto.txt              # só o texto falado, extraído do roteiro aprovado
│   ├── narracao.mp3
│   └── palavras.json          # tempo de início e fim de cada palavra
├── composicao/
│   ├── index.html             # composição HyperFrames do vídeo
│   └── cenas/                 # sub-composições, uma por bloco do roteiro
├── previa.mp4                 # render de baixa resolução para a revisão 2
└── final.mp4                  # render final
```

### status.md

Atualize sempre que mudar de etapa. Se a sessão for interrompida, a próxima sessão começa lendo este arquivo e continua de onde parou, sem refazer etapas aprovadas.

```
etapa_atual: onda-3-rodada-2
aprovado_roteiro: nao
aprovado_previa: nao
ultima_atualizacao: AAAA-MM-DD HH:MM
pendencias:
  - ...
```

Etapas possíveis, em ordem: `onda-1`, `onda-2`, `onda-3-rodada-N`, `onda-4-rodada-N`, `revisao-humana-1`, `narracao`, `previa`, `revisao-humana-2`, `final`, `concluido`.

---

## 5. Componentes reutilizáveis

Cada pasta de `componentes/` tem: o código (`.js` e/ou `.html`), um `LEIAME.md` curto com parâmetros e exemplo de uso, e uma imagem de referência (`referencia.png`) gerada a partir de um quadro renderizado. Os vídeos **importam** os componentes; nunca copie e altere um componente dentro da pasta de um vídeo. Se precisar de variação, adicione um parâmetro ao componente.

### tema.css
- Variáveis de cor: `--fundo: #1B2A41`, `--destaque: #FFC93C`, `--positivo: #3DDC97`, `--negativo: #FF6B6B`, `--texto: #FFFFFF`.
- Fontes: Montserrat ExtraBold para legendas e títulos, SemiBold para rodapés.
- Formato: 1080x1920, 30 fps.
- **Área segura** (onde a interface do Instagram, TikTok e Shorts não cobre): nenhum texto importante nos 220 px do topo, nos 420 px de baixo e nos 140 px da direita. Defina isso como variáveis e use em todos os componentes.

### ze/
- Personagem 3D low-poly ORIGINAL: corpo simples de cilindros e esferas, camiseta amarela (`--destaque`), calça azul, cabelo curto escuro, olhos de pontos. Não pode lembrar nenhum personagem conhecido.
- Parâmetros: posição, escala, expressão (`neutro`, `feliz`, `preocupado`, `surpreso`), gesto (`parado`, `aponta`, `ombros`, `comemora`).
- Animações sempre em função do tempo da composição (ver seção 6).

### balanca/
- Balança 3D com prato verde (`--positivo`) à esquerda e coral (`--negativo`) à direita.
- Parâmetros: inclinação de −1 a 1, rótulos de cada prato, tempo de entrada.
- Começa sempre equilibrada (inclinação 0). Só inclina se o roteiro tiver uma marcação explícita para isso; por padrão, termina equilibrada, para não sugerir veredito.

### cidade/
- Cenário low-poly de quarteirões, com lojas, banco, casas e uma vitrine de preços.
- Parâmetros: hora do dia, densidade de pessoas, preços na vitrine e letreiros (texto genérico, sem marcas reais).

### legendas/
- Lê `palavras.json` e mostra de 1 a 4 palavras por vez, centralizadas na área segura.
- A palavra sendo falada fica em `--destaque`, e as outras em `--texto`, com contorno escuro para legibilidade.
- Nunca quebra uma palavra no meio e nunca mostra palavra antes de ela ser falada.

### contador/
- Número animado de um valor a outro, com formatação brasileira (`R$ 1.234,56`, `12,5%`).
- Parâmetros: valor inicial, valor final, prefixo, sufixo, casas decimais, duração, cor.

### rodape-fonte/
- Texto pequeno no canto inferior esquerdo, dentro da área segura: `Fonte: IBGE, 2026`.
- Aparece sempre que um número da tela vier de uma fonte e fica visível enquanto o número estiver na tela.

### selo-ia/
- Pequeno selo fixo "Feito com auxílio de IA" no canto superior esquerdo, dentro da área segura, durante todo o vídeo.

---

## 6. Regras técnicas do HyperFrames

1. **Leia as skills antes de escrever.** O formato das composições (atributos `data-*`, trilhas, clipes, sub-composições, variáveis) é definido pela skill `hyperframes-core`. Siga exatamente o que ela documenta e não invente atributos.
2. **Tudo controlado pelo tempo da composição.** Nenhuma animação pode depender do relógio do navegador (`requestAnimationFrame` livre, `setInterval`, `Date.now()`, `performance.now()`). Animações GSAP devem estar em timelines que o framework consiga posicionar em qualquer instante, conforme a skill indica.
3. **Three.js determinístico.** Cada quadro 3D é calculado a partir do tempo atual da composição: dado o tempo `t`, a cena é posicionada e renderizada para aquele `t`. Sem física acumulada quadro a quadro, sem estado que dependa do quadro anterior.
4. **Aleatoriedade com semente fixa.** Se usar números aleatórios (pessoas na cidade, confetes), use um gerador com semente fixa, para o mesmo vídeo sair igual em todo render.
5. **Sem rede no render.** Bibliotecas, fontes, sons e imagens vêm de `assets/` ou do próprio componente.
6. **Duração vem da narração.** A duração de cada cena é calculada a partir de `palavras.json`: cada bloco do roteiro começa na primeira palavra do bloco e termina na primeira palavra do bloco seguinte (o último bloco ganha 1,5 s extras no final).
7. **Valide antes de renderizar.** Rode o lint e a validação do HyperFrames após qualquer alteração e corrija todos os erros antes de gerar a prévia.

### Comandos principais (confirmar nomes e opções na skill `hyperframes-cli`)

```
npx hyperframes init <pasta>      # criar composição nova
npx hyperframes lint              # checar erros de composição
npx hyperframes validate          # validar antes do render
npx hyperframes preview           # pré-visualizar no navegador
npx hyperframes render            # gerar MP4
npx hyperframes doctor            # diagnosticar o ambiente
```

- **Prévia:** resolução reduzida (ex.: 540x960) para ser rápida.
- **Final:** 1080x1920, 30 fps, H.264, áudio AAC.

---

## 7. Modelos de arquivo (pasta `modelos/`)

### 01-ideia.md
```
# E se [pergunta]?

## A pergunta exata
O que muda, a partir de quando, em que escala, e o que fica igual.

## Premissas assumidas
- ...

## Simplificações (o vídeo precisa dizer quais são)
- ...

## Perguntas que o vídeo precisa responder
- ...

## Por que este cenário é plausível no Brasil real
...
```

### 02-fontes.md
```
| # | Dado | Valor | Fonte | Link | Data do dado | Acessado em |
|---|------|-------|-------|------|--------------|-------------|
| F1 | ... | ... | ... | ... | ... | ... |

## Posições de especialistas
- A favor: [quem, o quê, link]
- Contra: [quem, o quê, link]
- Onde há consenso: ...
- Onde há disputa: ...
```

### 03-roteiro.md
```
# Roteiro — E se [pergunta]?
Versão: N (atualizar a cada rodada)
Duração estimada: XX s

## Bloco 1 — Gancho (0–3s)
Fala: "E se [tema]? Vamos imaginar."
Marcação: [FATO|PROJEÇÃO|ARGUMENTO A FAVOR|ARGUMENTO CONTRA] + fonte (F1, F2...)
Cena: componentes usados e o que acontece na tela
Texto na tela: números e rodapé de fonte

## Bloco 2 — Contexto
...

## Bloco 4 — A balança
(os dois lados com o mesmo número de frases e tempo semelhante)
...

## Bloco 6 — Encerramento
Fala: "E aí, você toparia? Me conta nos comentários."
```

### 04-revisoes.md
```
# Revisões

## Rodada 1
### O que o crítico considerou sólido
- ...
### Objeções
| # | Trecho | Nível | Objeção | Base | Resposta do autor | Decisão |
|---|--------|-------|---------|------|-------------------|---------|
| R1.1 | ... | CRÍTICA | ... | ... | ... | aceita / rejeitada (motivo) |
### Veredito do crítico
...

## Rodada 2
...

## Resumo final para a revisão humana
- O que mudou:
- O que ficou em aberto:
```

### status.md
Conforme a seção 4.

---

## 8. Scripts

### scripts/novo-video.sh
- Recebe o slug: `./scripts/novo-video.sh parar-de-imprimir-dinheiro`.
- Cria `videos/AAAA-MM-DD-slug/` com a data de hoje, copia os modelos e as subpastas `narracao/` e `composicao/`, e inicia o `status.md` em `onda-1`.

### scripts/narrar.py
- Recebe a pasta do vídeo, lê `narracao/texto.txt` e gera `narracao.mp3` e `palavras.json` com o edge-tts.
- Voz fixa: `pt-BR-AntonioNeural`, ritmo `+10%`. Nunca mude sem minha autorização.
- Use os eventos de limite de palavra do edge-tts para obter o tempo de cada palavra. Se a versão instalada só emitir limites de frase por padrão, configure para emitir limites de palavra.
- Formato do `palavras.json`: lista de `{ "palavra": "...", "inicio": 0.00, "fim": 0.00, "bloco": N }`, em segundos.
- O `texto.txt` marca o início de cada bloco com uma linha `[BLOCO N]`, que o script usa para preencher o campo `bloco` e não envia para a voz.
- Números são escritos por extenso no `texto.txt` quando a voz puder lê-los errado (ex.: "R$ 1,5 trilhão" → "um vírgula cinco trilhão de reais"). A versão em algarismos fica só na tela.

### scripts/verificar.sh
Roda no `final.mp4` e falha se algo estiver fora do padrão:
- Resolução 1080x1920 e 30 fps.
- Duração entre 45 e 60 s.
- Existe trilha de áudio e a narração não está cortada no fim.
- Volume da narração normalizado (aprox. −14 LUFS) e trilha de fundo, se existir, bem mais baixa que a voz.
- Gera 6 quadros de amostra em `videos/.../amostras/` para conferência visual.

---

## 9. Checklist antes de cada revisão humana

**Revisão 1 (roteiro):**
- [ ] Todo número do roteiro tem código de fonte (F1, F2...) e está no `02-fontes.md`.
- [ ] Toda frase tem marcação de FATO, PROJEÇÃO ou ARGUMENTO.
- [ ] Os blocos a favor e contra têm o mesmo número de frases e tempo semelhante.
- [ ] As ondas 3 e 4 terminaram sem objeção CRÍTICA ou IMPORTANTE pendente.
- [ ] Bordões de abertura, transição e encerramento estão presentes.

**Revisão 2 (prévia):**
- [ ] Narração, legendas e cenas estão sincronizadas.
- [ ] Todo número na tela tem rodapé de fonte e bate com o roteiro aprovado.
- [ ] Nenhum texto fora da área segura.
- [ ] Selo de IA visível do início ao fim.
- [ ] Nenhuma pessoa real, marca, logotipo ou personagem conhecido na tela.
- [ ] A balança termina equilibrada (salvo marcação explícita no roteiro).
- [ ] `verificar.sh` passou sem erros (no final).

---

## 10. Vídeo de teste (antes do primeiro vídeo real)

Crie `videos/AAAA-MM-DD-teste/` com 15 segundos usando todos os componentes: o Zé entra na cidade, um contador vai de R$ 10,00 a R$ 15,00 na vitrine com rodapé de fonte fictícia marcada como "(teste)", a balança aparece equilibrada e as legendas acompanham uma narração curta gerada pelo `narrar.py`. Renderize a prévia e o final, rode o `verificar.sh` duas vezes e confirme que os dois renders saíram idênticos (determinismo). Só depois disso comece o primeiro tema real.

---

## 11. Ordem de execução de um vídeo

1. `./scripts/novo-video.sh <slug>`
2. Ondas 1 e 2 (`01-ideia.md`, `02-fontes.md`, `03-roteiro.md`).
3. Ondas 3 e 4 com o subagente `critico`, registrando tudo em `04-revisoes.md`, até no máximo 4 rodadas.
4. 🛑 Revisão humana 1. Parar e esperar.
5. Extrair o texto falado do roteiro aprovado para `narracao/texto.txt` e rodar `scripts/narrar.py`.
6. Montar `composicao/` com os componentes, rodar lint e validação.
7. Renderizar `previa.mp4`.
8. 🛑 Revisão humana 2. Parar e esperar.
9. Renderizar `final.mp4`, rodar `verificar.sh`, conferir as amostras.
10. Marcar `status.md` como `concluido` e registrar em `docs/aprendizados.md` qualquer problema que tenha aparecido.

Se eu pedir mudança no roteiro depois da revisão 1, volte às ondas 3 e 4 só para os trechos alterados antes de seguir.
