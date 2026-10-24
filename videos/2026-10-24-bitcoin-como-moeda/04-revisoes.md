# Revisões

## Rodada 1

### O que o crítico considerou sólido
- F8 conferido: o Iudop/UCA deu 91,8% de "não usaram" em 2024 (pergunta sobre usar para comprar ou pagar algo); "mais de nove em cada dez" está correto.
- F14 conferido: −64,2% em 2022 e +155,4% em 2023, em dólar (a página de 2023 do DQYDJ tem erro nos preços, não no percentual).
- F7 conferido: reforma por 55 a 2, no acordo de US$ 1,4 bilhão com o FMI; aceitação privada voluntária. As fontes divergem sobre o "curso legal", e o roteiro só dizia que a obrigação caiu.
- F1 conferido (4,67 milhões de CPFs em jun. 2026, também no Blocktrends; dados preliminares).
- F11, F22 e F23 tratados como fatos estabelecidos; o "mais de 85%" é seguro porque a perda só cresce.
- A direção do termômetro (maioria contra o Bitcoin como moeda oficial) está correta; os problemas eram de datação e de fonte.

### Objeções
| # | Trecho | Nível | Objeção | Base | Resposta do autor | Decisão |
|---|--------|-------|---------|------|-------------------|---------|
| R1.1 | "O FMI recomenda que nenhum país faça do Bitcoin moeda oficial, e a maioria dos economistas consultados vê utilidade limitada nele como dinheiro." | IMPORTANTE | A única pesquisa por trás de "a maioria dos economistas consultados" é de 2013 (38 economistas dos EUA), conferida só pelo TechCrunch; "como dinheiro" é inferência; o espectador entende como pesquisa atual; o termômetro não tinha fonte na tela; o FMI é posição institucional e credor de El Salvador. | 02-fontes (F17 e ressalvas); TechCrunch, 24/04/2013. | Procede. A frase agora data e localiza a pesquisa e admite a falta de evidência nova: "na única pesquisa com economistas sobre isso que achei, de 2013, a maioria viu utilidade limitada nele"; saiu "como dinheiro". A tela ganhou "FMI, 2023 · economistas dos EUA, 2013" (com rodapé de F11 e F17). O FMI fica, porque a frase o apresenta como recomendação institucional, não como pesquisa; a ressalva de credor segue no 02-fontes. Saiu também "Como investimento, há mais incerteza": ela se apoiava em F18, de 2017, com o mesmo problema de datação, e custava tempo. | aceita |
| R1.2 | "Depois, a obrigação de aceitar caiu por lá." | IMPORTANTE | Logo depois do "9 em cada 10 não usaram", a sequência sugere que o baixo uso derrubou a obrigação; ela caiu como condição de um empréstimo do FMI. Recortada, vira "El Salvador desistiu porque ninguém usava". | Reuters/The Block, Decrypt, Electronic Payments International (F5, F7). | Procede. A correção sugerida ("num acordo de empréstimo com o FMI") somava cerca de 7 palavras, e as outras correções já levavam o vídeo a 86 s. Seguindo a regra do CLAUDE.md (cortar o exemplo real antes de apertar a balança), a frase saiu; o recuo, com a causa certa, fica no 01-ideia e no 02-fontes (F7, F12). O cartão "Obrigatório → Opcional" saiu da cena. | aceita (resolvida com corte) |
| R1.3 | "em El Salvador, que usa o dólar, mais de nove em cada dez pessoas não usaram Bitcoin em 2024" | IMPORTANTE | O 01-ideia prometia dizer que o dólar é mais estável que o real, e "que usa o dólar" não diz; é aí que o lado a favor tem seu melhor contra-argumento (onde a moeda corrói, a procura por alternativa tende a ser maior), e o "pouco mudasse" fica mais firme que a evidência; 2024 é o terceiro ano, sem bônus (em 2021, cerca de 1 em 4 usou). | F8; F2; 01-ideia. | Procede. Nova frase [FATO] logo depois do dado: "Mas lá se usa o dólar, de inflação menor que a do real", com nova fonte F24 (2025: EUA 2,7% e Brasil 4,26%; 2024: 2,9% e 4,83%) e as duas taxas na tela. O "talvez" da projeção continua. O uso de 1 em 4 no primeiro ano, com bônus, não entrou por tempo; fica em F8 e F10. | aceita em parte |
| R1.4 | "se fossem muitos, o Banco Central perderia força contra a inflação" | MENOR | F11 fala em minar a eficácia da política monetária, não em inflação; a cena mostra a substituição como fato e o texto como hipótese; salários e impostos em reais limitariam a troca. | F11. | Procede. Agora: "se muitos trocassem de moeda, os juros do Banco Central perderiam força contra a inflação", que é o mecanismo de F11 (a ferramenta do Banco Central são os juros). Na cena, a alavanca fica tracejada e com um "e se...?". O limite dado por salários e impostos em reais não entrou por tempo; a frase segue no condicional. | aceita em parte |
| R1.5 | "Quase cinco milhões de brasileiros usaram criptomoedas num só mês." | MENOR | São 4,67 milhões de CPFs em operações informadas à Receita, cerca de 70% do volume em USDT: investimento e câmbio, não pagamento. "Usaram" sugere uso como dinheiro e "quase cinco" arredonda para cima. O "+21%" do F1 diverge entre as fontes (+4,6% no Blocktrends). | Blocktrends; Investnews/BPMoney. | Procede. Agora: "4,6 milhões de brasileiros negociaram criptomoedas num só mês" (arredondado para baixo, com 4,67 milhões na tela). Não cabe "mais de" sem passar dos 4 s que o `roteiro.py` dá ao impacto do gancho. F1 corrigido: o crescimento diverge e não é usado; cerca de 70% em USDT (R$ 199,5 bi), conferido por busca. | aceita |
| R1.6 | "Hoje, o Bitcoin é legal aqui, mas como um bem digital, não como moeda." | MENOR | "Legal" soa como "curso legal", justamente o ponto em jogo; o termo da regulação é "ativo virtual". | Lei 14.478/2022; F3. | Procede. Agora: "Hoje, ele é permitido aqui como ativo virtual, não como moeda." A plaquinha da cena acompanha. | aceita |
| R1.7 | Simplificações do 01-ideia (impostos e custo de conversão) | MENOR | O 01-ideia diz que o vídeo precisa informar as simplificações, e esses dois itens não aparecem. Opcional: mostrar que a oscilação continua (cerca de 35% abaixo do recorde de out. 2025, F15). | 01-ideia; F15. | Procede em parte. Impostos e custo de conversão são detalhes que não mudam a direção do cenário, e não premissas; o 01-ideia foi corrigido e os separa das simplificações que o vídeo diz. O dado de F15 não entrou: o lado contra já mostra a oscilação nos dois sentidos, e o tempo está no limite. | aceita em parte (01-ideia corrigido) |

### Veredito do crítico
Nenhuma objeção CRÍTICA; três IMPORTANTES (R1.1, R1.2, R1.3), todas de correção curta, e quatro MENORES. "Depois das três correções, o roteiro está pronto." Não conferidos pelo crítico: o texto original do FMI (F11), a Lei 14.478/2022, as Resoluções do BCB (F3), F22, F23 e o enunciado exato do painel de 2013; a busca dele também não achou pesquisa com economistas sobre o Bitcoin como moeda de curso legal, nem com brasileiros.

### Mudanças da versão 2
- Gancho, contexto e longo prazo reescritos (R1.5, R1.6, R1.4); nova frase sobre o dólar com F24 (R1.3); termômetro datado e com fonte na tela (R1.1); frase do recuo de El Salvador cortada (R1.2).
- Duração estimada: cerca de 81 s (228 palavras), a mesma da versão 1. As correções somaram cerca de 20 palavras, compensadas com o corte da frase do recuo, a cláusula sobre investimento no termômetro e frases mais curtas no contexto e no longo prazo.

## Rodada 2

### O que o crítico considerou sólido
- F24 conferido: IPCA de 4,26% em 2025 e 4,83% em 2024 (IBGE); CPI dos EUA de 2,7% em dez./2025 (BLS); El Salvador perto de 1% (1,14% em nov./2025). A frase da R1.3 está certa e não cria viés.
- F17 conferido no TechCrunch (2013): 87% e "utilidade limitada", com a volatilidade como motivo, entre 38 economistas. Não há pesquisa mais recente sobre a função monetária do Bitcoin (o painel CFM-CEPR de 2017 trata de risco sistêmico; a enquete do WSJ de 2017, de bolha); a ressalva "a única que achei" continua honesta.
- F1: R$ 283 bi no 1º semestre de 2026, a maior parte em USDT, bate em várias fontes; "mais de 4 milhões de CPFs por mês" é compatível com "4,6 milhões".
- As correções R1.3, R1.4 e R1.6 estão certas; a balança tem 33 palavras a favor e 27 contra, os dois lados com dado.

### Objeções
| # | Trecho | Nível | Objeção | Base | Resposta do autor | Decisão |
|---|--------|-------|---------|------|-------------------|---------|
| R2.1 | "na única pesquisa com economistas sobre isso que achei, de 2013" | MENOR | Criada pela R1.1: "sobre isso" passou a apontar para "moeda oficial", e a pesquisa de 2013 não perguntou isso. | TechCrunch, 2013 (F17). | Procede, com ajuste: "sobre o Bitcoin" sozinho ficaria falso, porque há outras pesquisas do Clark Center sobre Bitcoin e cripto, sobre valor fundamental, propósito econômico e reservas públicas (F18, F20, F19). Ficou "sobre o Bitcoin como dinheiro", que é o que a pesquisa de 2013 avaliou (utilidade limitada, pela volatilidade) e o que o crítico diz não ter versão mais nova. Custo: 2 palavras. | aceita em parte |
| R2.2 | Cartão de El Salvador (bloco 3), depois do corte do recuo na R1.2 | MENOR | Nenhuma frase é falsa (lei de 2021, dado de 2024, obrigação até jan./2025), mas a omissão pode parecer que o vídeo esconde o recuo. Correção opcional: nota no cartão, com a causa junto. | F5, F7; reforma de 29/01/2025 e acordo com o FMI. | Procede. A tela do dado ganhou a nota "obrigação em vigor até jan./2025; depois, voluntária (acordo com o FMI)", com F7 no rodapé. A fala não muda, então não custa tempo. | aceita |

### Veredito do crítico
Nenhuma objeção CRÍTICA nem IMPORTANTE nova. O roteiro está pronto, com as incertezas já declaradas: a pesquisa com economistas é antiga, não há dado sobre o Bitcoin como moeda de curso legal e os documentos foram conferidos só por busca.

### Mudanças da versão 3
- Termômetro: "sobre isso" virou "sobre o Bitcoin como dinheiro" (R2.1).
- Cartão de El Salvador com a nota do recuo e a causa (R2.2), sem mudar a fala.
- Duração estimada: cerca de 82 s (231 palavras), abaixo do máximo de 90 s e acima da meta de 75 s.

## Resumo final para a revisão humana
- **O que mudou (versão 1 → 3):**
  - argumento a favor com base numérica (teto de 21 milhões, F22; real com mais de 85% de perda de poder de compra desde 1994, F23), antes da onda 3;
  - termômetro datado, com origem da pesquisa, fonte na tela e a admissão de que não há pesquisa mais nova (R1.1, R2.1);
  - diferença de El Salvador dita no vídeo, com a inflação do dólar menor que a do real (R1.3, F24);
  - frase que sugeria causa errada para o recuo de El Salvador cortada da fala; o recuo, com a causa certa, ficou só na nota do cartão (R1.2, R2.2);
  - gancho sem arredondar para cima e com "negociaram" no lugar de "usaram" (R1.5); "ativo virtual" no contexto (R1.6); longo prazo pelo mecanismo dos juros (R1.4).
- **O que ficou em aberto:**
  - não há pesquisa com economistas sobre o Bitcoin como moeda oficial, nem com economistas brasileiros; o termômetro se apoia no FMI (posição institucional e credor de El Salvador) e numa pesquisa de 2013 com economistas dos EUA, e diz isso;
  - o enunciado exato da pesquisa de 2013 (F17) não foi visto, só o resultado (87%, "utilidade limitada");
  - o uso maior em El Salvador no primeiro ano (cerca de 1 em 4, com bônus) e o limite à troca de moeda dado por salários e impostos em reais ficaram fora do vídeo, por tempo;
  - a perda de poder de compra do real foi conferida até meados de 2024; o vídeo diz "mais de 85%", que continua valendo;
  - duração estimada de 82 s, acima da meta de 75 s.
- **Links principais a abrir (tudo foi conferido só por busca):**
  - F1, Receita (via Money Times): https://www.moneytimes.com.br/criptomoedas-movimentam-r-283-bilhoes-no-primeiro-semestre-e-batem-novo-recorde-diz-receita-rens/
  - F3, Banco Central (via Mattos Filho): https://www.mattosfilho.com.br/unico/normas-regulamentacao-ativos-virtuais/
  - F7, reforma de El Salvador (via The Block): https://www.theblock.co/amp/post/337885/el-salvador-passes-bill-to-revise-bitcoin-adoption-strategy-per-imf-deal-reuters
  - F8, Iudop (via El Salvador Now): https://www.elsalvadornow.org/2025/01/17/92-of-salvadorans-did-not-use-bitcoin-in-2024-el-92-de-salvadorenos-no-uso-bitcoin-en-2024/
  - F11, FMI: https://www.imf.org/en/News/Articles/2023/02/23/pr2351-imf-executive-board-discusses-elements-of-effective-policies-for-crypto-assets
  - F14, DQYDJ: https://dqydj.com/2022-bitcoin-return
  - F17, Clark Center: http://www.igmchicago.org/surveys/bitcoins (e TechCrunch: https://techcrunch.com/2013/04/24/austan_goolsbee-on-bitcoins-usefulness-hahahaha-rotfl/amp)
  - F22, teto de 21 milhões (The Block): https://www.theblock.co/amp/post/379061/bitcoins-mined-supply-95-per-cent-21-million-cap-more-century-issuance-left
  - F23, IPCA desde 1994 (via Movimento Econômico): https://movimentoeconomico.com.br/dinheiro/2024/07/01/real-completa-30-anos-com-desafio-de-manter-poder-de-compra/
  - F24, inflação no Brasil e nos EUA: https://numerando.com.br/indices/ipca/acumulado e https://www.hl.co.uk/news/the-us-ended-2025-with-steady-but-elevated-inflation-in-december
- **As quatro perguntas da revisão humana (CLAUDE.md, seção 6):**
  - *Os dois lados têm o mesmo espaço e o mesmo tom?* Sim. São 33 palavras a favor e 27 contra (razão 1,22, dentro de 0,8–1,25). O lado a favor fica um pouco mais longo porque os números são lidos por extenso. Os dois lados usam o mesmo verbo ("aponta que") e têm dado concreto: 21 milhões e a inflação do real a favor; −64% e +155% contra.
  - *O termômetro reflete onde os especialistas estão, com fonte?* Sim, com as ressalvas ditas no vídeo: o FMI recomenda não fazer (F11, posição institucional), e a única pesquisa com economistas sobre o Bitcoin como dinheiro é de 2013, dos EUA (F17), com maioria vendo utilidade limitada. As duas fontes estão na tela.
  - *Alguma frase pode ser recortada e circular com sentido distorcido?* O ponto de atenção é "o real perdeu mais de 85% do poder de compra desde o Plano Real": é fato, mas recortado pode virar ataque ao real. Ele vem dentro de "Quem defende aponta que..." e na mesma frase do teto do Bitcoin, e é respondido pelo lado contra. O gancho diz "negociaram", não "pagaram"; a projeção de curto prazo tem "talvez"; o dado de El Salvador vem seguido da diferença do dólar e, na tela, do recuo com a causa.
  - *Todo número tem fonte e está atualizado?* Sim: todo número tem código no 02-fontes, e o `roteiro.py` confere. Os mais recentes são de 2025 e 2026 (F1, F24). Três números são mais antigos, e o vídeo diz a data de cada um: o uso em El Salvador é de 2024, a pesquisa mais recente do Iudop achada; a oscilação do Bitcoin é de 2022–2023; a perda do real foi calculada até 2024, e "mais de 85%" continua valendo. A pesquisa com economistas é de 2013, e o vídeo diz isso.
