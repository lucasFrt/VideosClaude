# ESTRUTURA.md — Guia técnico de execução

Este arquivo é o manual técnico do projeto. O `CLAUDE.md` define **o que** o canal é (tom, visual, ondas de revisão); este arquivo define **como** construir: pastas, skills, componentes, scripts, comandos e verificações. Em caso de conflito, o `CLAUDE.md` vale para conteúdo e este arquivo vale para técnica.

Regra geral: **não improvise o que já está definido aqui.** Se algo aqui estiver errado ou impossível na prática, não contorne em silêncio: registre o problema em `docs/aprendizados.md`, proponha a correção e me avise.

---

## 1. Ferramentas (todas gratuitas)

| Ferramenta | Para quê | Observação |
|---|---|---|
| Node.js 22+ | Rodar o HyperFrames | Instalar se não existir (o HyperFrames exige 22+) |
| HyperFrames | Montar e renderizar o vídeo a partir de HTML | Código aberto, da HeyGen; versão fixa no `package.json`, sempre via `scripts/hf.sh` |
| Skills do HyperFrames | Ensinar o Claude Code a usar o framework | Já versionadas em `.claude/skills/`, na mesma versão do CLI (ver seção 12) |
| GSAP | Animações 2D (textos, contadores, transições) | `assets/libs/gsap.min.js` |
| Three.js | Cenas 3D (Zé, balança, cidade) | `assets/libs/three.module.js` + `three.core.js` (módulo ES) |
| Python 3.11+ e edge-tts | Narração em pt-BR com tempos de cada palavra | Instalado em `.venv/` pelo `scripts/instalar.sh` (versão em `requirements.txt`) |
| FFmpeg | Motor interno do HyperFrames (codifica o MP4) | Vem pelo npm (`ffmpeg-static` e `@ffprobe-installer/ffprobe`, versões fixas); nunca é chamado diretamente (seção 6, regra 8) |
| Chrome headless | Renderizar os quadros | Versão fixa baixada pelo HyperFrames (`browser ensure`) |

Não use nenhum serviço pago, chave de API paga nem ferramenta que exija login. Se uma skill ou recurso do HyperFrames depender de serviço pago (por exemplo, voz sintética da HeyGen), não use: a narração é sempre feita pelo `scripts/narrar.py`.

---

## 2. Instalação inicial (executar uma única vez)

Em cada máquina nova, rode `./scripts/instalar.sh` (no Windows, pelo Git Bash). Ele pode ser repetido sem risco e faz os passos 1 a 5; os passos 6 e 7 já estão prontos no repositório.

1. Confere Node 22+ e Python 3.11+, e diz como instalar o que faltar.
2. Instala o HyperFrames na versão fixa do `package.json` (`npm ci`), junto com o FFmpeg que ele usa por dentro, e baixa o Chrome que ele usa.
3. Cria o `.venv/` e instala nele o edge-tts na versão do `requirements.txt`.
4. Confere as bibliotecas e fontes de `assets/` contra `assets/SHA256SUMS` e se as skills estão em `.claude/skills/`.
5. Roda o diagnóstico do HyperFrames, renderiza um teste de 3 s (GSAP, Three.js, fonte e áudio) e testa a voz.
6. Bibliotecas e fontes já estão em `assets/`, com versão fixa registrada em `docs/versoes.md`. Não baixe outras versões sem decisão registrada.
7. A estrutura de pastas da seção 3 e os modelos da seção 7 já existem.
8. **Leia o SKILL.md de `hyperframes` e de `hyperframes-cli` (e as referências que eles apontam) antes de escrever qualquer composição**, e a seção 12 deste arquivo.
9. Construa os componentes da seção 5 e o vídeo de teste da seção 10 antes do primeiro vídeo real.

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
│   ├── settings.json          # permissões e variáveis do HyperFrames para o Claude Code
│   └── skills/                # skills do HyperFrames, na versão do CLI (seção 12)
├── package.json               # HyperFrames com versão fixa (npm ci)
├── requirements.txt           # edge-tts com versão fixa
├── assets/
│   ├── SHA256SUMS             # conferência das bibliotecas e fontes
│   ├── libs/                  # gsap.min.js, three.module.js, three.core.js (versões fixas)
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
│   ├── selo-ia/               # aviso "Feito com auxílio de IA"
│   ├── palco/                 # base das cenas 3D (câmera, luz, chão, tempo do bloco)
│   ├── objetos/               # objetos 3D genéricos do kit (contêiner, carro, fábrica)
│   └── cartoes/               # números grandes, cartões e etiquetas 2D
├── modelos/                   # modelos em branco de cada arquivo de vídeo
│   ├── 01-ideia.md
│   ├── 02-fontes.md
│   ├── 03-roteiro.toml
│   ├── 04-revisoes.md
│   └── status.md
├── scripts/
│   ├── novo-video.sh          # cria a pasta de um vídeo a partir de modelos/
│   ├── roteiro.py             # confere o roteiro e gera o .md de leitura e o texto.txt
│   ├── narrar.py              # gera narração e palavras.json
│   ├── montar.py              # monta a composição a partir do roteiro e dos tempos
│   ├── ajustar-volume.sh      # põe a narração em −14 LUFS pelo HyperFrames
│   ├── verificar.sh           # checagens técnicas do vídeo final
│   ├── hf.sh                  # roda o HyperFrames na composição de um vídeo
│   ├── ambiente.sh            # variáveis comuns (versões fixas, telemetria desligada)
│   ├── mp4info.py             # lê resolução, fps e codecs do MP4 (usado pelo verificar.sh)
│   ├── instalar.sh            # prepara uma máquina nova (seção 2)
│   └── teste-ambiente/        # vídeo de 3 s usado pelo instalar.sh
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
├── 03-roteiro.toml            # onda 2, atualizado nas ondas 4 (a fonte da verdade)
├── 03-roteiro.md              # gerado pelo roteiro.py para leitura; não editar
├── 04-revisoes.md             # registro do debate das ondas 3 e 4
├── narracao/
│   ├── texto.txt              # só o texto falado, gerado pelo roteiro.py do roteiro aprovado
│   ├── narracao.mp3
│   ├── palavras.json          # tempo de início e fim de cada palavra
│   └── ESTIMADO               # só existe quando os tempos são estimados, sem voz
├── composicao/
│   ├── index.html             # raiz da composição (gerada pelo montar.py)
│   ├── tempos.js              # tempos de cada bloco e frase para as cenas (gerado)
│   ├── cenas/                 # bloco-N.html, uma por bloco (escritas à mão);
│   │                          # legendas.html e sobreposicoes.html (geradas)
│   ├── assets/                # link para assets/ do projeto (criado pelo hf.sh)
│   ├── componentes/           # link para componentes/ do projeto (criado pelo hf.sh)
│   └── narracao/              # link para ../narracao (criado pelo hf.sh)
├── previa.mp4                 # render rápido (qualidade draft) para a revisão 2 (fora do Git)
├── final.mp4                  # render final (fora do Git)
└── amostras/                  # quadros e assinatura gerados pelo verificar.sh (fora do Git)
```

### status.md

Atualize sempre que mudar de etapa e acrescente uma linha em `historico` com data, hora e a etapa que começou: é assim que se mede o tempo de produção de cada vídeo (`docs/validacao.md`). Se a sessão for interrompida, a próxima sessão começa lendo este arquivo e continua de onde parou, sem refazer etapas aprovadas.

```
etapa_atual: onda-3-rodada-2
aprovado_roteiro: nao
aprovado_previa: nao
ultima_atualizacao: AAAA-MM-DD HH:MM
pendencias:
  - ...
historico:
  - AAAA-MM-DD HH:MM onda-1
  - AAAA-MM-DD HH:MM onda-2
  - AAAA-MM-DD HH:MM onda-3-rodada-1
```

Etapas possíveis, em ordem: `onda-1`, `onda-2`, `onda-3-rodada-N`, `onda-4-rodada-N`, `revisao-humana-1`, `narracao`, `previa`, `revisao-humana-2`, `final`, `concluido`.

---

## 5. Componentes reutilizáveis

Cada pasta de `componentes/` tem: o código (`.js` e/ou `.html`), um `LEIAME.md` curto com parâmetros e exemplo de uso, e uma imagem de referência (`referencia.png`) gerada a partir de um quadro renderizado. Os vídeos **importam** os componentes; nunca copie e altere um componente dentro da pasta de um vídeo. Se precisar de variação, adicione um parâmetro ao componente.

### tema.css
- Variáveis de cor: `--fundo: #1B2A41`, `--destaque: #FFC93C`, `--positivo: #3DDC97`, `--negativo: #FF6B6B`, `--texto: #FFFFFF`.
- Fontes: Montserrat ExtraBold para legendas e títulos, SemiBold para rodapés.
- Formato: 1080x1920, 30 fps.
- **Área segura** (onde a interface do Instagram, TikTok e Shorts não cobre): nenhum texto importante nos 220 px do topo, nos 590 px de baixo (abaixo de y = 1330 ficam a legenda do post, o nome do perfil e os botões: ali, só decoração) e nos 140 px da direita. Defina isso como variáveis e use em todos os componentes.

### ze/
- Personagem 3D low-poly ORIGINAL: corpo simples de cilindros e esferas, camiseta amarela (`--destaque`), calça azul, cabelo curto escuro, olhos de pontos. Não pode lembrar nenhum personagem conhecido.
- Parâmetros: posição, escala, expressão (`neutro`, `feliz`, `preocupado`, `surpreso`), gesto (`parado`, `aponta`, `ombros`, `comemora`).
- Animações sempre em função do tempo da composição (ver seção 6).
- Protótipo pronto (`componentes/ze/ze.js`, uso no `LEIAME.md`), esperando aprovação do estilo; demonstração em `videos/2026-10-24-prototipo-ze/`.
- A cena precisa de uma luz de frente vinda da câmera, senão a parte de baixo do rosto escurece.

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

### palco/
- Base das cenas 3D: renderizador, câmera em movimento lento, luz suave (com luz de frente) e chão; `aoBuscar` entrega à cena o tempo local do bloco.
- `animacao.js`: transições em função do tempo, compartilhadas pelo Zé e pela balança.

### objetos/
- Objetos 3D low-poly genéricos do kit (contêiner, carro, fábrica). Objeto novo entra aqui, não na pasta do vídeo.

### cartoes/
- Elementos 2D das cenas: número grande, cartão (com borda verde, coral ou amarela) e etiquetas, na largura da área segura.

Legendas, rodapés de fonte e selo de IA não se escrevem à mão: o `scripts/montar.py` os gera para cada vídeo.

---

## 6. Regras técnicas do HyperFrames

1. **Leia as skills antes de escrever.** O formato das composições (atributos `data-*`, trilhas, clipes, sub-composições, variáveis) é definido pela skill `hyperframes` (contrato no SKILL.md e detalhes em `references/format.md` e `references/runtimes.md`). Siga exatamente o que ela documenta e não invente atributos. Quando a skill e este arquivo divergirem, vale a seção 12.
2. **Tudo controlado pelo tempo da composição.** Nenhuma animação pode depender do relógio do navegador (`requestAnimationFrame` livre, `setInterval`, `Date.now()`, `performance.now()`). Animações GSAP devem estar em timelines que o framework consiga posicionar em qualquer instante, conforme a skill indica.
3. **Three.js determinístico.** Cada quadro 3D é calculado a partir do tempo atual da composição: dado o tempo `t`, a cena é posicionada e renderizada para aquele `t`. Sem física acumulada quadro a quadro, sem estado que dependa do quadro anterior. Na prática: `import * as THREE from "./assets/libs/three.module.js";` dentro de um `<script type="module">` e o desenho dentro de um ouvinte `hf-seek` (exemplo funcionando em `scripts/teste-ambiente/composicao/cenas/cubo.html`). **Atenção:** o `hf-seek` traz o tempo do vídeo inteiro, não o da cena; use o `aoBuscar` do `componentes/palco/palco.js`, que entrega o tempo local do bloco.
4. **Aleatoriedade com semente fixa.** Se usar números aleatórios (pessoas na cidade, confetes), use um gerador com semente fixa, para o mesmo vídeo sair igual em todo render.
5. **Sem rede no render.** Bibliotecas, fontes, sons e imagens vêm de `assets/` ou do próprio componente. Os caminhos são sempre relativos à pasta `composicao/` (`assets/libs/gsap.min.js`, `componentes/tema.css`, `narracao/narracao.mp3`), inclusive dentro das cenas; o `scripts/hf.sh` cria os links que fazem esses caminhos existirem.
6. **Duração vem da narração.** A duração de cada cena é calculada a partir de `palavras.json`: cada bloco do roteiro começa na primeira palavra do bloco e termina na primeira palavra do bloco seguinte (o `scripts/montar.py` faz essa conta e entrega os tempos às cenas em `TEMPOS.bloco(n)`, que é como as cenas devem marcar seus momentos; nunca segundos escritos à mão). O bloco 1 começa sempre em 0 s (a voz tem um pequeno silêncio antes da primeira palavra, e o primeiro quadro precisa mostrar o gancho), e o último bloco ganha 1,5 s extras no final.
7. **Valide antes de renderizar.** Rode o `lint` e o `check` do HyperFrames após qualquer alteração e corrija todos os erros antes de gerar a prévia. Confira também os quadros com `snapshot`: passar no `check` não mostra como ficou.
8. **Só HyperFrames, nunca FFmpeg direto.** O FFmpeg é o motor interno do HyperFrames e ninguém o chama: medir áudio é `audio`, ajustar volume é `normalize-audio` (pelo `scripts/ajustar-volume.sh`), ver quadros é `snapshot`, renderizar é `render`.
9. **Narração na composição:** sempre `<audio id="narracao" src="narracao/narracao.mp3" data-start="0" data-volume="1">` no `index.html`. O `ajustar-volume.sh` acerta o `data-volume`.

### Comandos principais (detalhes e opções na skill `hyperframes-cli`)

Sempre pelo `scripts/hf.sh`, que roda o CLI de versão fixa dentro de `composicao/`, cria os links e desliga telemetria e atualizações automáticas. O `index.html`, as legendas e as sobreposições saem do `scripts/montar.py`; as cenas `cenas/bloco-N.html` são escritas à mão. Não use `init` dentro da pasta do vídeo.

```
python3 scripts/montar.py videos/<pasta>                   # monta a composição (rodar de novo sempre que a narração ou o roteiro mudar)
./scripts/hf.sh videos/<pasta> lint                       # checar erros de composição
./scripts/hf.sh videos/<pasta> check --json               # validar antes do render (substitui o antigo validate)
./scripts/hf.sh videos/<pasta> snapshot --at 1,10,30      # quadros em PNG para conferir
./scripts/hf.sh videos/<pasta> timeline --json            # o que toca quando
./scripts/hf.sh videos/<pasta> preview --background       # pré-visualizar no navegador
./scripts/ajustar-volume.sh videos/<pasta>                # narração em −14 LUFS no vídeo final
./scripts/hf.sh videos/<pasta> render --quality draft --output ../previa.mp4
./scripts/hf.sh videos/<pasta> render --quality delivery --output ../final.mp4
./scripts/hf.sh doctor                                    # diagnosticar o ambiente
```

- **Prévia:** `--quality draft`, em 1080x1920. O HyperFrames não renderiza abaixo do tamanho da composição, então a prévia ganha velocidade pela qualidade, não pela resolução.
- **Final:** `--quality delivery`, 1080x1920, 30 fps, H.264, áudio AAC (padrão do MP4 do HyperFrames).

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

## Termômetro
Onde os especialistas estão, de verdade: consenso para um lado, divisão real ou falta de evidência. Base: pesquisa com economistas (ex.: Clark Center, antigo IGM Forum) ou revisão da literatura, com código na tabela acima (F...).
- ...
```

### 03-roteiro.toml
O roteiro é escrito como dados, e o `scripts/roteiro.py` gera dele o `03-roteiro.md` (para ler e para o crítico) e o `narracao/texto.txt` (para a voz). O modelo completo, comentado, está em `modelos/03-roteiro.toml`. Resumo:

```
titulo = "E se [pergunta]?"
versao = 1                       # atualizar a cada rodada

[[bloco]]                        # Gancho, Contexto, O que mudaria, A balança, Exemplo real (opcional), Encerramento
nome = "Gancho"
cena = "componentes usados e o que acontece na tela"

  [[bloco.frase]]
  fala = "R$ 1,5 trilhão."       # o texto do narrador
  marcacao = "FATO"              # FATO, PROJEÇÃO, PREMISSA, ARGUMENTO A FAVOR, ARGUMENTO CONTRA, TERMÔMETRO, BORDÃO
  fontes = ["F1"]                # obrigatório em tudo, menos BORDÃO e PREMISSA
  tela = "R$ 1,5 trilhão"        # opcional: o que aparece na tela (o rodapé sai das fontes)
  voz = "Um vírgula cinco trilhão de reais."   # opcional: como a voz deve ler

  [[bloco.frase]]
  fala = "E se [tema]? Vamos imaginar."
  marcacao = "BORDÃO"
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

### scripts/roteiro.py
- `python3 scripts/roteiro.py checar videos/<pasta>`: confere o `03-roteiro.toml` e gera o `03-roteiro.md`. Erros que barram: frase sem marcação válida; frase sem fonte (menos bordões e premissas); fonte que não existe no `02-fontes.md` ou sem link e data de acesso; texto de modelo esquecido; blocos fora da ordem ou faltando; bordões ausentes; argumentos fora da balança; balança com número de frases diferente entre os lados ou tamanho fora da razão 0,8–1,25; termômetro ausente ou repetido; texto na tela sem fonte.
- Avisos: duração estimada fora de 45–90 s (estimativa por palavras; a real sai da narração), gancho ou encerramento longos e algarismos na fala sem a versão `voz` por extenso.
- `python3 scripts/roteiro.py texto videos/<pasta>`: faz a mesma conferência e, sem erros, gera o `narracao/texto.txt` com os `[BLOCO N]`, usando a `voz` de cada frase quando existir.
- Precisa do Python 3.11 ou mais novo (lê TOML sem instalar nada).

### scripts/narrar.py
- Recebe a pasta do vídeo, lê `narracao/texto.txt` e gera `narracao.mp3` e `palavras.json` com o edge-tts.
- Voz fixa: `pt-BR-AntonioNeural`, ritmo `+10%`. Nunca mude sem minha autorização.
- Use os eventos de limite de palavra do edge-tts para obter o tempo de cada palavra. Se a versão instalada só emitir limites de frase por padrão, configure para emitir limites de palavra.
- Formato do `palavras.json`: lista de `{ "palavra": "...", "inicio": 0.00, "fim": 0.00, "bloco": N }`, em segundos.
- O `texto.txt` marca o início de cada bloco com uma linha `[BLOCO N]`, que o script usa para preencher o campo `bloco` e não envia para a voz.
- Números são escritos por extenso no `texto.txt` quando a voz puder lê-los errado (ex.: "R$ 1,5 trilhão" → "um vírgula cinco trilhão de reais"). A versão em algarismos fica só na tela.
- Grava o áudio do edge-tts como veio. O volume é acertado depois, na composição, pelo `scripts/ajustar-volume.sh`.
- Usa o edge-tts do `.venv/` automaticamente quando o Python do sistema não o tem. Precisa de internet com WebSocket liberado.
- `--estimar`: sem voz (quando o edge-tts não alcança a internet), gera só o `palavras.json` com tempos estimados pelo tamanho das palavras e pela pontuação, e deixa a marca `narracao/ESTIMADO`. Serve para montar e revisar o vídeo antes da voz; a narração real substitui tudo.

### scripts/montar.py
- `python3 scripts/montar.py videos/<pasta>`: lê o `03-roteiro.toml`, o `02-fontes.md` e o `narracao/palavras.json` e gera o `composicao/index.html` (cada cena no seu tempo, a narração com o volume já ajustado preservado), o `tempos.js`, as legendas e as sobreposições (selo de IA e rodapés de fonte).
- Cria um modelo simples para cada `cenas/bloco-N.html` que faltar; nunca sobrescreve uma cena existente.
- Distribui as palavras entre as frases pela quantidade de letras, então funciona com a voz sintética, com tempos estimados e com uma gravação humana.

### scripts/verificar.sh
Roda no `final.mp4` e falha se algo estiver fora do padrão:
- Resolução 1080x1920 e 30 fps.
- Duração entre 45 e 90 s.
- Existe trilha de áudio e a narração não está cortada no fim.
- Volume da narração normalizado (aprox. −14 LUFS) e trilha de fundo, se existir, bem mais baixa que a voz.
- Gera 6 quadros de amostra em `videos/.../amostras/` para conferência visual.
- Tudo pelo HyperFrames (`audio` para volume e silêncio, `snapshot` para os quadros) e pelo `scripts/mp4info.py` (resolução, fps e codecs lidos do cabeçalho do MP4), sem FFmpeg direto.
- As amostras ficam em `amostras/`: `ref-*.png` são quadros do `final.mp4` e `pair-*.jpg` mostram composição e final lado a lado.
- Grava em `amostras/assinatura.txt` o SHA-256 do `final.mp4` e avisa se o render saiu idêntico ao anterior (teste de determinismo: o HyperFrames gera os mesmos bytes para a mesma composição).
- `--teste` aceita de 10 a 20 s em vez de 45 a 90 s (vídeo de teste da seção 10).

### scripts/ajustar-volume.sh
- `./scripts/ajustar-volume.sh videos/<pasta>`: roda o `normalize-audio` do HyperFrames no `<audio id="narracao">` e grava o ganho no `data-volume`.
- A narração do edge-tts é mono e o HyperFrames a toca nos dois canais, o que soma 3 dB; por isso o alvo para áudio mono é −17 LUFS, que dá −14 no vídeo final (medido: −14,1).
- Rode depois de montar a composição e antes da prévia, e de novo se a narração mudar.

### scripts/hf.sh
- `./scripts/hf.sh videos/<pasta> <comando> [opções]`: roda o HyperFrames dentro de `composicao/` (comandos na seção 6). Sem a pasta, roda comandos gerais (`./scripts/hf.sh doctor`).
- Usa o CLI e o FFmpeg nas versões fixas do `package.json` (`scripts/ambiente.sh`).
- Antes de cada comando, liga `composicao/assets`, `composicao/componentes` e `composicao/narracao` às pastas reais. No Windows sem permissão para links, copia as pastas a cada execução; nunca edite essas cópias.
- Recusa os comandos fora das regras da seção 12 (`publish`, `cloud`, `feedback`, `upgrade`, `skills` etc.).

### scripts/instalar.sh
- Prepara uma máquina nova e prova que ela renderiza (seção 2). `--sem-voz` pula o teste de conexão do edge-tts.

---

## 9. Checklist antes de cada revisão humana

**Revisão 1 (roteiro):**
- [ ] `python3 scripts/roteiro.py checar` passou sem erros (fontes, marcações, bordões, blocos, equilíbrio da balança e termômetro conferidos automaticamente).
- [ ] O termômetro diz com honestidade onde os especialistas estão (o script só confere que ele existe e tem fonte; o conteúdo é conferência humana).
- [ ] Os números do roteiro batem com o `02-fontes.md` e estão atualizados.
- [ ] As ondas 3 e 4 terminaram sem objeção CRÍTICA ou IMPORTANTE pendente.

**Revisão 2 (prévia):**
- [ ] Narração, legendas e cenas estão sincronizadas.
- [ ] Todo número na tela tem rodapé de fonte e bate com o roteiro aprovado.
- [ ] Nenhum texto fora da área segura (abaixo de y = 1330, só decoração).
- [ ] Selo de IA visível do início ao fim.
- [ ] Nenhuma pessoa real, marca, logotipo ou personagem conhecido na tela.
- [ ] A balança termina equilibrada (salvo marcação explícita no roteiro).
- [ ] `verificar.sh` passou sem erros (no final).

---

## 10. Vídeo de teste (antes do primeiro vídeo real)

Crie `videos/AAAA-MM-DD-teste/` com 15 segundos usando todos os componentes: o Zé entra na cidade, um contador vai de R$ 10,00 a R$ 15,00 na vitrine com rodapé de fonte fictícia marcada como "(teste)", a balança aparece equilibrada e as legendas acompanham uma narração curta gerada pelo `narrar.py`. Renderize a prévia e o final, rode o `verificar.sh --teste`, renderize o final de novo e rode o `verificar.sh --teste` mais uma vez: ele precisa dizer "render idêntico ao anterior" (determinismo). Só depois disso comece o primeiro tema real.

---

## 11. Ordem de execução de um vídeo

1. `./scripts/novo-video.sh <slug>`
2. Ondas 1 e 2 (`01-ideia.md`, `02-fontes.md`, `03-roteiro.toml`), até o `roteiro.py checar` passar sem erros.
3. Ondas 3 e 4 com o subagente `critico`, registrando tudo em `04-revisoes.md`, até no máximo 4 rodadas. O crítico lê `01-ideia.md`, `03-roteiro.md` e `02-fontes.md`; a partir da rodada 2, recebe também a tabela de objeções anteriores com decisão e base. Depois de cada adaptação, rode o `roteiro.py checar` de novo.
4. 🛑 Revisão humana 1. Parar e esperar.
5. `python3 scripts/roteiro.py texto videos/<pasta>` e `python3 scripts/narrar.py videos/<pasta>` (sem internet para a voz: `--estimar`, e a voz depois).
6. `python3 scripts/montar.py videos/<pasta>`, escrever as cenas `cenas/bloco-N.html` com os componentes (tempos de `TEMPOS.bloco(n)`), rodar `scripts/ajustar-volume.sh`, rodar `lint` e `check` pelo `scripts/hf.sh` e conferir os quadros com `snapshot`.
7. Renderizar `previa.mp4`.
8. 🛑 Revisão humana 2. Parar e esperar.
9. Renderizar `final.mp4`, rodar `verificar.sh`, conferir as amostras.
10. Marcar `status.md` como `concluido` (com a linha no `historico`) e registrar em `docs/aprendizados.md` qualquer problema que tenha aparecido.

Se eu pedir mudança no roteiro depois da revisão 1, volte às ondas 3 e 4 só para os trechos alterados antes de seguir.

---

## 12. Skills do HyperFrames × regras do canal

As skills em `.claude/skills/` (`hyperframes`, `hyperframes-cli`, `hyperframes-registry` e `media-use`) são cópias da versão do CLI fixada no `package.json` e servem para a **técnica** do framework: formato das composições, contrato de render, legendas, 3D, comandos. Elas foram escritas para qualquer projeto e às vezes mandam fazer coisas que este canal não faz. Quando divergirem, valem o `CLAUDE.md` e este arquivo:

- **Versões fixas.** Não rode `upgrade`, `skills update`, `npx hyperframes@latest` nem `npx skills add`, e ignore avisos de versão nova. Atualizar o HyperFrames é uma decisão minha: trocar a versão no `package.json`, copiar as skills da tag correspondente do repositório `heygen-com/hyperframes` para `.claude/skills/`, registrar em `docs/versoes.md`, rodar `./scripts/instalar.sh` e refazer o vídeo de teste, conferindo se o `verificar.sh` ainda dá −14 LUFS (a compensação de 3 dB do `ajustar-volume.sh` depende do comportamento atual do `normalize-audio`).
- **Nada pago, nada com conta, nada na nuvem.** Nunca HeyGen (voz, avatar, música, imagens), `cloud`, `lambda`, `cloudrun`, `publish` ou `auth`. Na `media-use`, só ferramentas locais e gratuitas, com `--local-only`.
- **FFmpeg só por dentro do HyperFrames.** Mesmo que uma skill mostre um comando `ffmpeg` ou `ffprobe`, use o comando equivalente do HyperFrames (seção 6, regra 8).
- **Na validação, a voz é a do `scripts/narrar.py`.** Nunca `hyperframes tts`. O `transcribe` só entra na troca para voz humana (seção 13), para tirar os tempos da gravação.
- **Nada sai da máquina.** Telemetria desligada (`.claude/settings.json` e `scripts/hf.sh`); não envie `feedback`, `--search-miss` nem relatórios de lacuna, e não rode `usage`.
- **O fluxo é o das ondas** (`CLAUDE.md`, seção 6), não o da skill (três storylines, `SPEC.md`, `REVIEW.md`, aplicativo de desktop). As paradas 🛑 continuam valendo: renderizar o final só depois da revisão humana 2.
- **Conteúdo e visual são do `CLAUDE.md`.** Música e efeitos só se o roteiro pedir, com licença anotada em `assets/sons/`. O formato é sempre 1080x1920 (a skill assume 1920x1080 por padrão). Áreas seguras e tamanhos vêm do `componentes/tema.css`, não dos números da skill.
- **Legendas:** as regras da seção 5 (1 a 4 palavras, palavra falada em amarelo, nunca antes de ser falada) valem sobre os padrões da skill; as técnicas dela (`fitTextFontSize`, grupos com saída garantida) podem ser usadas.
- **Registro de blocos:** um bloco do `hyperframes-registry` pode servir de ponto de partida, mas o que for reutilizado vira componente em `componentes/`, adaptado à identidade do canal, nunca dentro da pasta do vídeo. O `add` precisa de rede: só durante a construção, nunca no render.

---

## 13. Trocar a voz (depois da validação)

Na validação a voz é a do `narrar.py`. Para publicar com voz humana, o vídeo é **renderizado de novo** com a gravação. Não troque só a faixa de áudio do `final.mp4`: legendas e cenas são cronometradas pelo `palavras.json` da voz sintética e ficariam fora de sincronia. Como tudo deriva do `palavras.json`, as cenas se reajustam sozinhas no novo render.

1. Grave lendo o `narracao/texto.txt`, sem trocar palavras (pequenas pausas e ritmo próprio são bem-vindos).
2. Guarde a narração sintética como `narracao/narracao-tts.mp3` e ponha a gravação no lugar de `narracao/narracao.mp3`.
3. Gere um `palavras.json` novo a partir da gravação: o `hyperframes transcribe` (local, com `--language pt`) dá o tempo de cada palavra, e um script de alinhamento casa essas palavras com o `texto.txt` para preencher o campo `bloco`. Esse script ainda não existe: fazer quando a troca for decidida.
4. Rode o `ajustar-volume.sh` (ele detecta se a gravação é mono ou estéreo), renderize prévia e final e rode o `verificar.sh`.
