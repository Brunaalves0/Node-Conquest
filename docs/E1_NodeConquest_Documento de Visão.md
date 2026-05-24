# E1 — Proposta e Definição do Projeto

> **Disciplina:** Teoria dos Grafos  
> **Prazo:** 25 de março de 2026  
> **Peso:** 10% da nota final  

---

## Identificação do Grupo

| Grupo: Node Conquest | |
|-------|---------------|
| Bruna Alves de Jesus | 40420418 |
| Luis Fernando Barcelos Hardt | 38774631 |
| Miguel da Silva Pereira | 41005422 |
| Domínio de aplicação | Jogos |

---

## 1. Contexto e Motivação

Em jogos de estratégia em turnos, o cálculo de rotas para dezenas ou centenas de unidades pode levar ao alto custo computacional, resultando em quedas de FPS ou demora na resposta da IA. O desafio específico em jogos com grades hexagonais também está na definição de distância entre as células com 6 vizinhos, que exigem maior precisão para evitar caminhos 'quebrados' que prejudicam a imersão do jogador.
Franquias como Sid Meier's Civilization e Age of Wonders são voltadas não somente à ideia de construção e manutenção de cidades, mas também a aspectos de exploração e combate. Essas funcionalidades exigem lidar constantemente com o pathfinding de diversas unidades, o que pode se tornar um gargalo para computadores com componentes menos eficientes caso haja falta de otimização.
O trabalho pretende explorar e demonstrar como a estrutura de dados e algoritmos de otimização de busca impactam nestas questões. O uso do algoritmo A* permite que o agente não apenas encontre o caminho, mas faça de forma que pareça natural, evitando desvios desnecessários e respeitando a experiência do jogador.

---

## 2. Objetivo Geral

O sistema deve simular a movimentação de agentes em um mapa hexagonal 2D, utilizando o algoritmo A* para calcular e visualizar rotas otimizadas com base em custos de movimento e obstáculos.

---

## 3. Objetivos Específicos

- [Modelar a grade hexagonal como um grafo ponderado, onde cada célula possui um peso fixo de 1 a 3 que representa o custo de movimento.]
- [Implementar funcionalidades de persistência de dados, permitindo salvar e carregar o estado atual do mapa e a posição das unidades.]
- [Desenvolver o algoritmo A* para coordenadas hexagonais, permitindo a busca de caminho entre pontos selecionado pelo usuário e as IAs.]
- [Projetar uma interface de visualização de dados, que apresente o caminho calculado e o custo total acumulado da rota, permitindo a comparação visual entre diferentes caminhos no grafo.]

---

## 4. Público-Alvo / Caso de Uso Principal

Um desenvolvedor de um jogo de estratégia em turnos que precisa implementar um sistema de busca de caminho que considere diferentes custos de movimento.

---

## 5. Justificativa Técnica — Por que Grafos?

A utilização de grafos permite tratar o mapa hexagonal como um conjunto de vértices (cada célula da grade) e arestas (as conexões de vizinhança entre as células) de forma mais eficiente em questões de custo e algoritmo do que uma abordagem de busca em grade pura ou BFS (que ignoram a variação de custos/peso). O modelo irá usar de grafo não-direcional, pois as unidades poderão se mover de forma bidirecional entre as células, e ponderado, para permitir a representação do custo de movimento do terreno (como planícies, florestas, colinas e lagos). Como padrão de modelagem, o peso será atribuído ao vértice de destino (o custo para entrar na célula) e não à aresta em si. Para a representação interna, será utilizada uma matriz bidimensional, otimizando a busca de vizinhos durante a execução do A*.

---

## 6. Tipo de Grafo

| Característica | Escolha | Justificativa breve |
|----------------|---------|---------------------|
| Dirigido ou não-dirigido | Não-dirigido | Não é necessário impedir a navegação bidirecional |
| Ponderado ou não-ponderado | Ponderado | Peso permite comportamentos mais complexos |
| Conectado / bipartido / geral | Conectado | Conectado por decisão de projeto. Obstáculos são vértices removidas do grafo |
| Representação interna pretendida | lista de adjacência / matriz | Matriz | Simples implementação e busca eficiente O(1) |

---

## 7. Diagrama Conceitual

![Diagrama conceitual](./docs/E1_NodeConquest_DiagramaConceitual.jpg)

**Legenda:** Representação do mapa hexagonal. O caminho em vermelho ilustra a rota de menor custo calculada pelo algoritmo, desviando de obstáculos (células pretas) e priorizando terrenos com menor custo de movimento. As células possuem pesos que podem ser cumulativos dependendo do terreno: as de custo 1 representam planícies, as de custo 2 representam colinas ou florestas, e as de custo 3 representam lagos ou áreas onde colinas e florestas estão presentes simultâneamente.

---

*Teoria dos Grafos — Profa. Dra. Andréa Ono Sakai*
