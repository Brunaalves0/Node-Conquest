# Node Conquest
Node Conquest é um jogo de estratégia por turnos desenvolvido em Python utilizando a biblioteca Pygame. O objetivo principal é expandir seu território em um mapa de grade hexagonal, capturando nós e isolando áreas para dominar o tabuleiro.

---

## 🚀 Funcionalidades Atuais
Mapa Hexagonal Dinâmico: Geração de grade baseada em grafos com pesos de movimentação variados (custo de 1 a 3).

### Sistema de Câmera Automática:
O renderizador calcula as dimensões do mapa e centraliza a visualização automaticamente na tela.

### Algoritmo A (A-Star):
Implementação de busca de caminho inteligente para movimentação dos jogadores e das IAs.

### Gestão de Território:
Sistema que detecta quando um nó é capturado e atualiza as cores e pontuações em tempo real.

### Inteligência Artificial:
Oponentes que tomam decisões e se movimentam automaticamente durante seus turnos.

### Interface de Usuário (UI):
Menu principal, tutorial integrado, cards de status dos jogadores e botão de encerrar turno.

### Condição de Vitória:
O jogo detecta automaticamente quando todos os nós foram dominados, declarando o vencedor com base na pontuação.

---

## 🎮 Como Jogar

### Objetivo: Conquiste o máximo de nós possível. O jogo termina quando não restarem nós neutros no mapa.

### Movimentação:

- Cada jogador possui 3 pontos de movimento por turno.

- Nós neutros ou inimigos possuem um custo (exibido no centro do hexágono).

- Mover-se através do seu próprio território não consome pontos (desde que você ainda tenha se movimentado).

- Se você isolar uma área que não foi capturada, todo aquele território se torna seu.

### Controles:

- Clique Esquerdo: Seleciona o destino para o jogador.

- Botão "Encerrar Turno": Passa a vez para o próximo ator (Player ou IA).

- ESC: Retorna ao menu principal.

- S: Salvar o jogo atual.

---

## 🛠️ Estrutura do Projeto

```
Node-Conquest/
├── docs/
│   ├── E1_NodeConquest_Visao.md
│   ├── E2_NodeConquest_Design.md
│   └── E3_NodeConquest_Nucleo.md
├── src/
│   ├── algorithms/
│   │   ├── a_star.py         # Implementação do algoritmo A* 
│   │   └── territory.py      # Implementação do algoritmo de captura de área isolada
│   ├── core/
│   │   ├── data_manager.py   # Leitura/Escrita de JSON
│   │   └── graph.py          # Representação por matriz 2D
│   ├── entities/
│   │   ├── node.py           # Vértices
│   │   └── player.py         # Objeto do jogador/IAs
│   ├── maps/
│   ├── ui/
│   │   └── renderer.py       # Renderização Pygame 
│   └── main.py
├── LICENSE
├── README.md
└── requirements.txt          # Dependência: Pygame
```

---

### 📋 Pré-requisitos

Python 3.x

Pygame 2.5.0>

---

### ⚙️ Como Rodar o Jogo

Use o seguintes comandos:

1. Clone o repositório:

```
git clone https://github.com/Luis-Hardt/Node-Conquest.git
```

2. Instale as dependências:

```
pip install requirements.txt
```

3. Inicialise main.py:

```
cd src
python main.py
```
