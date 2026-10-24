// Número animado de um valor a outro, com formatação brasileira (ESTRUTURA.md, seção 5).
// Uso dentro de uma cena:
//   import { contar } from "./componentes/contador/contador.js";
//   contar(tl, document.getElementById("cena-numero"), { de: 0, para: 12, sufixo: "%", inicio: 0.4 });
// O valor é recalculado em cada quadro a partir do tempo da timeline (GSAP).

export function formatar(valor, { prefixo = "", sufixo = "", casas = 0 } = {}) {
  const numero = valor.toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });
  return `${prefixo}${numero}${sufixo}`;
}

export function contar(tl, elemento, opcoes) {
  const { de = 0, para, inicio = 0, duracao = 1.4, ease = "power2.out" } = opcoes;
  const estado = { valor: de };
  const escrever = () => (elemento.textContent = formatar(estado.valor, opcoes));
  escrever();
  tl.fromTo(estado, { valor: de }, { valor: para, duration: duracao, ease, onUpdate: escrever }, inicio);
}
