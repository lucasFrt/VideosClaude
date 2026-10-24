# Versões

Versões fixas usadas no projeto. Ao atualizar qualquer item, registre aqui a nova versão, a data e o motivo, atualize `assets/SHA256SUMS` quando for o caso, rode `./scripts/instalar.sh` e refaça o vídeo de teste.

## Ferramentas

| Ferramenta | Versão | Onde é fixada |
|---|---|---|
| HyperFrames (CLI) | 0.8.192 | `package.json` / `package-lock.json` (`npm ci`) |
| Skills do HyperFrames | tag `v0.8.192` (`c16b783`) de github.com/heygen-com/hyperframes | `.claude/skills/` (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) |
| Chrome Headless Shell | 152.0.7977.30 | escolhida pelo HyperFrames 0.8.192 (`browser ensure`) |
| edge-tts | 7.3.1 | `requirements.txt` (instalado em `.venv/`) |
| Node.js | 22 ou mais novo | exigência do HyperFrames; testado com 22.22.0 |
| Python | 3.10 ou mais novo | testado com 3.13.17 |
| FFmpeg | `ffmpeg-static` 5.3.0 (build b6.1.1; no Linux é o FFmpeg 7.0.2 estático) | `package.json`; motor interno do HyperFrames, nunca chamado direto |
| FFprobe | `@ffprobe-installer/ffprobe` 2.1.2 (binário da plataforma) | `package.json`; idem |

## Bibliotecas e fontes (em `assets/`, conferidas por `assets/SHA256SUMS`)

| Arquivo | Versão | Origem | Licença |
|---|---|---|---|
| `libs/gsap.min.js` | GSAP 3.15.0 | npm `gsap@3.15.0`, `dist/gsap.min.js` | GSAP Standard "no charge" (gsap.com/standard-license) |
| `libs/three.module.js` + `libs/three.core.js` | Three.js r186 (0.186.1) | npm `three@0.186.1`, `build/` | MIT (`libs/LICENSE-three.txt`) |
| `fontes/Montserrat-ExtraBold.ttf` | Montserrat v9.000 | github.com/JulietaUla/Montserrat, tag `v9.000` (`f1f4e9b`) | OFL 1.1 (`fontes/OFL.txt`) |
| `fontes/Montserrat-SemiBold.ttf` | Montserrat v9.000 | idem | OFL 1.1 |

## Histórico

- 2026-10-24: instalação inicial. Three.js começou na r159 (`three.min.js`) e foi trocado no mesmo dia pela r186 em módulo ES (ver `aprendizados.md`, item 9).
