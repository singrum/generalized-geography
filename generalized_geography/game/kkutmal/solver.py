### Changeable Directed Edge Geography ###
# data structure : UnlabeledMultiDiGraph that have nodes = V x {0,1} for some V and edges such that e[0][1] != e[1][1]
#                  노드는 (v,0) 또는 (v,1) 튜플로 나타내어짐
#                  엣지는 (u,0)->(v,1) 또는 (u,1)->(v,0) 꼴
# position : (G, (v, 0))

from collections import deque
from copy import copy, deepcopy
from typing import NamedTuple, Deque, Tuple
from networkx import DiGraph, condensation, descendants, strongly_connected_components
from sympy import false, true
import generalized_geography as gg


class BipartiteNode(NamedTuple):
    value: any
    index: int


def fastly_classify(graph, verbose=1):
    node_type1 = classify_reusable_winlose(graph, verbose=verbose)
    remove_2_cycles(graph, verbose=verbose)
    node_type2 = classify_loop_winlose(graph, verbose=verbose)
    return {**node_type1, **node_type2}


def get_unique_out_edges(graph: gg.UnlabeledMultiDiGraph):
    nodes = [node for node, deg in graph.out_degree() if node.index ==
             0 and deg == 1]
    edges = [list(graph.out_edges(node))[0] for node in nodes]
    return edges


def remove_2_cycles(graph: gg.UnlabeledMultiDiGraph, unique_out_edges=None, verbose=1):

    if verbose == 1:
        print("Remove 2 cycles : ", end="")

    if unique_out_edges == None:
        unique_out_edges = get_unique_out_edges(graph)

    to_remove = []

    # self loop 짝수 개 검출
    for edge in unique_out_edges:
        m = graph.get_multiplicity(edge[1], edge[0])
        if m >= 2:
            graph.remove_edge(edge[1], edge[0], m - m % 2)
            to_remove.append((edge[1], edge[0], m - m % 2))

    # 2-cycle 검출
    for edge1 in unique_out_edges:
        for edge2 in unique_out_edges:
            if edge1 >= edge2:
                continue
            if graph.has_edge(edge1[1], edge2[0]) and graph.has_edge(edge2[1], edge1[0]):
                delete_num = min(
                    graph.get_multiplicity(edge1[1], edge2[0]),
                    graph.get_multiplicity(edge2[1], edge1[0])
                )
                graph.remove_edges_from(
                    [(edge1[1], edge2[0], delete_num), (edge2[1], edge1[0], delete_num)])
                to_remove.append((edge1[1], edge2[0], delete_num))
                to_remove.append((edge2[1], edge1[0], delete_num))

    if verbose == 1:
        print(sum([m for _, _, m in to_remove]), "edges removed")


def classify_loop_winlose(graph: gg.UnlabeledMultiDiGraph, unique_out_edges=None, verbose=1, lose_sinks=None, win_sinks=None):
    if verbose == 1:
        print("Classify loop winlose : ", end="")

    if unique_out_edges == None:
        unique_out_edges = get_unique_out_edges(graph)

    node_type = {}
    loops = DiGraph()
    loops.add_edges_from(
        [(v, u) for u, v in unique_out_edges if graph.has_edge(v, u)])

    if not lose_sinks:
        lose_sinks = [node for node, deg in graph.out_degree()
                      if node.index == 1 and deg == 0]
    if not win_sinks:
        win_sinks = [node for node, deg in graph.out_degree(
        ) if node.index == 1 and deg == 1 and loops.has_edge(*list(graph.out_edges(node))[0])]

    for n in lose_sinks:
        node_type[n] = "L"
    for n in win_sinks:
        node_type[n] = "W"

    q: Deque[BipartiteNode] = deque(win_sinks + lose_sinks)

    while q:
        node = q.popleft()

        preds = [pred for pred in graph.predecessors(
            node) if pred not in node_type]
        graph.remove_node(node)

        if node.index == 0:
            if node_type[node] == "L":
                for pred in preds:
                    node_type[pred] = "W"
                    q.append(pred)

            else:
                for pred in preds:
                    if graph.out_degree(pred) == 0:
                        node_type[pred] = "L"
                        q.append(pred)

                    elif graph.out_degree(pred) == 1 and loops.has_edge(*list(graph.out_edges(pred))[0]):
                        node_type[pred] = "W"
                        q.append(pred)
        else:
            if node_type[node] == "L":
                for pred in preds:
                    if graph.out_degree(pred) == 0:
                        node_type[pred] = "L"
                        q.append(pred)

            else:
                for pred in preds:
                    node_type[pred] = "W"
                    q.append(pred)

    if verbose == 1:
        win_nodes = [node for node in node_type if node_type[node] == "W"]
        lose_nodes = [node for node in node_type if node_type[node] == "L"]
        print(len(win_nodes), "win,", len(lose_nodes),
              "lose,", len(graph), "remain")

    return node_type


def classify_reusable_winlose(graph: gg.UnlabeledMultiDiGraph, verbose=1):
    if verbose == 1:
        print("Classify loop winlose : ", end="")
    node_type = {}
    sinks = [node for node, deg in graph.out_degree() if deg == 0]

    q: Deque[BipartiteNode] = deque()

    for sink in sinks:
        node_type[sink] = "L"
        q.append(sink)

    while q:
        node = q.popleft()
        preds = [pred for pred in graph.predecessors(node)
                 if pred not in node_type]
        graph.remove_node(node)
        if node.index == 0:
            if node_type[node] == "L":
                for pred in preds:
                    node_type[pred] = "W"
                    q.append(pred)

            else:
                for pred in preds:
                    if graph.out_degree(pred) == 0:
                        node_type[pred] = "L"
                        q.append(pred)

        else:
            if node_type[node] == "L":
                for pred in preds:
                    if graph.out_degree(pred) == 0:
                        node_type[pred] = "L"
                        q.append(pred)

            else:
                for pred in preds:
                    node_type[pred] = "W"
                    q.append(pred)

    if verbose == 1:
        win_nodes = [node for node in node_type if node_type[node] == "W"]
        lose_nodes = [node for node in node_type if node_type[node] == "L"]
        print(len(win_nodes), "win,", len(lose_nodes),
              "lose,", len(graph), "remain")

    return node_type


def reachable_graph(graph: gg.UnlabeledMultiDiGraph, node: any) -> gg.UnlabeledMultiDiGraph:
    if type(node) != BipartiteNode:
        node = BipartiteNode(node, 0)
    reachable_nodes = descendants(graph, node) | {node}
    subgraph = graph.subgraph(reachable_nodes).copy()
    return subgraph


def is_win_dfs(graph: gg.UnlabeledMultiDiGraph, node: any, trail=None, sort_key=None):
    if trail == None:
        trail = []

    if type(node) != BipartiteNode:
        node = BipartiteNode(node, 0)

    graph_copy = reachable_graph(graph, node)
    node_type = fastly_classify(graph_copy, verbose=0)

    # Ending State
    if node in node_type:
        if node_type[node] == "W":
            return true
        else:
            return false

    edges = moves(graph_copy, node)
    edges.sort(key=lambda x: len(
        moves(graph_copy, x[-1])) if sort_key == None else sort_key)

    for edge in edges:

        graph_copy.remove_edge(*edge, 1)
        if not is_win_dfs(graph_copy, edge[-1], [*trail, edge]):
            return True
        graph_copy.add_edge(*edge, 1)

    return False


def moves(graph: gg.UnlabeledMultiDiGraph, node: any):
    if type(node) != BipartiteNode:
        node = BipartiteNode(node, 0)

    return [(succ0, succ1)
            for succ0 in graph.successors(node)
            for succ1 in graph.successors(succ0)]


def get_major_graph(graph: gg.UnlabeledMultiDiGraph) -> gg.UnlabeledMultiDiGraph:
    scc_list = list(strongly_connected_components(graph))
    scc_graph = condensation(graph, scc_list)
    leaf_scc_indices = {
        n for n in scc_graph if scc_graph.out_degree(n) == 0}
    leaf_sccs = [scc_list[i] for i in leaf_scc_indices]

    if len(leaf_sccs) != 1:
        raise Exception("주요 루트 없음")

    return graph.subgraph(leaf_sccs[0]).copy()


class Encoder:
    def __init__(self, edges: list[Tuple[BipartiteNode, BipartiteNode]]):
        self.edges_map = edges
        self.index_map = {edge: i for i, edge in enumerate(edges)}

    def encode(self, index: int):
        return self.index_map[index]

    def decode(self, edge: Tuple[BipartiteNode, BipartiteNode]):
        return self.edges_map[edge]


class Game:
    def __init__(self, graph: gg.UnlabeledMultiDiGraph):
        self.original_graph = graph
        self.node_type = fastly_classify(graph)

        self.major_graph = get_major_graph(graph)
        self.encoder = Encoder(
            [e for e in self.major_graph.edges if e[0].index == 1])

        
