// Balança 3D do bloco "A balança" (ESTRUTURA.md, seção 5): prato verde à esquerda,
// coral à direita. Começa equilibrada e, sem marcação explícita no roteiro, termina
// equilibrada. Tudo em função do tempo.
//
// Uso dentro de uma cena (<script type="module">):
//   import { criarBalanca } from "./componentes/balanca/balanca.js";
//   const balanca = criarBalanca();
//   cena.add(balanca.grupo);
//   balanca.posar(t, {
//     entrada: 0.2,                                      // quando aparece
//     destaque: [[0, null], [2, "esquerda"], [6, "direita"], [10, null]],
//     inclinacao: [[0, 0]],                              // de -1 (coral desce) a 1 (verde desce)
//   });

import * as THREE from "../../assets/libs/three.module.js";
import { comSobra, limitar, suave, transicao } from "../palco/animacao.js";

const CORES = { estrutura: 0x8fa3c4, metal: 0xd7deea, positivo: 0x3ddc97, negativo: 0xff6b6b };
const BRACO = 1.35; // meia largura do travessão
const ALTURA = 2.25; // altura do eixo
const CORDA = 0.95;
const INCLINACAO_MAXIMA = 0.28; // radianos

function malha(geometria, cor, extra = {}) {
  return new THREE.Mesh(
    geometria,
    new THREE.MeshStandardMaterial({ color: cor, flatShading: true, roughness: 0.7, ...extra }),
  );
}

export function criarBalanca({ escala = 1 } = {}) {
  const grupo = new THREE.Group();
  const corpo = new THREE.Group();
  grupo.add(corpo);

  const base = malha(new THREE.CylinderGeometry(0.62, 0.78, 0.2, 8), CORES.estrutura);
  base.position.y = 0.1;
  const poste = malha(new THREE.CylinderGeometry(0.07, 0.1, ALTURA - 0.15, 6), CORES.estrutura);
  poste.position.y = (ALTURA - 0.15) / 2 + 0.15;
  const eixo = malha(new THREE.IcosahedronGeometry(0.13, 0), CORES.metal);
  eixo.position.y = ALTURA;
  const travessao = new THREE.Group();
  travessao.position.y = ALTURA;
  travessao.add(malha(new THREE.BoxGeometry(BRACO * 2, 0.08, 0.12), CORES.metal));
  corpo.add(base, poste, travessao, eixo);

  const pratos = [-1, 1].map((lado) => {
    const pendurado = new THREE.Group();
    const corda = malha(new THREE.CylinderGeometry(0.015, 0.015, CORDA, 4), CORES.metal);
    corda.position.y = -CORDA / 2;
    const cor = lado < 0 ? CORES.positivo : CORES.negativo;
    const prato = malha(new THREE.CylinderGeometry(0.62, 0.48, 0.12, 10), cor, { emissive: cor, emissiveIntensity: 0 });
    prato.position.y = -CORDA - 0.06;
    pendurado.add(corda, prato);
    corpo.add(pendurado);
    return { lado, pendurado, prato };
  });

  function posar(t, roteiro = {}) {
    const entrada = roteiro.entrada ?? 0;
    const inclinacoes = roteiro.inclinacao || [[0, 0]];
    const destaques = roteiro.destaque || [[0, null]];

    const aparecer = limitar((t - entrada) / 0.6);
    grupo.visible = aparecer > 0;
    corpo.scale.setScalar(escala * Math.max(0.001, comSobra(aparecer)));

    // Inclinação pedida no roteiro, mais um balanço mínimo para parecer viva
    const pedida = transicao(inclinacoes, t, (v) => v, 0.9, suave);
    const angulo = pedida * INCLINACAO_MAXIMA + 0.012 * Math.sin(t * 1.4) * aparecer;
    travessao.rotation.z = angulo;

    for (const { lado, pendurado, prato } of pratos) {
      // A ponta do travessão gira com ele; o prato pendurado continua na horizontal.
      pendurado.position.set(lado * BRACO * Math.cos(angulo), ALTURA + lado * BRACO * Math.sin(angulo), 0);
      const nome = lado < 0 ? "esquerda" : "direita";
      const peso = transicao(destaques, t, (d) => (d === nome ? 1 : 0), 0.3, suave);
      prato.material.emissiveIntensity = 0.45 * peso;
      prato.scale.setScalar(1 + 0.08 * peso);
    }
  }

  posar(0);
  return {
    grupo,
    posar,
    // Centro de cada prato no mundo, para pôr rótulos (palco.naTela).
    centroDoPrato: (lado) => {
      const p = pratos[lado === "esquerda" ? 0 : 1].prato;
      return p.getWorldPosition(new THREE.Vector3());
    },
  };
}
