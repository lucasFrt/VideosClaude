// Funções de animação em função do tempo, usadas pelos componentes 3D (Zé, balança).
// Nenhuma guarda estado: o mesmo t sempre dá o mesmo resultado.

export const limitar = (x) => Math.min(1, Math.max(0, x));
export const suave = (k) => k * k * (3 - 2 * k);

// Chega com uma pequena sobra e assenta: dá peso aos gestos.
export const comSobra = (k) => {
  const c = 1.1;
  return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2;
};

export function misturar(a, b, k) {
  if (a === null || b === null || typeof a === "string") return k < 0.5 ? a : b;
  if (typeof a === "number") return a + (b - a) * k;
  if (Array.isArray(a)) return a.map((v, i) => misturar(v, b[i], k));
  const r = {};
  for (const chave of Object.keys(a)) r[chave] = misturar(a[chave], b[chave], k);
  return r;
}

// Valor no tempo t de uma lista de chaves [[t0, v0], [t1, v1], ...]. Cada chave começa
// uma transição a partir de onde o valor estava naquele instante, então trocas rápidas
// não dão saltos.
export function transicao(chaves, t, valorDe, duracao, curva, atraso = 0) {
  let atual = valorDe(chaves[0][1]);
  for (let i = 1; i < chaves.length; i++) {
    const inicio = chaves[i][0] + atraso;
    if (t < inicio) break;
    const proxima = i + 1 < chaves.length ? chaves[i + 1][0] + atraso : Infinity;
    const k = limitar((Math.min(t, proxima) - inicio) / duracao);
    atual = misturar(atual, valorDe(chaves[i][1]), curva(k));
  }
  return atual;
}
