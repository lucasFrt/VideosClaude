# Canal "E se...?"

Vídeos curtos (45–90 s, 1080x1920) que explicam ideias econômicas mostrando consequências possíveis, prós e contras. Feitos com HyperFrames (HTML + GSAP + Three.js), narração do edge-tts e o Claude Code.

- **`CLAUDE.md`**: identidade do canal, tom, visual e fluxo em ondas (o Claude Code lê sozinho).
- **`ESTRUTURA.md`**: manual técnico (pastas, componentes, scripts, comandos).
- **`docs/aprendizados.md`**: problemas encontrados e propostas que esperam decisão.

## Preparar uma máquina

Precisa de: Git, Node.js 22+ e Python 3.11+. O FFmpeg que o HyperFrames usa por dentro vem junto pelo npm; não instale nem use à parte.

| Sistema | Como instalar |
|---|---|
| macOS | `brew install node python` |
| Windows | Git for Windows (traz o Git Bash), `winget install OpenJS.NodeJS.LTS Python.Python.3.12`. Opcional: ativar o Modo de Desenvolvedor, para o `hf.sh` usar links em vez de cópias |
| Linux | `sudo apt install nodejs python3 python3-venv` (Node 22+ pelo nodejs.org se a distribuição tiver um mais velho) |

Depois, num terminal (no Windows, o Git Bash):

```bash
git clone https://github.com/lucasFrt/VideosClaude.git
cd VideosClaude
./scripts/instalar.sh
```

O instalador confere as ferramentas, instala o HyperFrames (com o FFmpeg dele) e o edge-tts nas versões fixas, baixa o Chrome que o HyperFrames usa, confere bibliotecas e fontes, renderiza um teste de 3 s e testa a voz. Pode rodar de novo sempre que quiser.

Pronto: abra a pasta no VS Code e inicie o Claude Code. As permissões dos scripts do projeto já estão em `.claude/settings.json`.

## Comandos do dia a dia

```bash
./scripts/novo-video.sh <slug>                          # cria videos/AAAA-MM-DD-slug/
python3 scripts/roteiro.py checar videos/<pasta>        # confere o 03-roteiro.toml e gera o .md
python3 scripts/roteiro.py texto videos/<pasta>         # gera o texto da narração
python3 scripts/narrar.py videos/<pasta>                # narração + palavras.json (Windows: python)
./scripts/ajustar-volume.sh videos/<pasta>              # narração em −14 LUFS (via HyperFrames)
./scripts/hf.sh videos/<pasta> check --json             # valida a composição
./scripts/hf.sh videos/<pasta> preview --background     # pré-visualiza no navegador
./scripts/hf.sh videos/<pasta> render --quality draft --output ../previa.mp4
./scripts/hf.sh videos/<pasta> render --quality delivery --output ../final.mp4
./scripts/verificar.sh videos/<pasta>                   # confere o final.mp4
```

## Situação

- Instalação pronta e testada: render, determinismo e volume conferidos, sem chamar o FFmpeg diretamente.
- Roteiro estruturado com checagem automática (`scripts/roteiro.py`) e critérios de validação (`docs/validacao.md`).
- Protótipo do Zé em `videos/2026-10-24-prototipo-ze/` esperando sua decisão sobre o estilo.
- Depois disso: os outros componentes (`ESTRUTURA.md`, seção 5), o vídeo de teste (seção 10) e a composição gerada a partir do roteiro.
- Propostas esperando decisão: `docs/aprendizados.md`, itens marcados **[proposta]**.
