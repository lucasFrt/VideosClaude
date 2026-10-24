# Aprendizados

O que deu errado ou não batia com a documentação, e como foi resolvido. Itens marcados **[proposta]** esperam decisão.

## 2026-10-24 — Instalação inicial

### 1. Instalação das skills e do HyperFrames bloqueada no ambiente na nuvem
`npx skills add heygen-com/hyperframes` foi negado pela política de permissões da sessão, porque instala código e instruções de fora do projeto. O mesmo vale para `npx hyperframes`. Sem as skills, não dá para seguir a regra 6.1 (ler a `hyperframes-core` antes de escrever composições), então os componentes (exceto `tema.css`) e o vídeo de teste ficaram parados.
**Pendente:** autorização para instalar e rodar o HyperFrames e as skills dele.

### 2. edge-tts não funciona no ambiente na nuvem
O edge-tts fala com `speech.platform.bing.com` por WebSocket, e o proxy de rede deste ambiente não aceita conexões WebSocket. O `narrar.py` foi testado só com uma voz falsa (separação por bloco, `palavras.json` e normalização funcionam).
**[proposta]** Rodar o `narrar.py` no seu computador e versionar `narracao.mp3` e `palavras.json`, ou usar um ambiente com acesso a WebSocket.

### 3. Nomes de arquivo diferentes entre CLAUDE.md, ESTRUTURA.md e critico.md
O CLAUDE.md (seção 6) e o `critico.md` falam em `ideia.md`, `fontes.md`, `roteiro.md` e `revisoes.md`; o ESTRUTURA.md usa `01-ideia.md`, `02-fontes.md`, `03-roteiro.md` e `04-revisoes.md`. Pela regra do ESTRUTURA.md (técnica vale o ESTRUTURA), uso os nomes numerados.
**[proposta]** Atualizar o CLAUDE.md e o `critico.md` para os nomes numerados.

### 4. Marcações das frases
O CLAUDE.md usa `[ARGUMENTO DE UM LADO]`; o modelo do roteiro usa `[ARGUMENTO A FAVOR]` e `[ARGUMENTO CONTRA]`. São compatíveis; uso as duas do modelo, que facilitam conferir o equilíbrio da balança.
**[proposta]** Ajustar o CLAUDE.md para as duas marcações.

### 5. Crítico sem memória entre rodadas
O CLAUDE.md diz que o crítico recebe só ideia, roteiro e fontes; o `critico.md` exige que objeções resolvidas não voltem na rodada seguinte. Sem ver as rodadas anteriores, ele não tem como saber o que já foi resolvido, principalmente as objeções rejeitadas (o trecho continua igual e ele vai apontar de novo).
**[proposta]** A partir da rodada 2, entregar também a tabela de objeções anteriores com a decisão e a base de cada uma. Ele só reabre uma objeção rejeitada se trouxer base nova.

### 6. verificar.sh × vídeo de teste
A seção 8 manda falhar fora de 45–60 s, e a seção 10 manda rodar o `verificar.sh` no vídeo de teste de 15 s, que falharia sempre.
**Resolvido (provisório):** `verificar.sh --teste` aceita de 10 a 20 s. **[proposta]** Registrar a opção no ESTRUTURA.md.

### 7. Como provar o determinismo
Rodar o `verificar.sh` duas vezes no mesmo `final.mp4` não prova que dois renders saem iguais, e comparar os bytes do MP4 pode dar diferença só por metadados.
**Resolvido:** o `verificar.sh` grava em `amostras/assinatura.txt` o MD5 dos quadros e do áudio decodificados e, na rodada seguinte, avisa se o novo render saiu idêntico. O teste fica: renderizar, verificar, renderizar de novo, verificar.

### 8. Quem normaliza o volume em −14 LUFS
O `verificar.sh` confere −14 LUFS, mas nenhuma etapa gerava esse nível.
**Resolvido:** o `narrar.py` normaliza a narração (loudnorm em duas passagens, modo linear, que mexe só no ganho e não desloca os tempos das palavras).

### 9. Three.js: `three.min.js` só existe até a r159
A partir da r160 o Three.js só é distribuído como módulo ES (`three.module.min.js` + `three.core.min.js`). Por ora está em `assets/libs/` a r159, que imprime um aviso de "deprecated" no console mas funciona.
**[proposta]** Depois de ler como o HyperFrames carrega o Three.js, decidir entre ficar na r159 ou ir para a versão atual em módulo ES.

### 10. Início do bloco 1
A regra 6.6 diz que cada bloco começa na primeira palavra dele. O edge-tts põe um pequeno silêncio antes da primeira palavra, então o bloco 1 ficaria começando depois do zero.
**[proposta]** O bloco 1 começa sempre em 0 s.
