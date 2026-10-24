# Cartões

Elementos 2D das cenas, na largura da área segura (a cena define só o `top`):

- `.numero-grande`: número de impacto em amarelo com contorno; `<span class="legenda-numero">` embaixo.
- `.cartao` (com `.positivo`, `.negativo` ou `.destaque` para a cor da borda): `<span class="titulo-cartao">`, texto e `<span class="menor">`.
- `.linha-de-etiquetas` com `.etiqueta` (mesmas cores).

Entradas e saídas ficam na timeline GSAP da cena (`fromTo` de `opacity` e `y`), nunca em CSS.
