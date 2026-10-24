# Palco

Base das cenas 3D: `palco.js` cria renderizador, câmera, luzes suaves (com a luz de frente que evita o rosto escuro) e o chão; `animacao.js` tem as funções de transição em função do tempo usadas pelo Zé e pela balança.

```js
import { criarPalco, aoBuscar, moverCamera, naTela } from "./componentes/palco/palco.js";
const B = TEMPOS.bloco(3);                       // tempos do bloco (gerados pelo montar.py)
const { renderer, cena, camera } = criarPalco(document.getElementById("b3-palco"));
aoBuscar(B, (t) => {                             // t = tempo local do bloco (0 no começo)
  // posicione tudo em função de t
  moverCamera(camera, t, { altura: 1.6, distancia: 10.5, alvo: [0, 1.1, 0] }); // câmera sempre se movendo devagar
  renderer.render(cena, camera);
});
```

Importante: o evento `hf-seek` do HyperFrames traz o tempo do vídeo inteiro, não o da cena; o `aoBuscar` faz a conta e só desenha enquanto o bloco está na tela.
