import unittest
import networkx as nx
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\src\\louvain_enchanced')))

from comm_dec import (
    get_partition_at_level,
    calculate_modularity,
    find_best_partition,
    create_dendrogram,
    create_induced_graph,
    load_binary_graph,
)

class TestLouvainEnhanced(unittest.TestCase):

    def setUp(self):
        self.graph = nx.karate_club_graph()

    def test_find_best_partition(self):
        partition = find_best_partition(self.graph)
        self.assertIsInstance(partition, dict)
        self.assertGreater(len(partition), 0)

    def test_calculate_modularity(self):
        partition = find_best_partition(self.graph)
        modularity = calculate_modularity(partition, self.graph)
        self.assertIsInstance(modularity, float)
        self.assertGreaterEqual(modularity, -1.0)
        self.assertLessEqual(modularity, 1.0)

    def test_create_dendrogram(self):
        dendrogram = create_dendrogram(self.graph)
        self.assertIsInstance(dendrogram, list)
        self.assertGreater(len(dendrogram), 0)

    def test_get_partition_at_level(self):
        dendrogram = create_dendrogram(self.graph)
        partition = get_partition_at_level(dendrogram, 1)
        self.assertIsInstance(partition, dict)
        self.assertGreater(len(partition), 0)

    def test_create_induced_graph(self):
        partition = find_best_partition(self.graph)
        induced_graph = create_induced_graph(partition, self.graph)
        self.assertIsInstance(induced_graph, nx.Graph)
        self.assertGreater(len(induced_graph.nodes), 0)

    def test_load_binary_graph(self):
        # binary_graph = load_binary_graph("path_to_binary_file")
        # self.assertIsInstance(binary_graph, nx.Graph)
        pass

if __name__ == '__main__':
    unittest.main()