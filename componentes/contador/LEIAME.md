# Contador

Número animado de um valor a outro, com formatação brasileira (`R$ 1.234,56`, `12,5%`) e algarismos de largura fixa (`contador.css`). O valor de cada quadro sai do tempo da timeline.

```js
import { contar, formatar } from "./componentes/contador/contador.js";
contar(tl, document.getElementById("b2-receita-n"), {
  de: 0, para: 90, prefixo: "R$ ", sufixo: " bi", casas: 0, inicio: 1.2, duracao: 1.4,
});
formatar(1234.5, { prefixo: "R$ ", casas: 2 }); // "R$ 1.234,50"
```

Todo número na tela precisa de `tela` e `fontes` na frase do roteiro: é isso que faz o `montar.py` pôr o rodapé de fonte.
