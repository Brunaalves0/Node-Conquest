import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.graph import Graph
from core.player import Player
from algorithms.a_star import AStar

class TestAStar(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(5, 5, 64, 64)
        for node in self.graph.nodes.values():
            node.weight = 1
        self.start_node = self.graph.get_node(0, 0)
        self.actor = Player("Test", self.start_node, (255, 255, 255))
        self.a_star = AStar(self.graph)

    def test_caso_base(self):
        goal_node = self.graph.get_node(2, 2)
        self.graph.get_node(1, 1).weight = 3
        path = self.a_star.get_path(self.start_node, goal_node, self.actor)
        self.assertTrue(len(path) > 0)
        self.assertEqual(path[-1], goal_node)

    def test_grafo_vazio_ou_nulo(self):
        empty_graph = Graph(0, 0, 64, 64)
        a_star_empty = AStar(empty_graph)
        path = a_star_empty.get_path(None, None, self.actor)
        self.assertEqual(path, [])

    def test_grafo_completo(self):
        goal_node = self.graph.get_node(4, 4)
        path = self.a_star.get_path(self.start_node, goal_node, self.actor)
        self.assertTrue(len(path) > 0)
        self.assertEqual(path[-1], goal_node)

if __name__ == '__main__':
    unittest.main()