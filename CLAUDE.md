# CLAUDE.md — Canal "E se...?" de economia e política

> **MODO ATUAL: VALIDAÇÃO.** Só criamos vídeos para testar o formato. Nada é publicado. Temas sobre candidatos e propostas eleitorais estão fora do escopo por enquanto.

Este arquivo define a identidade fixa do canal. Leia-o inteiro antes de qualquer tarefa e siga-o em todos os vídeos. A parte técnica (pastas, skills, componentes, scripts e comandos) está em `ESTRUTURA.md`; leia os dois. A consistência de tom, visual e estrutura é o que diferencia o canal de conteúdo automatizado genérico.

---

## 1. Quem somos

**Nome do canal:** [DEFINIR, ex.: "E se fosse assim?"]

**Missão:** explicar ideias econômicas e propostas políticas de um jeito que qualquer pessoa entenda, mostrando consequências possíveis, prós e contras, sem dizer em quem votar ou o que pensar.

**Público:** brasileiros de 18 a 40 anos, curiosos, sem formação em economia, que querem entender a notícia antes de formar opinião.

**Promessa ao público:** "A gente não te diz o que pensar. A gente te mostra o que poderia acontecer."

---

## 2. Personalidade do narrador

O narrador é sempre a mesma "pessoa": um amigo curioso que estudou o assunto a fundo e explica na mesa do bar, sem arrogância.

- **Tom:** calmo, curioso e levemente bem-humorado. Nunca debochado, nunca indignado, nunca alarmista.
- **Postura:** faz perguntas, testa hipóteses, admite incerteza ("ninguém sabe ao certo, mas...").
- **Linguagem:** frases curtas, português do dia a dia, zero jargão sem explicação. Se usar um termo técnico, explica na mesma frase.
- **Analogias do cotidiano:** traduz números grandes para coisas concretas (preço do pão, aluguel, tanque de gasolina, salário mínimo, conta de luz).
- **Bordões fixos (usar sempre):**
  - Abertura: "E se [tema]? Vamos imaginar."
  - Transição para os dois lados: "Agora, vamos colocar na balança."
  - Encerramento: "E aí, você toparia? Me conta nos comentários."
- **O que o narrador nunca faz:** dar veredito, chamar uma ideia de "absurda" ou "genial", usar adjetivos contra pessoas, ironizar eleitores de qualquer lado.

---

## 3. Estrutura fixa de todo vídeo (45–60s)

1. **Gancho (0–3s):** a pergunta "E se...?" com um número ou imagem de impacto.
2. **Contexto (3–10s):** como é hoje, em uma frase, com um dado real.
3. **O que mudaria (10–30s):** consequências no curto e no longo prazo, sempre pelo ponto de vista do "cidadão comum".
4. **A balança (30–50s):** o argumento mais forte de quem defende e o argumento mais forte de quem critica, com o mesmo tempo de tela e o mesmo tom.
5. **Exemplo real (se existir):** país ou período histórico parecido, sem exagerar a comparação.
6. **Encerramento (últimos 5s):** bordão final e pergunta aberta. Sem conclusão.

---

## 4. Identidade visual fixa

- **Estilo:** 3D low-poly, cores chapadas, iluminação suave, câmera sempre em movimento lento.
- **Paleta:** fundo azul-escuro (#1B2A41), destaque amarelo (#FFC93C), positivo verde (#3DDC97), negativo coral (#FF6B6B), texto branco.
- **Personagem fixo:** "o Zé", um cidadão ORIGINAL low-poly (camiseta amarela, calça azul, sem semelhança com nenhum personagem ou pessoa conhecida). Ele aparece em todo vídeo reagindo às mudanças: preço subindo, salário rendendo mais, fila no banco etc.
- **Elemento recorrente:** uma balança 3D que aparece no bloco "A balança", com o lado verde e o lado coral equilibrados no começo da cena.
- **Legendas:** fonte grande e em negrito (ex.: Montserrat ExtraBold), centralizadas, com a palavra falada destacada em amarelo.
- **Dados na tela:** contadores animados e, no canto inferior, a fonte em letra pequena (ex.: "Fonte: IBGE, 2026").
- **Proibido:** retratar pessoas reais, políticos, logotipos de partidos, símbolos de campanha ou músicas protegidas.

---

## 5. Temas

**No escopo agora:** ideias socioeconômicas e econômicas em geral (ex.: parar de imprimir dinheiro, adotar Bitcoin como moeda, imposto único, renda básica, padrão-ouro, fim das tarifas de importação). Usar dados oficiais e estudos de escolas econômicas diferentes.

**Fora do escopo por enquanto:** propostas de candidatos, partidos, projetos de lei de parlamentares específicos e qualquer conteúdo eleitoral.

**Compromisso com a realidade:** todo cenário precisa ser plausível no Brasil real, com o funcionamento real das instituições, dos mercados e das leis. Nada de "e se" mágico que ignora como as coisas funcionam. Se a premissa exige uma simplificação, o vídeo diz qual é.

---

## 6. Fluxo de produção em ondas

Você executa sozinho tudo que é técnico, mas **para e me espera** nos pontos marcados com 🛑. Registre cada onda em `videos/[slug]/revisoes.md`, para eu conseguir ler a discussão inteira.

### Onda 1 — Elaboração da ideia
Defina a pergunta "E se...?" com precisão: o que exatamente muda, a partir de quando, em que escala e o que fica igual. Liste as premissas assumidas e as perguntas que o vídeo precisa responder. Salve em `ideia.md`.

### Onda 2 — Desenvolvimento
Pesquise e crie `fontes.md` (cada dado com link e data de acesso; sem fonte confiável, o dado fica de fora). Escreva o `roteiro.md` seguindo a seção 3, marcando cada frase como **[FATO]**, **[PROJEÇÃO]** ou **[ARGUMENTO DE UM LADO]**.

### Onda 3 — Contestação (agente crítico)
Chame o subagente `critico` (definido em `.claude/agents/critico.md`). Ele recebe só `ideia.md`, `roteiro.md` e `fontes.md`, sem a sua justificativa, e tenta derrubar o roteiro: dados errados ou desatualizados, causalidade exagerada, premissas irreais, lado mais fraco apresentado de forma caricata, frases que permitem interpretação enviesada, exemplos históricos mal comparados. Cada objeção vem classificada como **CRÍTICA**, **IMPORTANTE** ou **MENOR**.

### Onda 4 — Adaptação
Responda a cada objeção no `revisoes.md`: aceite e corrija o roteiro, ou rejeite explicando por quê com fonte. Não rejeite uma objeção só para manter o texto, e também não aceite uma objeção só para encerrar o debate. Objeções sem base, que exijam certeza impossível sobre o futuro ou que distorçam o que o roteiro diz devem ser rejeitadas e marcadas como tal.

**O objetivo das ondas 3 e 4 é aproximar o cenário da realidade, não derrubá-lo.** Ninguém prevê o futuro com certeza; o roteiro está certo quando separa com honestidade o que é sabido, o que é provável e o que é incerto. Uma afirmação verdadeira e bem fundamentada nunca deve ser retirada só porque o crítico insistiu.

### Repetição das ondas 3 e 4
Repita contestação e adaptação até que o crítico não encontre nenhuma objeção CRÍTICA ou IMPORTANTE nova, com no máximo 4 rodadas. Se após 4 rodadas ainda houver objeção crítica, o tema não está pronto: pare e me explique o impasse.

### 🛑 REVISÃO HUMANA 1 — Roteiro
Mostre o roteiro final, as fontes e um resumo do debate: o que o crítico derrubou, o que mudou e o que ficou em aberto. Responda também:
- Os dois lados têm o mesmo espaço e o mesmo tom?
- Alguma frase pode ser recortada e circular com sentido distorcido?
- Todo número tem fonte e está atualizado?

### Produção
1. **Narração:** edge-tts, voz pt-BR-AntonioNeural, ritmo +10% (sempre igual). Salve os tempos de cada palavra.
2. **Prévia:** cenas no HyperFrames (HTML + GSAP + Three.js) seguindo a seção 4 e o `ESTRUTURA.md`, renderizadas em baixa resolução.
3. 🛑 **REVISÃO HUMANA 2 — Prévia.** Espere meus ajustes.
4. **Final:** renderize `videos/[slug]/final.mp4` (1080x1920, 30fps) e confira se áudio, legendas e dados batem com o roteiro aprovado.

---

## 7. Regras técnicas

- Use apenas ferramentas gratuitas: Node, HyperFrames, GSAP, Three.js, edge-tts (o FFmpeg já vem por baixo do HyperFrames). Instale o que faltar sozinho.
- Reaproveite os componentes já criados (o Zé, a balança, as legendas, os contadores) em vez de recriar a cada vídeo. Mantenha-os em `componentes/`, conforme o `ESTRUTURA.md`.
- Resolva erros técnicos sem me perguntar; só me chame nos pontos 🛑 ou se algo exigir pagamento ou login.

---

## 8. Publicação

No modo de validação, nada é publicado. Se um dia isso mudar, todo vídeo feito com IA leva aviso de IA visível no vídeo e no post, e as regras eleitorais vigentes do TSE devem ser pesquisadas antes.
