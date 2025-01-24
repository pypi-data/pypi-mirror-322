# coding: utf-8

import array
import numbers
import warnings
from typing import Union, Dict, List, Optional
from __future__ import print_function

import networkx as nx
import numpy as np

from .community_status import Status

__author__ = """himangshu"""

__PASS_MAX = -1
__MIN = 0.0000001


def get_random_state(seed: Union[None, int, np.random.RandomState]) -> np.random.RandomState:
    """Convert seed into a np.random.RandomState instance.

    Parameters
    ----------
    seed : None | int | instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.

    Returns
    -------
    np.random.RandomState
        RandomState instance.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError(f"{seed} cannot be used to seed a numpy.random.RandomState instance")

def get_partition_at_level(dendrogram: List[Dict[int, int]], level: int) -> Dict[int, int]:
    """Return the partition of the nodes at the given level.

    Parameters
    ----------
    dendrogram : list of dict
        A list of partitions, i.e., dictionaries where keys of the i+1 are the values of the i.
    level : int
        The level which belongs to [0..len(dendrogram)-1].

    Returns
    -------
    partition : dict
        A dictionary where keys are the nodes and the values are the set it belongs to.
    """
    partition = dendrogram[0].copy()
    for idx in range(1, level + 1):
        for node, community in partition.items():
            partition[node] = dendrogram[idx][community]
    return partition

def calculate_modularity(partition: Dict[int, int], graph: nx.Graph, weight: str = 'weight') -> float:
    """Compute the modularity of a partition of a graph.

    Parameters
    ----------
    partition : dict
        The partition of the nodes, i.e., a dictionary where keys are their nodes and values the communities.
    graph : networkx.Graph
        The networkx graph which is decomposed.
    weight : str, optional
        The key in graph to use as weight. Default to 'weight'.

    Returns
    -------
    modularity : float
        The modularity.

    Raises
    ------
    KeyError
        If the partition is not a partition of all graph nodes.
    ValueError
        If the graph has no link.
    TypeError
        If graph is not a networkx.Graph.
    """
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    internal_weights = dict()
    degree_weights = dict()
    total_links = graph.size(weight=weight)
    if total_links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        community = partition[node]
        degree_weights[community] = degree_weights.get(community, 0.) + graph.degree(node, weight=weight)
        for neighbor, data in graph[node].items():
            edge_weight = data.get(weight, 1)
            if partition[neighbor] == community:
                if neighbor == node:
                    internal_weights[community] = internal_weights.get(community, 0.) + float(edge_weight)
                else:
                    internal_weights[community] = internal_weights.get(community, 0.) + float(edge_weight) / 2.

    modularity_score = 0.
    for community in set(partition.values()):
        modularity_score += (internal_weights.get(community, 0.) / total_links) - \
                            (degree_weights.get(community, 0.) / (2. * total_links)) ** 2
    return modularity_score

def find_best_partition(graph: nx.Graph,
                        initial_partition: Optional[Dict[int, int]] = None,
                        weight: str = 'weight',
                        resolution: float = 1.0,
                        randomize: Optional[bool] = None,
                        random_state: Optional[Union[int, np.random.RandomState]] = None) -> Dict[int, int]:
    """Compute the partition of the graph nodes which maximizes the modularity using the Louvain heuristics.

    Parameters
    ----------
    graph : networkx.Graph
        The networkx graph which is decomposed.
    initial_partition : dict, optional
        The algorithm will start using this partition of the nodes. It's a dictionary where keys are their nodes and values the communities.
    weight : str, optional
        The key in graph to use as weight. Default to 'weight'.
    resolution : float, optional
        Will change the size of the communities, default to 1.
    randomize : bool, optional
        Will randomize the node evaluation order and the community evaluation order to get different partitions at each call.
    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used by `np.random`.

    Returns
    -------
    partition : dict
        The partition, with communities numbered from 0 to number of communities.
    """
    dendrogram = create_dendrogram(graph,
                                   initial_partition,
                                   weight,
                                   resolution,
                                   randomize,
                                   random_state)
    return get_partition_at_level(dendrogram, len(dendrogram) - 1)

def create_dendrogram(graph: nx.Graph,
                      initial_partition: Optional[Dict[int, int]] = None,
                      weight: str = 'weight',
                      resolution: float = 1.0,
                      randomize: Optional[bool] = None,
                      random_state: Optional[Union[int, np.random.RandomState]] = None) -> List[Dict[int, int]]:
    """Find communities in the graph and return the associated dendrogram.

    Parameters
    ----------
    graph : networkx.Graph
        The networkx graph which will be decomposed.
    initial_partition : dict, optional
        The algorithm will start using this partition of the nodes. It's a dictionary where keys are their nodes and values the communities.
    weight : str, optional
        The key in graph to use as weight. Default to 'weight'.
    resolution : float, optional
        Will change the size of the communities, default to 1.
    randomize : bool, optional
        Will randomize the node evaluation order and the community evaluation order to get different partitions at each call.
    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used by `np.random`.

    Returns
    -------
    dendrogram : list of dict
        A list of partitions, i.e., dictionaries where keys of the i+1 are the values of the i.
    """
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    if randomize is not None:
        warnings.warn("The `randomize` parameter will be deprecated in future versions. Use `random_state` instead.", DeprecationWarning)
        if randomize is False:
            random_state = 0

    if randomize and random_state is not None:
        raise ValueError("`randomize` and `random_state` cannot be used at the same time")

    random_state = get_random_state(random_state)

    if graph.number_of_edges() == 0:
        partition = {node: i for i, node in enumerate(graph.nodes())}
        return [partition]

    current_graph = graph.copy()
    status = Status()
    status.init(current_graph, weight, initial_partition)
    status_list = []
    __one_level(current_graph, status, weight, resolution, random_state)
    new_modularity = __modularity(status, resolution)
    partition = __renumber(status.node2com)
    status_list.append(partition)
    modularity = new_modularity
    current_graph = create_induced_graph(partition, current_graph, weight)
    status.init(current_graph, weight)

    while True:
        __one_level(current_graph, status, weight, resolution, random_state)
        new_modularity = __modularity(status, resolution)
        if new_modularity - modularity < __MIN:
            break
        partition = __renumber(status.node2com)
        status_list.append(partition)
        modularity = new_modularity
        current_graph = create_induced_graph(partition, current_graph, weight)
        status.init(current_graph, weight)
    return status_list[:]

def create_induced_graph(partition: Dict[int, int], graph: nx.Graph, weight: str = "weight") -> nx.Graph:
    """Produce the graph where nodes are the communities.

    Parameters
    ----------
    partition : dict
        A dictionary where keys are graph nodes and values the part the node belongs to.
    graph : networkx.Graph
        The initial graph.
    weight : str, optional
        The key in graph to use as weight. Default to 'weight'.

    Returns
    -------
    induced_graph : networkx.Graph
        A networkx graph where nodes are the parts.
    """
    induced_graph = nx.Graph()
    induced_graph.add_nodes_from(partition.values())

    for node1, node2, data in graph.edges(data=True):
        edge_weight = data.get(weight, 1)
        community1 = partition[node1]
        community2 = partition[node2]
        previous_weight = induced_graph.get_edge_data(community1, community2, {weight: 0}).get(weight, 1)
        induced_graph.add_edge(community1, community2, **{weight: previous_weight + edge_weight})

    return induced_graph

def __renumber(dictionary: Dict[int, int]) -> Dict[int, int]:
    """Renumber the values of the dictionary from 0 to n."""
    values = set(dictionary.values())
    target = set(range(len(values)))

    if values == target:
        return dictionary.copy()

    renumbering = {v: i for i, v in enumerate(values)}
    return {k: renumbering[v] for k, v in dictionary.items()}

def load_binary_graph(data: str) -> nx.Graph:
    """Load binary graph as used by the cpp implementation of this algorithm."""
    with open(data, "rb") as file:
        reader = array.array("I")
        reader.fromfile(file, 1)
        num_nodes = reader.pop()
        reader = array.array("I")
        reader.fromfile(file, num_nodes)
        cumulative_degrees = reader.tolist()
        num_links = reader.pop()
        reader = array.array("I")
        reader.fromfile(file, num_links)
        links = reader.tolist()

    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    previous_degree = 0

    for index in range(num_nodes):
        last_degree = cumulative_degrees[index]
        neighbors = links[previous_degree:last_degree]
        graph.add_edges_from([(index, int(neighbor)) for neighbor in neighbors])
        previous_degree = last_degree

    return graph


def __one_level(graph, status, weight_key, resolution, random_state):
    """Compute one level of communities"""
    modified = True
    nb_pass_done = 0
    cur_mod = __modularity(status, resolution)
    new_mod = cur_mod

    while modified and nb_pass_done != __PASS_MAX:
        cur_mod = new_mod
        modified = False
        nb_pass_done += 1

        for node in __randomize(graph.nodes(), random_state):
            com_node = status.node_to_community[node]
            degc_totw = status.node_degrees.get(node, 0.) / (status.total_edge_weight * 2.)  # NOQA
            neigh_communities = __neighcom(node, graph, status, weight_key)
            remove_cost = - neigh_communities.get(com_node, 0) + \
                resolution * (status.community_degrees.get(com_node, 0.) - status.node_degrees.get(node, 0.)) * degc_totw
            __remove(node, com_node,
                     neigh_communities.get(com_node, 0.), status)
            best_com = com_node
            best_increase = 0
            for com, dnc in __randomize(neigh_communities.items(), random_state):
                incr = remove_cost + dnc - \
                       resolution * status.community_degrees.get(com, 0.) * degc_totw
                if incr > best_increase:
                    best_increase = incr
                    best_com = com
            __insert(node, best_com,
                     neigh_communities.get(best_com, 0.), status)
            if best_com != com_node:
                modified = True
        new_mod = __modularity(status, resolution)
        if new_mod - cur_mod < __MIN:
            break


def __neighcom(node, graph, status, weight_key):
    """
    Compute the communities in the neighborhood of node in the graph given
    with the decomposition node_to_community
    """
    weights = {}
    for neighbor, datas in graph[node].items():
        if neighbor != node:
            edge_weight = datas.get(weight_key, 1)
            neighbor_community = status.node_to_community[neighbor]
            weights[neighbor_community] = weights.get(neighbor_community, 0) + edge_weight

    return weights


def __remove(node, community, weight, status):
    """ Remove node from community and modify status"""
    status.community_degrees[community] = (status.community_degrees.get(community, 0.)
                                           - status.node_degrees.get(node, 0.))
    status.internal_edges[community] = float(status.internal_edges.get(community, 0.) -
                                             weight - status.self_loops.get(node, 0.))
    status.node_to_community[node] = -1


def __insert(node, community, weight, status):
    """ Insert node into community and modify status"""
    status.node_to_community[node] = community
    status.community_degrees[community] = (status.community_degrees.get(community, 0.) +
                                           status.node_degrees.get(node, 0.))
    status.internal_edges[community] = float(status.internal_edges.get(community, 0.) +
                                             weight + status.self_loops.get(node, 0.))


def __modularity(status, resolution):
    """
    Fast compute the modularity of the partition of the graph using
    status precomputed
    """
    links = float(status.total_edge_weight)
    result = 0.
    for community in set(status.node_to_community.values()):
        in_degree = status.internal_edges.get(community, 0.)
        degree = status.community_degrees.get(community, 0.)
        if links > 0:
            result += in_degree * resolution / links -  ((degree / (2. * links)) ** 2)
    return result


def __randomize(items, random_state):
    """Returns a List containing a random permutation of items"""
    randomized_items = list(items)
    random_state.shuffle(randomized_items)
    return randomized_items