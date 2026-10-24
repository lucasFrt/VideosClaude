# Aprendizados

O que deu errado ou não batia com a documentação, e como foi resolvido. Itens marcados **[proposta]** esperam decisão.

## 2026-10-24 — Instalação inicial

### 1. Skills do HyperFrames no ambiente na nuvem
O `npx skills add heygen-com/hyperframes` foi negado pela política de permissões da sessão na nuvem, mesmo com autorização. O `npm install` do HyperFrames funcionou.
**Resolvido:** as skills foram copiadas da tag `v0.8.192` do repositório oficial (mesma versão do CLI) para `.claude/skills/` e ficam versionadas no Git. Instalei só o conjunto principal (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`); não existe skill `hyperframes-core` (o contrato está na `hyperframes`).

### 2. edge-tts não funciona no ambiente na nuvem
O edge-tts fala com `speech.platform.bing.com` por WebSocket, e o proxy do ambiente na nuvem não aceita WebSocket. Na sua máquina deve funcionar; o `instalar.sh` testa isso no passo 7. O `narrar.py` foi testado com uma voz falsa (separação por bloco, `palavras.json`, normalização e uso do `.venv/`).

### 3. Nomes de arquivo diferentes entre CLAUDE.md, ESTRUTURA.md e critico.md
O CLAUDE.md (seção 6) e o `critico.md` falam em `ideia.md`, `fontes.md`, `roteiro.md` e `revisoes.md`; o ESTRUTURA.md usa `01-ideia.md` etc. Pela regra do ESTRUTURA.md (técnica vale o ESTRUTURA), uso os nomes numerados.
**[proposta]** Atualizar o CLAUDE.md e o `critico.md` para os nomes numerados.

### 4. Marcações das frases
O CLAUDE.md usa `[ARGUMENTO DE UM LADO]`; o modelo do roteiro usa `[ARGUMENTO A FAVOR]` e `[ARGUMENTO CONTRA]`. São compatíveis; uso as do modelo, que facilitam conferir o equilíbrio da balança.
**[proposta]** Ajustar o CLAUDE.md para as duas marcações.

### 5. Crítico sem memória entre rodadas
O CLAUDE.md diz que o crítico recebe só ideia, roteiro e fontes; o `critico.md` exige que objeções resolvidas não voltem. Sem ver as rodadas anteriores, ele vai reapontar as objeções rejeitadas.
**[proposta]** A partir da rodada 2, entregar também a tabela de objeções anteriores com a decisão e a base de cada uma. Ele só reabre uma objeção rejeitada se trouxer base nova.

### 6. verificar.sh × vídeo de teste
A seção 8 manda falhar fora de 45–60 s, e a seção 10 manda rodar o `verificar.sh` no vídeo de teste de 15 s.
**Resolvido:** `verificar.sh --teste` aceita de 10 a 20 s (registrado no ESTRUTURA.md).

### 7. Como provar o determinismo
Rodar o `verificar.sh` duas vezes no mesmo arquivo não prova nada, e os bytes do MP4 podem mudar só por metadados.
**Resolvido:** o `verificar.sh` grava o MD5 dos quadros e do áudio decodificados e avisa se o render seguinte saiu idêntico. Testado: dois renders da mesma cena 3D deram o mesmo MD5.

### 8. Volume em −14 LUFS
Nenhuma etapa gerava esse nível. Primeiro resolvi no `narrar.py` com o FFmpeg; depois troquei pelo HyperFrames (item 15).
**Resolvido:** o `scripts/ajustar-volume.sh` usa o `normalize-audio` do HyperFrames. Limitação dele: mede a narração mono, mas a toca nos dois canais, o que soma 3 dB (medido: alvo −14 deu −11,1 no vídeo final). O script compensa usando −17 para áudio mono: o vídeo final sai em −14,1 LUFS.

### 9. Three.js
O `three.min.js` só existe até a r159 e gera um aviso de "deprecated" em todo `check`.
**Resolvido:** trocado pela r186 em módulo ES (`three.module.js` + `three.core.js`), testado dentro de uma sub-composição, sem avisos. Uso: `import * as THREE from "./assets/libs/three.module.js";`.

### 10. Início do bloco 1
A regra 6.6 diz que cada bloco começa na primeira palavra dele, mas o edge-tts põe um pequeno silêncio antes da primeira palavra.
**[proposta]** O bloco 1 começa sempre em 0 s.

### 11. Correções técnicas no ESTRUTURA.md
Aplicadas porque o texto original não funcionava na prática: Node 22+ (o HyperFrames exige); `validate` foi substituído por `check`; a skill `hyperframes-core` não existe; a prévia não pode ter resolução menor que a composição (virou `--quality draft`); caminhos relativos à pasta da composição, com links criados pelo `scripts/hf.sh`; instalação automatizada pelo `scripts/instalar.sh`.

### 12. Skills do HyperFrames que conflitam com as regras do canal
As skills mandam, por exemplo, atualizar a versão do CLI sozinho, enviar relatórios de feedback depois de cada render, usar HeyGen para voz e música e pôr música em todo vídeo acima de 15 s.
**Resolvido:** seção 12 do ESTRUTURA.md (o que vale aqui), telemetria e atualização automática desligadas em `.claude/settings.json` e `scripts/hf.sh`, e o `hf.sh` recusa `publish`, `cloud`, `feedback`, `upgrade`, `skills` e afins.

### 13. Áreas seguras: ESTRUTURA × skill do HyperFrames
O ESTRUTURA.md reserva 220 px no topo, 420 px embaixo e 140 px à direita. A skill de vídeo vertical recomenda nada no topo até 168 px e **nenhum texto abaixo de 1330 px** (590 px do fundo), porque a legenda do post, o nome do perfil e os botões ocupam essa faixa no Instagram e no TikTok. Com 420 px, o rodapé de fonte e as legendas podem ficar embaixo do texto do post.
**[proposta]** Subir a margem de baixo para algo entre 520 e 600 px. Por ora o `tema.css` segue os 420 px do ESTRUTURA.md.

### 14. Windows
Scripts com fim de linha CRLF quebram no Git Bash: o `.gitattributes` força LF. Links simbólicos exigem o Modo de Desenvolvedor; sem ele, o `hf.sh` copia as pastas a cada execução.

### 15. Só HyperFrames, sem FFmpeg direto (decisão sua)
Os scripts chamavam o FFmpeg e o FFprobe diretamente (normalizar a narração, medir o vídeo final, tirar quadros, gerar o áudio do teste), e o README pedia para instalar o FFmpeg.
**Resolvido:**
- Volume: `normalize-audio` do HyperFrames (`scripts/ajustar-volume.sh`).
- Medir áudio do vídeo final: `hyperframes audio`.
- Quadros de amostra: `hyperframes snapshot --against final.mp4`.
- Resolução, fps e codecs: `scripts/mp4info.py`, que lê o cabeçalho do MP4 em Python puro.
- Determinismo: SHA-256 do arquivo (dois renders da mesma composição saem com os mesmos bytes).
- O áudio do teste do instalador agora vem pronto em `scripts/teste-ambiente/narracao/`.

O HyperFrames não funciona sem FFmpeg (é com ele que codifica o MP4; só a renderização na nuvem paga da HeyGen dispensa). Por isso o FFmpeg agora vem pelo npm, com versão fixa (`ffmpeg-static` e `@ffprobe-installer/ffprobe`), e o `scripts/ambiente.sh` aponta o HyperFrames para ele: ninguém instala o FFmpeg no sistema. O `.claude/settings.json` proíbe o Claude Code de chamar `ffmpeg` e `ffprobe`.
Testado com um `ffmpeg` e um `ffprobe` falsos na frente do PATH, que acusariam qualquer chamada: instalador, ajuste de volume, dois renders finais e duas verificações rodaram sem nenhuma chamada a eles.
