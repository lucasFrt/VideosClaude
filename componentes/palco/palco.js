// Palco 3D padrão das cenas (CLAUDE.md, seção 4): renderizador, câmera, luz suave e chão.
// Uso dentro de uma cena (<script type="module">):
//   import { criarPalco, aoBuscar, moverCamera } from "./componentes/palco/palco.js";
//   const B = TEMPOS.bloco(3);
//   const { cena, camera, renderer } = criarPalco(document.getElementById("b3-palco"));
//   aoBuscar(B, (t) => { ...; moverCamera(camera, t); renderer.render(cena, camera); });

import * as THREE from "../../assets/libs/three.module.js";

export function criarPalco(canvas, { fov = 32, chao = true } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(1080, 1920, false);
  renderer.setClearColor(0x1b2a41);
  const cena = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(fov, 1080 / 1920, 0.1, 100);

  cena.add(new THREE.HemisphereLight(0xfff4e0, 0x5a6a88, 1.5));
  const principal = new THREE.DirectionalLight(0xfff1d6, 2.2);
  principal.position.set(-3, 5, 6);
  const contorno = new THREE.DirectionalLight(0x9fc4ff, 1.4);
  contorno.position.set(4, 3, -5);
  // Luz vinda da câmera: sem ela, a parte de baixo dos rostos escurece.
  const frente = new THREE.DirectionalLight(0xffffff, 1.1);
  frente.position.set(0, 1.5, 8);
  cena.add(principal, contorno, frente);

  if (chao) {
    const piso = new THREE.Mesh(
      new THREE.CircleGeometry(9, 24),
      new THREE.MeshStandardMaterial({ color: 0x24385a, flatShading: true, roughness: 1 }),
    );
    piso.rotation.x = -Math.PI / 2;
    cena.add(piso);
  }
  return { renderer, cena, camera };
}

// O hf-seek traz o tempo do vídeo inteiro, não o da cena. Esta função entrega à cena o
// tempo local do bloco (0 no começo dele) e só desenha enquanto o bloco está na tela.
export function aoBuscar(bloco, desenhar) {
  window.addEventListener("hf-seek", (e) => {
    const t = e.detail.time - bloco.inicioAbsoluto;
    if (t >= -0.05 && t <= bloco.duracao + 0.05) desenhar(Math.max(0, t));
  });
  desenhar(0);
}

// Câmera sempre em movimento lento: aproxima devagar e balança de leve.
export function moverCamera(camera, t, { altura = 1.55, distancia = 7.2, aproximacao = 0.07, balanco = 0.45, alvo = [0, 1.15, 0] } = {}) {
  camera.position.set(balanco * Math.sin(t * 0.25), altura, distancia - t * aproximacao);
  camera.lookAt(alvo[0], alvo[1], alvo[2]);
}

// Posição na tela (em px do quadro 1080x1920) de um ponto 3D, para pôr rótulos HTML.
export function naTela(ponto, camera) {
  const v = ponto.clone().project(camera);
  return { x: (v.x + 1) * 540, y: (1 - v.y) * 960 };
}
