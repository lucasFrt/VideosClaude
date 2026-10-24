// Gerado pelo scripts/montar.py a partir do palavras.json. Não edite.
// TEMPOS.bloco(n) devolve os tempos do bloco n com as frases em tempo local (0 = começo do bloco),
// que é o tempo da timeline da cena. Para o hf-seek, que traz o tempo do vídeo inteiro, use
// inicioAbsoluto (palco.aoBuscar já faz isso).
window.TEMPOS = {
  "duracao": 78.93,
  "estimado": true,
  "blocos": [
    {
      "numero": 1,
      "nome": "Gancho",
      "inicio": 0.0,
      "fim": 7.09,
      "duracao": 7.09,
      "frases": [
        {
          "inicio": 0.15,
          "fim": 2.8,
          "marcacao": "FATO",
          "fontes": [
            "F1"
          ],
          "tela": "12% (média)"
        },
        {
          "inicio": 3.27,
          "fim": 6.27,
          "marcacao": "BORDÃO",
          "fontes": [],
          "tela": null
        }
      ]
    },
    {
      "numero": 2,
      "nome": "Contexto",
      "inicio": 7.09,
      "fim": 22.83,
      "duracao": 15.74,
      "frases": [
        {
          "inicio": 7.09,
          "fim": 13.0,
          "marcacao": "FATO",
          "fontes": [
            "F2",
            "F3"
          ],
          "tela": "R$ 90 bi por ano"
        },
        {
          "inicio": 13.47,
          "fim": 17.24,
          "marcacao": "FATO",
          "fontes": [
            "F7"
          ],
          "tela": null
        },
        {
          "inicio": 17.71,
          "fim": 22.01,
          "marcacao": "PREMISSA",
          "fontes": [],
          "tela": null
        }
      ]
    },
    {
      "numero": 3,
      "nome": "O que mudaria",
      "inicio": 22.83,
      "fim": 44.57,
      "duracao": 21.74,
      "frases": [
        {
          "inicio": 22.83,
          "fim": 31.47,
          "marcacao": "PROJEÇÃO",
          "fontes": [
            "F4"
          ],
          "tela": null
        },
        {
          "inicio": 31.94,
          "fim": 37.05,
          "marcacao": "PROJEÇÃO",
          "fontes": [
            "F3"
          ],
          "tela": null
        },
        {
          "inicio": 37.52,
          "fim": 43.75,
          "marcacao": "PROJEÇÃO",
          "fontes": [
            "F5",
            "F9"
          ],
          "tela": null
        }
      ]
    },
    {
      "numero": 4,
      "nome": "A balança",
      "inicio": 44.57,
      "fim": 74.58,
      "duracao": 30.01,
      "frases": [
        {
          "inicio": 44.57,
          "fim": 46.32,
          "marcacao": "BORDÃO",
          "fontes": [],
          "tela": null
        },
        {
          "inicio": 46.79,
          "fim": 54.5,
          "marcacao": "ARGUMENTO A FAVOR",
          "fontes": [
            "F10",
            "F9"
          ],
          "tela": null
        },
        {
          "inicio": 54.97,
          "fim": 63.58,
          "marcacao": "ARGUMENTO CONTRA",
          "fontes": [
            "F5"
          ],
          "tela": null
        },
        {
          "inicio": 64.05,
          "fim": 73.76,
          "marcacao": "TERMÔMETRO",
          "fontes": [
            "F4",
            "F8",
            "F5",
            "F9"
          ],
          "tela": null
        }
      ]
    },
    {
      "numero": 5,
      "nome": "Encerramento",
      "inicio": 74.58,
      "fim": 78.93,
      "duracao": 4.35,
      "frases": [
        {
          "inicio": 74.58,
          "fim": 77.43,
          "marcacao": "BORDÃO",
          "fontes": [],
          "tela": null
        }
      ]
    }
  ]
};
window.TEMPOS.bloco = function (n) {
  const b = this.blocos[n - 1];
  const local = (x) => Math.round((x - b.inicio) * 1000) / 1000;
  return {
    numero: b.numero,
    nome: b.nome,
    inicioAbsoluto: b.inicio,
    duracao: b.duracao,
    frases: b.frases.map((f) => ({ ...f, inicio: local(f.inicio), fim: local(f.fim) })),
  };
};
