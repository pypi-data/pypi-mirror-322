# coding: utf-8

from typing import Dict, Optional
import networkx as nx

class Status:
    def __init__(self) -> None:
        self.node_to_community: Dict[int, int] = {}
        self.total_edge_weight: float = 0
        self.community_degrees: Dict[int, float] = {}
        self.node_degrees: Dict[int, float] = {}
        self.internal_edges: Dict[int, float] = {}
        self.self_loops: Dict[int, float] = {}

    def __str__(self) -> str:
        return (f"node_to_community: {self.node_to_community}, community_degrees: {self.community_degrees}, "
                f"internal_edges: {self.internal_edges}, total_edge_weight: {self.total_edge_weight}")

    def copy(self) -> 'Status':
        """Perform a deep copy of status"""
        new_status = Status()
        new_status.node_to_community = self.node_to_community.copy()
        new_status.internal_edges = self.internal_edges.copy()
        new_status.community_degrees = self.community_degrees.copy()
        new_status.node_degrees = self.node_degrees.copy()
        new_status.total_edge_weight = self.total_edge_weight
        new_status.self_loops = self.self_loops.copy()
        return new_status

    def init(self, graph: nx.Graph, weight: str, partition: Optional[Dict[int, int]] = None) -> None:
        """Initialize the status of a graph with every node in one community

        Parameters
        ----------
        graph : networkx.Graph
            The networkx graph which will be decomposed.
        weight : str
            The key in graph to use as weight.
        partition : dict, optional
            The partition of the nodes, i.e., a dictionary where keys are their nodes and values the communities.
        """
        community_id = 0
        self.node_to_community = {}
        self.total_edge_weight = 0
        self.community_degrees = {}
        self.node_degrees = {}
        self.internal_edges = {}
        self.self_loops = {}

        for node in graph.nodes():
            self.node_to_community[node] = community_id
            node_degree = float(graph.degree(node, weight=weight))
            if partition is None:
                self.community_degrees[community_id] = node_degree
                self.node_degrees[node] = node_degree
                self.internal_edges[community_id] = float(graph.get_edge_data(node, node, default={weight: 0}).get(weight, 0))
            else:
                community = partition[node]
                self.node_to_community[node] = community
                self.community_degrees[community] = self.community_degrees.get(community, 0) + node_degree
                self.node_degrees[node] = node_degree
                self.internal_edges[community] = self.internal_edges.get(community, 0) + float(graph.get_edge_data(node, node, default={weight: 0}).get(weight, 0))
            self.total_edge_weight += node_degree
            community_id += 1
        self.total_edge_weight /= 2