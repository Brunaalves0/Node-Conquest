# E3 — MVP: Núcleo Funcional com Primeiras Telas

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 10 de maio de 2026  
> **Peso:** 25% da nota final  

---

## Identificação do Grupo

| Grupo: Node Conquest | |
|-------|----------|
| [Repositório GitHub](https://github.com/Luis-Hardt/Node-Conquest.git) | |
| Bruna Alves de Jesus | 40420418 |
| Luis Fernando Barcelos Hardt | 38774631 |
| Miguel da Silva Pereira | 41005422 |

---

## 1. Como Executar o MVP

**Pré-requisitos:**

```bash
Python 3.12 ou superior
Bibliotecas: pygame 2.6.0 ou superior
```

**Instalação:**

```bash
git clone https://github.com/Luis-Hardt/Node-Conquest
cd Node-Conquest-main
pip install -r requirements.txt
```

**Execução:**

```bash
python src/main.py
```

**Saída esperada:**

```
A janela gráfica do jogo (Pygame) deve iniciar, exibindo o Menu Principal.
```

---

## 2. Algoritmo Implementado

| Campo | Resposta |
|-------|----------|
| Nome do algoritmo | A* Estrela |
| Arquivo de implementação | src/algorithms/a_star.py |
| Complexidade de tempo | O(E logV) |
| Complexidade de espaço | O(V) |

**Trecho do código com comentário de Big-O:**

```python
import heapq
import itertools

class AStar:
    def __init__(self, graph):
        # Inicializa com o grafo que contém a matriz de nós
        self.graph = graph

    def _to_cube(self, node):
        """Converte coordenadas axiais para cúbicas para cálculo de distância hexagonal."""
        q = node.grid_x - (node.grid_y - (node.grid_y % 2)) // 2
        r = node.grid_y
        s = -q - r
        return q, r, s

    def heuristic(self, a, b):
        """Heurística de distância em grade hexagonal (Manhattan em cubos)."""
        aq, ar, as_ = self._to_cube(a)
        bq, br, bs = self._to_cube(b)
        return max(abs(aq - bq), abs(ar - br), abs(as_ - bs))

    def get_path(self, start_node, goal_node, actor):
        """Calcula o menor caminho considerando os pesos dos vértices (1-3)."""
        frontier = []
        counter = itertools.count() # Garante desempate estável no heap
        
        # Inicia a fila de prioridade: (prioridade, contador, nó)
        heapq.heappush(frontier, (0, next(counter), start_node))
        
        came_from = {start_node: None}
        cost_so_far = {start_node: 0}
        
        while frontier:
            # Pega o nó com menor custo acumulado + heurística
            current = heapq.heappop(frontier)[2]
            
            if current == goal_node:
                break
            
            # Explora vizinhos disponíveis no grafo
            for next_node in self.graph.get_neighbors(current, actor):
                # O custo é a soma do custo anterior com o peso do nó de destino (1, 2 ou 3)
                new_cost = cost_so_far[current] + next_node.move_cost
                
                # Se for um caminho mais barato ou primeira vez visitando o nó
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    # f(n) = g(n) + h(n)
                    priority = new_cost + self.heuristic(goal_node, next_node)
                    heapq.heappush(frontier, (priority, next(counter), next_node))
                    came_from[next_node] = current
                    
        return self._reconstruct_path(came_from, start_node, goal_node)

    def _reconstruct_path(self, came_from, start, goal):
        """Backtracking para montar a lista de nós do destino até a origem."""
        if goal not in came_from:
            return []
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse() # Inverte para ter a ordem correta (início -> fim)
        return path
```

---

## 3. Estrutura do Repositório

```
node-conquest-terrarium/
├── docs/
│   ├── E1_NodeConquest_Visao.md
│   ├── E2_NodeConquest_Design.md
│   ├── E3_NodeConquest_Visao.md
├── src/
│   ├── core/
|   │   ├── data_manager.py   # Leitura/Escrita de JSON
│   │   ├── graph.py          # Representação por matriz 2D
│   │   ├── node.py           # Vértices
│   │   ├── player.py         # Jogador e IAs
│   │   └── territory.py      # Algoritmo de captura automática de regiões
│   ├── algorithms/
│   │   └── a_star.py         # Implementação do algoritmo A* 
│   ├── ui/
│   │   └── renderer.py       # Renderização Pygame 
│   └── main.py
├── data/
│   └── maps/                 # Arquivos de mapas
├── LICENSE                   
├── README.md                 
└── requirements.txt          # Dependência: Pygame
```

---

## 4. Telas do MVP

### Tela de Entrada

![Tela de Entrada](./docs/E3_mvp_inicial.png)

*Descrição: Tela inicial, contendo botões para iniciar um novo jogo, carregar último salvo e ver tutorial de como se joga.*

### Tela de Resultado

![Tela de Resultado](./docs/E3_mvp_resultado.png)

*Descrição: Tela principal do jogo, contendo o jogador e as 3 IAs inimigas no mapa.*

---

## 5. Testes Unitários

Para rodar os testes unitários do algoritmo principal localizados na pasta de testes dedicada, execute o seguinte comando a partir da raiz do projeto:

```bash
python src/test/test_a_star.py
```

---

## 6. Histórico de Commits

| Hash (7 chars) | Mensagem | Autor |
|----------------|----------|-------|
| `25cd307` | feat: scripts iniciais e documento e3_template | Luis Hardt |
| `f3c40bb` | feat: scripts principais e funcionamento basico | Luis Hardt |
| `eaeee75` | fix: readme | Luis Hardt |
| `6a5e2a9` | feat: carregamento e fixes | Luis Hardt |
| `15f9f81` | feat: camera móvel + zoom, tamanhos de mapa | Luis Hardt |

---

## 7. O que está funcionando / O que ainda falta

| Funcionalidade | Status | Observação |
|---------------|--------|------------|
| Classe do grafo | ✅ Completo | Mapeamento de nós fixos e adjacências |
| Algoritmo principal | ✅ Completo | Implementado com heurística de grade cúbica |
| Leitura de arquivo | ✅ Completo | Leitura/Escrita de estados via JSON |
| Geração prodecural | ✅ Completo | Criação aleatória da grade com pesos 1 a 3 |
| Testes unitários | ✅ Completo | Implementados via biblioteca `unittest` cobrindo 3 casos base do A* |

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
