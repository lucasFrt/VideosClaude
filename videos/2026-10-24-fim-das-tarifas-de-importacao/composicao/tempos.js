// Gerado pelo scripts/montar.py a partir do palavras.json. Não edite.
// TEMPOS.bloco(n) devolve os tempos do bloco n com as frases em tempo local (0 = começo do bloco),
// que é o tempo da timeline da cena. Para o hf-seek, que traz o tempo do vídeo inteiro, use
// inicioAbsoluto (palco.aoBuscar já faz isso).
window.TEMPOS = {
  "duracao": 81.23,
  "estimado": false,
  "blocos": [
    {
      "numero": 1,
      "nome": "Gancho",
      "inicio": 0.0,
      "fim": 7.92,
      "duracao": 7.92,
      "frases": [
        {
          "inicio": 0.1,
          "fim": 2.87,
          "marcacao": "FATO",
          "fontes": [
            "F1"
          ],
          "tela": "12% (média)"
        },
        {
          "inicio": 3.65,
          "fim": 7.14,
          "marcacao": "BORDÃO",
          "fontes": [],
          "tela": null
        }
      ]
    },
    {
      "numero": 2,
      "nome": "Contexto",
      "inicio": 7.92,
      "fim": 23.61,
      "duracao": 15.69,
      "frases": [
        {
          "inicio": 7.92,
          "fim": 13.14,
          "marcacao": "FATO",
          "fontes": [
            "F2",
            "F3"
          ],
          "tela": "R$ 90 bi por ano"
        },
        {
          "inicio": 13.92,
          "fim": 17.82,
          "marcacao": "FATO",
          "fontes": [
            "F7"
          ],
          "tela": null
        },
        {
          "inicio": 18.6,
          "fim": 22.83,
          "marcacao": "PREMISSA",
          "fontes": [],
          "tela": null
        }
      ]
    },
    {
      "numero": 3,
      "nome": "O que mudaria",
      "inicio": 23.61,
      "fim": 45.65,
      "duracao": 22.04,
      "frases": [
        {
          "inicio": 23.61,
          "fim": 32.23,
          "marcacao": "PROJEÇÃO",
          "fontes": [
            "F4"
          ],
          "tela": null
        },
        {
          "inicio": 33.01,
          "fim": 37.94,
          "marcacao": "PROJEÇÃO",
          "fontes": [
            "F3"
          ],
          "tela": null
        },
        {
          "inicio": 38.73,
          "fim": 44.86,
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
      "inicio": 45.65,
      "fim": 75.95,
      "duracao": 30.3,
      "frases": [
        {
          "inicio": 45.65,
          "fim": 47.78,
          "marcacao": "BORDÃO",
          "fontes": [],
          "tela": null
        },
        {
          "inicio": 48.57,
          "fim": 55.76,
          "marcacao": "ARGUMENTO A FAVOR",
          "fontes": [
            "F10",
            "F9"
          ],
          "tela": null
        },
        {
          "inicio": 56.55,
          "fim": 64.78,
          "marcacao": "ARGUMENTO CONTRA",
          "fontes": [
            "F5"
          ],
          "tela": null
        },
        {
          "inicio": 65.57,
          "fim": 75.17,
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
      "inicio": 75.95,
      "fim": 81.23,
      "duracao": 5.28,
      "frases": [
        {
          "inicio": 75.95,
          "fim": 79.73,
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
