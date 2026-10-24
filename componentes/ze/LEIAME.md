# Zé

O personagem fixo do canal: low-poly, original, camiseta amarela e calça azul. **Protótipo em avaliação**: o estilo (3D feito em código) ainda precisa da sua aprovação (`docs/aprendizados.md`, item 17). Demonstração em `videos/2026-10-24-prototipo-ze/`; poses em `poses.jpg`.

## Uso

Dentro de uma cena (`<script type="module">`), com o Three.js do projeto:

```js
import * as THREE from "./assets/libs/three.module.js";
import { criarZe } from "./componentes/ze/ze.js";

const ze = criarZe({ escala: 1 });
cena.add(ze.grupo);

const roteiro = {
  posicao: [[0, [-1.5, 0, 0]], [1.7, [0, 0, 0]]],   // [tempo, [x, y, z]]: anda sozinho entre as posições
  rotacao: [[0, 1.25], [1.5, 0]],                   // [tempo, ângulo em y]; 0 = de frente para a câmera
  expressao: [[0, "neutro"], [2, "surpreso"]],      // [tempo, expressão]
  gesto: [[0, "parado"], [3, "aponta"]],            // [tempo, gesto]
};

window.addEventListener("hf-seek", (e) => {
  ze.posar(e.detail.time, roteiro);
  renderer.render(cena, camera);
});
```

## Parâmetros

| Parâmetro | Valores |
|---|---|
| `escala` | tamanho (1 = cerca de 2,2 unidades de altura; `ze.altura` informa) |
| `posicao` | lista de `[tempo, [x, y, z]]`; entre duas posições ele anda, com passo proporcional à distância |
| `rotacao` | lista de `[tempo, ângulo]` (radianos em y) |
| `expressao` | `neutro`, `feliz`, `preocupado`, `surpreso` |
| `gesto` | `parado`, `aponta` (braço do lado direito da tela), `ombros`, `comemora` |

## Como ele se mexe

- Tudo é função do tempo: `posar(t)` desenha sempre o mesmo quadro para o mesmo `t`, em qualquer ordem (testado: dois renders com os mesmos bytes).
- Cada troca de expressão ou gesto é uma transição a partir de onde ele estava, então trocas rápidas não dão salto.
- Gestos chegam com uma pequena sobra e assentam; a cabeça vai na frente e cada braço no seu tempo; o tronco faz antecipação e acomodação.
- Sempre vivo: respiração, pequenos movimentos de cabeça e piscadas em intervalos variados, mas fixos.
- A sombra no chão é um disco escuro (barato e determinístico); a luz fica por conta da cena. Use uma luz de frente vinda da câmera, ou a parte de baixo do rosto escurece.
