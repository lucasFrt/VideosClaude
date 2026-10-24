// O Zé: o personagem fixo do canal (ESTRUTURA.md, seção 5). Low-poly e original.
// Tudo é calculado a partir do tempo t: posar(t) pode ser chamado em qualquer ordem
// e sempre desenha o mesmo quadro (ESTRUTURA.md, seção 6, regra 3).
//
// Uso dentro de uma cena (<script type="module">):
//   import { criarZe } from "./componentes/ze/ze.js";
//   const ze = criarZe({ escala: 1 });
//   cena.add(ze.grupo);
//   const roteiro = {
//     posicao: [[0, [-2, 0, 0]], [1.5, [0, 0, 0]]],    // anda sozinho entre as posições
//     rotacao: [[0, 1.2], [1.5, 0]],                   // ângulo em y (0 = de frente)
//     expressao: [[0, "neutro"], [2, "feliz"]],        // neutro, feliz, preocupado, surpreso
//     gesto: [[0, "parado"], [2, "comemora"]],         // parado, aponta, ombros, comemora
//   };
//   window.addEventListener("hf-seek", (e) => { ze.posar(e.detail.time, roteiro); renderer.render(cena, camera); });

import * as THREE from "../../assets/libs/three.module.js";
import { comSobra, limitar, misturar, suave, transicao } from "../palco/animacao.js";

const CORES = {
  camiseta: 0xffc93c, // --destaque
  calca: 0x3b6ea8,
  pele: 0xc68e5e,
  cabelo: 0x2a1e17,
  sapato: 0x2b2b33,
  detalhe: 0x1a1414, // olhos, sobrancelhas e boca
};

const EXPRESSOES = {
  neutro: { sobrancelhaY: 0, sobrancelhaGiro: 0, olho: 1, neutra: 1, sorriso: 0, triste: 0, aberta: 0 },
  feliz: { sobrancelhaY: 0.012, sobrancelhaGiro: -0.12, olho: 0.85, neutra: 0, sorriso: 1, triste: 0, aberta: 0 },
  preocupado: { sobrancelhaY: 0.008, sobrancelhaGiro: 0.38, olho: 1, neutra: 0, sorriso: 0, triste: 1, aberta: 0 },
  surpreso: { sobrancelhaY: 0.05, sobrancelhaGiro: 0, olho: 1.35, neutra: 0, sorriso: 0, triste: 0, aberta: 1 },
};

// Cada braço: abertura (para o lado), frente (para a frente) e cotovelo, em radianos.
// "lado" é o braço do lado direito da tela (x > 0); "outro" é o do lado esquerdo.
const BRACO_PARADO = { abertura: 0.12, frente: 0, cotovelo: -0.15 };
const GESTOS = {
  parado: { lado: BRACO_PARADO, outro: BRACO_PARADO, cabecaY: 0, cabecaX: 0, cabecaZ: 0, ombros: 0, pulo: 0, giro: 0 },
  aponta: {
    lado: { abertura: 1.25, frente: -0.4, cotovelo: -0.05 },
    outro: BRACO_PARADO,
    cabecaY: 0.4, cabecaX: 0, cabecaZ: 0, ombros: 0, pulo: 0, giro: 0.12,
  },
  ombros: {
    lado: { abertura: 0.5, frente: -0.3, cotovelo: -1.35 },
    outro: { abertura: 0.5, frente: -0.3, cotovelo: -1.35 },
    cabecaY: 0, cabecaX: 0, cabecaZ: 0.16, ombros: 0.07, pulo: 0, giro: 0,
  },
  comemora: {
    lado: { abertura: 2.55, frente: -0.15, cotovelo: -0.35 },
    outro: { abertura: 2.55, frente: -0.15, cotovelo: -0.35 },
    cabecaY: 0, cabecaX: -0.18, cabecaZ: 0, ombros: 0.03, pulo: 1, giro: 0,
  },
};

const PASSADA = 0.55; // distância de meio passo, em unidades da cena

// Posição em trechos retos, com saída e chegada suaves; devolve também a distância
// percorrida, que comanda as pernas.
function trajeto(chaves, t) {
  let distancia = 0;
  for (let i = 1; i < chaves.length; i++) {
    const [t0, p0] = chaves[i - 1];
    const [t1, p1] = chaves[i];
    const trecho = Math.hypot(p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]);
    if (t < t1) {
      const k = t <= t0 ? 0 : suave((t - t0) / (t1 - t0));
      return { posicao: misturar(p0, p1, k), distancia: distancia + trecho * k };
    }
    distancia += trecho;
  }
  return { posicao: chaves[chaves.length - 1][1], distancia };
}

// Piscadas em intervalos variados, mas sempre os mesmos para o mesmo t.
function piscada(t) {
  const ciclo = 3.3;
  const n = Math.floor(t / ciclo);
  const sorteio = Math.abs(Math.sin(n * 12.9898 + 78.233) * 43758.5453) % 1;
  const fase = t - (n * ciclo + 0.4 + sorteio * 2.2);
  return fase >= 0 && fase < 0.14 ? 1 - 0.9 * Math.sin((Math.PI * fase) / 0.14) : 1;
}

// Antecipação e acomodação do tronco em volta de cada troca de gesto.
function impulso(chaves, t) {
  let s = 0;
  for (let i = 1; i < chaves.length; i++) {
    const u = t - chaves[i][0];
    s += -0.04 * Math.exp(-(((u + 0.03) / 0.05) ** 2)) + 0.025 * Math.exp(-(((u - 0.13) / 0.06) ** 2));
  }
  return s;
}

function malha(geometria, cor) {
  return new THREE.Mesh(geometria, new THREE.MeshStandardMaterial({ color: cor, flatShading: true, roughness: 0.85 }));
}

function criarBraco(lado) {
  const ombro = new THREE.Group();
  ombro.position.set(lado * 0.33, 0.6, 0);
  const manga = malha(new THREE.CylinderGeometry(0.105, 0.095, 0.2, 6), CORES.camiseta);
  manga.position.y = -0.07;
  const braco = malha(new THREE.CylinderGeometry(0.075, 0.07, 0.34, 6), CORES.pele);
  braco.position.y = -0.2;
  const cotovelo = new THREE.Group();
  cotovelo.position.y = -0.36;
  const antebraco = malha(new THREE.CylinderGeometry(0.07, 0.062, 0.3, 6), CORES.pele);
  antebraco.position.y = -0.15;
  const mao = malha(new THREE.IcosahedronGeometry(0.08, 0), CORES.pele);
  mao.position.y = -0.33;
  cotovelo.add(antebraco, mao);
  ombro.add(manga, braco, cotovelo);
  return { ombro, cotovelo };
}

function criarPerna(lado) {
  const quadril = new THREE.Group();
  quadril.position.set(lado * 0.13, 0.86, 0);
  const perna = malha(new THREE.CylinderGeometry(0.12, 0.11, 0.76, 6), CORES.calca);
  perna.position.y = -0.38;
  const sapato = malha(new THREE.BoxGeometry(0.18, 0.1, 0.3), CORES.sapato);
  sapato.position.set(0, -0.8, 0.05);
  quadril.add(perna, sapato);
  return quadril;
}

function criarCabeca() {
  const cabeca = new THREE.Group();
  cabeca.position.y = 0.98;
  const rosto = malha(new THREE.IcosahedronGeometry(0.3, 1), CORES.pele);
  const cabelo = malha(new THREE.SphereGeometry(0.318, 8, 5, 0, Math.PI * 2, 0, Math.PI * 0.48), CORES.cabelo);
  cabelo.position.set(0, 0.03, -0.025);
  cabelo.rotation.x = -0.25;
  const nariz = malha(new THREE.IcosahedronGeometry(0.045, 0), 0xb57d50);
  nariz.position.set(0, -0.02, 0.29);
  cabeca.add(rosto, cabelo, nariz);

  const olhos = [-1, 1].map((lado) => {
    const olho = malha(new THREE.SphereGeometry(0.036, 6, 4), CORES.detalhe);
    olho.position.set(lado * 0.1, 0.04, 0.285);
    cabeca.add(olho);
    return olho;
  });
  const sobrancelhas = [-1, 1].map((lado) => {
    const s = malha(new THREE.BoxGeometry(0.11, 0.022, 0.025), CORES.cabelo);
    s.position.set(lado * 0.1, 0.12, 0.28);
    s.userData.lado = lado;
    cabeca.add(s);
    return s;
  });

  const bocas = {
    neutra: malha(new THREE.BoxGeometry(0.11, 0.022, 0.02), CORES.detalhe),
    sorriso: malha(new THREE.TorusGeometry(0.065, 0.017, 4, 8, Math.PI), CORES.detalhe),
    triste: malha(new THREE.TorusGeometry(0.05, 0.015, 4, 8, Math.PI), CORES.detalhe),
    aberta: malha(new THREE.TorusGeometry(0.038, 0.015, 4, 10), CORES.detalhe),
  };
  bocas.sorriso.rotation.z = Math.PI; // arco virado para cima vira sorriso
  for (const [nome, boca] of Object.entries(bocas)) {
    boca.position.set(0, nome === "sorriso" ? -0.08 : nome === "triste" ? -0.14 : -0.12, 0.285);
    cabeca.add(boca);
  }
  return { cabeca, olhos, sobrancelhas, bocas };
}

export function criarZe({ escala = 1 } = {}) {
  const grupo = new THREE.Group();
  grupo.scale.setScalar(escala);

  const sombra = new THREE.Mesh(
    new THREE.CircleGeometry(0.42, 16),
    new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.28, depthWrite: false }),
  );
  sombra.rotation.x = -Math.PI / 2;
  sombra.position.y = 0.002;

  const corpo = new THREE.Group();
  const pernas = [-1, 1].map(criarPerna);
  const cintura = malha(new THREE.CylinderGeometry(0.25, 0.25, 0.14, 7), CORES.calca);
  cintura.position.y = 0.88;

  const tronco = new THREE.Group();
  tronco.position.y = 0.88;
  const camiseta = malha(new THREE.CylinderGeometry(0.31, 0.27, 0.66, 7), CORES.camiseta);
  camiseta.position.y = 0.33;
  const pescoco = malha(new THREE.CylinderGeometry(0.09, 0.1, 0.12, 6), CORES.pele);
  pescoco.position.y = 0.7;
  const bracos = { lado: criarBraco(1), outro: criarBraco(-1) };
  const rosto = criarCabeca();
  tronco.add(camiseta, pescoco, bracos.lado.ombro, bracos.outro.ombro, rosto.cabeca);

  corpo.add(...pernas, cintura, tronco);
  grupo.add(sombra, corpo);

  function posar(t, roteiro = {}) {
    const posicoes = roteiro.posicao || [[0, [0, 0, 0]]];
    const rotacoes = roteiro.rotacao || [[0, 0]];
    const expressoes = roteiro.expressao || [[0, "neutro"]];
    const gestos = roteiro.gesto || [[0, "parado"]];

    // Deslocamento e caminhada (o passo vem da distância percorrida)
    const { posicao, distancia } = trajeto(posicoes, t);
    const antes = trajeto(posicoes, t - 0.05).distancia;
    const andar = limitar(((distancia - antes) / 0.05) / 1.2);
    const fase = (distancia / PASSADA) * Math.PI;
    grupo.position.set(posicao[0], posicao[1], posicao[2]);
    grupo.rotation.y = transicao(rotacoes, t, (v) => v, 0.45, suave);

    // Gesto: cabeça na frente, braços logo atrás, cada um no seu tempo
    const g = (atraso, duracao) => transicao(gestos, t, (nome) => GESTOS[nome], duracao, comSobra, atraso);
    const cabecaG = g(0, 0.35);
    const ladoG = g(0.05, 0.42);
    const outroG = g(0.09, 0.46);

    const balanco = Math.sin(fase) * andar;
    pernas[0].rotation.x = balanco * 0.55;
    pernas[1].rotation.x = -balanco * 0.55;

    for (const [nome, lado, pose] of [["lado", 1, ladoG.lado], ["outro", -1, outroG.outro]]) {
      const { ombro, cotovelo } = bracos[nome];
      ombro.rotation.z = lado * pose.abertura;
      ombro.rotation.x = pose.frente + lado * balanco * 0.35 * (1 - limitar(pose.abertura - 0.2));
      ombro.position.y = 0.6 + cabecaG.ombros;
      cotovelo.rotation.x = pose.cotovelo;
    }

    // Respiração, antecipação e pulo de comemoração
    const respira = 0.012 * Math.sin((2 * Math.PI * t) / 3.4);
    const squash = impulso(gestos, t);
    tronco.scale.set(1 - squash * 0.6, 1 + respira + squash, 1 - squash * 0.6);
    tronco.rotation.y = cabecaG.giro;
    const pulo = cabecaG.pulo * Math.abs(Math.sin(t * 7.5)) * 0.12;
    corpo.position.y = Math.abs(Math.sin(fase)) * 0.035 * andar + Math.max(0, pulo);
    sombra.scale.setScalar(1 - pulo * 1.5);

    const cabeca = rosto.cabeca;
    cabeca.rotation.set(
      cabecaG.cabecaX + 0.03 * Math.sin((2 * Math.PI * t) / 4.1),
      cabecaG.cabecaY + 0.04 * Math.sin((2 * Math.PI * t) / 5.3),
      cabecaG.cabecaZ,
    );

    // Expressão
    const e = transicao(expressoes, t, (nome) => EXPRESSOES[nome], 0.3, suave);
    const pisca = piscada(t);
    for (const olho of rosto.olhos) olho.scale.set(e.olho, e.olho * pisca, e.olho);
    for (const s of rosto.sobrancelhas) {
      s.position.y = 0.12 + e.sobrancelhaY;
      s.rotation.z = -s.userData.lado * e.sobrancelhaGiro;
    }
    for (const [nome, boca] of Object.entries(rosto.bocas)) {
      const peso = Math.max(0, e[nome]);
      boca.scale.setScalar(peso);
      boca.visible = peso > 0.01;
    }
  }

  posar(0);
  return { grupo, posar, altura: 2.2 * escala };
}
