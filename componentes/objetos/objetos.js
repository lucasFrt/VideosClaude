// Objetos 3D low-poly do kit de cenas (contêiner, carro, fábrica). Genéricos: sem marcas,
// logotipos nem letreiros reais (CLAUDE.md, seção 4). Cada função devolve um THREE.Group
// com a base em y = 0; anime posição, escala e rotação na cena, em função do tempo.

import * as THREE from "../../assets/libs/three.module.js";

function malha(geometria, cor, extra = {}) {
  return new THREE.Mesh(
    geometria,
    new THREE.MeshStandardMaterial({ color: cor, flatShading: true, roughness: 0.8, ...extra }),
  );
}

export function criarConteiner({ cor = 0x3f8f8a } = {}) {
  const grupo = new THREE.Group();
  const caixa = malha(new THREE.BoxGeometry(2.6, 1.1, 1.1), cor);
  caixa.position.y = 0.55;
  grupo.add(caixa);
  // Nervuras na lateral e nas portas
  for (let i = -5; i <= 5; i++) {
    const nervura = malha(new THREE.BoxGeometry(0.06, 1.0, 0.04), cor);
    nervura.position.set(i * 0.22, 0.55, 0.57);
    grupo.add(nervura);
  }
  const porta = malha(new THREE.BoxGeometry(0.04, 1.0, 1.0), 0x2f6f6b);
  porta.position.set(1.31, 0.55, 0);
  grupo.add(porta);
  return grupo;
}

export function criarCarro({ cor = 0xe8edf5 } = {}) {
  const grupo = new THREE.Group();
  const corpo = malha(new THREE.BoxGeometry(1.9, 0.42, 0.85), cor);
  corpo.position.y = 0.4;
  const cabine = malha(new THREE.BoxGeometry(1.0, 0.36, 0.76), cor);
  cabine.position.set(-0.1, 0.79, 0);
  const vidro = malha(new THREE.BoxGeometry(1.02, 0.22, 0.78), 0x2a3b55);
  vidro.position.set(-0.1, 0.8, 0);
  grupo.add(corpo, cabine, vidro);
  for (const x of [-0.6, 0.6]) {
    for (const z of [-0.43, 0.43]) {
      const roda = malha(new THREE.CylinderGeometry(0.2, 0.2, 0.14, 8), 0x22252b);
      roda.rotation.x = Math.PI / 2;
      roda.position.set(x, 0.2, z);
      grupo.add(roda);
    }
  }
  for (const z of [-0.28, 0.28]) {
    const farol = malha(new THREE.BoxGeometry(0.04, 0.08, 0.14), 0xffe7a3, { emissive: 0xffe7a3, emissiveIntensity: 0.4 });
    farol.position.set(0.96, 0.45, z);
    grupo.add(farol);
  }
  return grupo;
}

export function criarFabrica({ cor = 0x7b8aa8 } = {}) {
  const grupo = new THREE.Group();
  const galpao = malha(new THREE.BoxGeometry(2.4, 1.0, 1.3), cor);
  galpao.position.y = 0.5;
  grupo.add(galpao);
  // Telhado em dente de serra
  for (let i = 0; i < 3; i++) {
    const dente = malha(new THREE.CylinderGeometry(0.4, 0.4, 1.3, 3), 0x5a6a88);
    dente.rotation.set(Math.PI / 2, 0, Math.PI / 2);
    dente.position.set(-0.8 + i * 0.8, 1.15, 0);
    grupo.add(dente);
  }
  const chamine = malha(new THREE.CylinderGeometry(0.12, 0.15, 1.1, 6), 0x5a6a88);
  chamine.position.set(0.9, 1.55, -0.3);
  const porta = malha(new THREE.BoxGeometry(0.5, 0.6, 0.04), 0x3a4660);
  porta.position.set(0, 0.3, 0.66);
  grupo.add(chamine, porta);
  for (const x of [-0.8, 0.8]) {
    const janela = malha(new THREE.BoxGeometry(0.4, 0.25, 0.04), 0xffe7a3, { emissive: 0xffe7a3, emissiveIntensity: 0.25 });
    janela.position.set(x, 0.62, 0.66);
    grupo.add(janela);
  }
  return grupo;
}
