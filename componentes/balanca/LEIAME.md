# Balança

Balança 3D do bloco "A balança": prato verde (`--positivo`) à esquerda, coral (`--negativo`) à direita. Começa equilibrada e, sem marcação explícita de inclinação no roteiro, termina equilibrada. Exemplo em `videos/2026-10-24-fim-das-tarifas-de-importacao/composicao/cenas/bloco-4.html`.

```js
import { criarBalanca } from "./componentes/balanca/balanca.js";
const balanca = criarBalanca({ escala: 0.8 });
cena.add(balanca.grupo);
balanca.posar(t, {
  entrada: 0.2,                                              // quando aparece (cresce com sobra)
  destaque: [[0, null], [2, "esquerda"], [9, "direita"], [16, null]], // prato que acende
  inclinacao: [[0, 0]],                                      // -1 (coral desce) a 1 (verde desce); só com marcação no roteiro
});
const p = naTela(balanca.centroDoPrato("esquerda"), camera); // posição na tela, para rótulos HTML
```
