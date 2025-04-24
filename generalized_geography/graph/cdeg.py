### Changeable Directed Edge Geography ###
# data structure : UnlabeledMultiDiGraph that have nodes = V x {0,1} for some V and edges such that e[0][1] != e[1][1]
#                  노드는 (v,0) 또는 (v,1) 튜플로 나타내어짐
#                  엣지는 (u,0)->(v,1) 또는 (u,1)->(v,0) 꼴
# position : (G, (v, 0))

from collections import deque
from copy import copy, deepcopy
from typing import Any, Dict, List, NamedTuple, Deque, NewType, Tuple
from networkx import DiGraph, condensation, descendants, path_graph, strongly_connected_components
from sympy import false, true

from generalized_geography.common.constants import LOS, WIN
from generalized_geography.common.unlabeled_multidigraph import UnlabeledMultiDiGraph


class BipartiteNode(NamedTuple):
    value: any
    index: int

    def __str__(self):
        return f"{self.value}{self.index}"

    def __repr__(self):
        return f"{self.value}{self.index}"


BipartiteEdge = NewType("BipartiteEdge", Tuple[BipartiteNode, BipartiteNode])


class CDEG:
    node_type: Dict[Any, int]
    graph: UnlabeledMultiDiGraph
    path_graph: DiGraph
    two_cycles: UnlabeledMultiDiGraph
    loops = DiGraph
    removed_edges: UnlabeledMultiDiGraph

    def __init__(self, graph: UnlabeledMultiDiGraph):
        self.node_type = {}
        self.graph = graph
        self.path_graph = DiGraph()
        self.two_cycles = UnlabeledMultiDiGraph()
        self.loops = DiGraph()
        self.removed_edges = UnlabeledMultiDiGraph()

    def fastly_classify(self, verbose=0):
        self.node_type.clear()
        self.path_graph.clear()
        self.two_cycles.clear()
        self.loops.clear()
        self.classify_reusable_winlose(verbose=verbose)
        self.remove_2_cycles(verbose=verbose)
        self.classify_loop_winlose(verbose=verbose)

    def classify_reusable_winlose(self, verbose=0):
        if verbose == 1:
            print("Classify loop winlose : ", end="")

        sinks = [node for node, deg in self.graph.out_degree() if deg == 0]

        q: Deque[BipartiteNode] = deque()

        for sink in sinks:
            self.node_type[sink] = LOS
            q.append(sink)

        while q:
            node = q.popleft()
            preds = [pred for pred in self.graph.predecessors(node)
                     if pred not in self.node_type]
            self.removed_edges.add_edges_from(
                list(self.graph.out_edges(node, data="multiplicity")) +
                list(self.graph.in_edges(node, data="multiplicity")))

            self.graph.remove_node(node)

            if node.index == 0:
                if self.node_type[node] == LOS:
                    for pred in preds:
                        self.path_graph.add_edge(pred, node)
                        self.node_type[pred] = WIN
                        q.append(pred)

                else:
                    for pred in preds:
                        if self.graph.out_degree(pred) == 0:
                            self.path_graph.add_edge(pred, node)
                            self.node_type[pred] = LOS
                            q.append(pred)

            else:
                if self.node_type[node] == LOS:
                    for pred in preds:
                        if self.graph.out_degree(pred) == 0:
                            self.path_graph.add_edge(pred, node)
                            self.node_type[pred] = LOS
                            q.append(pred)

                else:
                    for pred in preds:
                        self.path_graph.add_edge(pred, node)
                        self.node_type[pred] = WIN
                        q.append(pred)

        if verbose == 1:
            win_nodes = [
                node for node in self.node_type if self.node_type[node] == WIN]
            lose_nodes = [
                node for node in self.node_type if self.node_type[node] == LOS]
            print(len(win_nodes), "win,", len(lose_nodes),
                  "lose,", len(self.graph), "remain")

    def remove_2_cycles(self, unique_out_edges=None, verbose=0):

        if verbose == 1:
            print("Remove 2 cycles : ", end="")

        if unique_out_edges == None:
            unique_out_edges = get_unique_out_edges(self.graph)

        to_remove = []

        # self loop 짝수 개 검출
        for edge in unique_out_edges:
            m = self.graph.get_multiplicity(edge[1], edge[0])
            if m >= 2:
                self.removed_edges.add_edge(edge[1], edge[0], m - m % 2)
                self.graph.remove_edge(edge[1], edge[0], m - m % 2)

                to_remove.append((edge[1], edge[0], m - m % 2))

        # 2-cycle 검출
        for edge1 in unique_out_edges:
            for edge2 in unique_out_edges:
                if edge1 >= edge2:
                    continue
                if self.graph.has_edge(edge1[1], edge2[0]) and self.graph.has_edge(edge2[1], edge1[0]):
                    delete_num = min(
                        self.graph.get_multiplicity(edge1[1], edge2[0]),
                        self.graph.get_multiplicity(edge2[1], edge1[0])
                    )
                    self.removed_edges.add_edges_from(
                        [(edge1[1], edge2[0], delete_num), (edge2[1], edge1[0], delete_num)])
                    self.graph.remove_edges_from(
                        [(edge1[1], edge2[0], delete_num), (edge2[1], edge1[0], delete_num)])

                    to_remove.append((edge1[1], edge2[0], delete_num))
                    to_remove.append((edge2[1], edge1[0], delete_num))

        if verbose == 1:
            print(sum([m for _, _, m in to_remove]), "edges removed")

        self.two_cycles.add_edges_from(to_remove)

    def classify_loop_winlose(self, unique_out_edges=None, verbose=0, lose_sinks=None, win_sinks=None):
        if verbose == 1:
            print("Classify loop winlose : ", end="")

        if unique_out_edges == None:
            unique_out_edges = get_unique_out_edges(self.graph)

        self.loops.clear()
        self.loops.add_edges_from(
            [(v, u) for u, v in unique_out_edges if self.graph.has_edge(v, u)])

        if not lose_sinks:
            lose_sinks = [node for node, deg in self.graph.out_degree()
                          if node.index == 1 and deg == 0]
        if not win_sinks:
            win_sinks = [node for node, deg in self.graph.out_degree(
            ) if node.index == 1 and deg == 1 and self.loops.has_edge(*list(self.graph.out_edges(node))[0])]

        for n in lose_sinks:
            self.node_type[n] = LOS
        for n in win_sinks:
            self.path_graph.add_edge(n, list(self.graph.out_edges(n))[0])
            self.node_type[n] = WIN

        q: Deque[BipartiteNode] = deque(win_sinks + lose_sinks)

        while q:
            node = q.popleft()

            preds = [pred for pred in self.graph.predecessors(
                node) if pred not in self.node_type]
            self.removed_edges.add_edges_from(
                list(self.graph.out_edges(node, data="multiplicity")) +
                list(self.graph.in_edges(node, data="multiplicity")))
            self.graph.remove_node(node)

            if node.index == 0:
                if self.node_type[node] == LOS:
                    for pred in preds:
                        self.node_type[pred] = WIN
                        self.path_graph.add_edge(pred, node)
                        q.append(pred)

                else:
                    for pred in preds:
                        if self.graph.out_degree(pred) == 0:
                            self.node_type[pred] = LOS
                            self.path_graph.add_edge(pred, node)
                            q.append(pred)

                        elif self.graph.out_degree(pred) == 1 and self.loops.has_edge(*list(self.graph.out_edges(pred))[0]):
                            self.node_type[pred] = WIN
                            self.path_graph.add_edge(
                                pred, list(self.graph.out_edges(pred))[0])
                            self.path_graph.add_edge(pred, node)
                            q.append(pred)
            else:
                if self.node_type[node] == LOS:
                    for pred in preds:
                        if self.graph.out_degree(pred) == 0:
                            self.node_type[pred] = LOS
                            q.append(pred)

                else:
                    for pred in preds:
                        self.node_type[pred] = WIN
                        q.append(pred)

        if verbose == 1:
            win_nodes = [
                node for node in self.node_type if self.node_type[node] == WIN]
            lose_nodes = [
                node for node in self.node_type if self.node_type[node] == LOS]
            print(len(win_nodes), "win,", len(lose_nodes),
                  "lose,", len(self.graph), "remain")

    def copy(self):
        cdeg = CDEG(self.graph.copy())
        cdeg.node_type = self.node_type.copy()
        cdeg.path_graph = self.path_graph.copy()
        cdeg.two_cycles = self.two_cycles.copy()
        cdeg.loops = self.loops.copy()
        return cdeg

    def is_win(self, node: any, sort_key=None, win_callback=None, cnt_limit=None):

        def dfs(graph: UnlabeledMultiDiGraph, node: any, trail=None):
            nonlocal cnt_limit
            if cnt_limit != None and cnt_limit == 0:
                raise Exception("Exceed Limit")

            if trail == None:
                trail = []

            if type(node) != BipartiteNode:
                node = BipartiteNode(node, 0)

            graph_copy = reachable_graph(graph, node)

            cdeg = CDEG(graph_copy)
            cdeg.fastly_classify()
            node_type = cdeg.node_type

            if node in node_type:
                if node_type[node] == WIN:
                    return true
                else:
                    if win_callback:
                        win_callback(trail)
                    if cnt_limit:
                        cnt_limit -= 1
                    return false

            edges = moves(graph_copy, node)

            edges.sort(key=lambda x: len(
                moves(graph_copy, x[-1])) if sort_key == None else sort_key)

            for edge in edges:

                graph_copy.remove_edge(*edge, 1)
                if not dfs(graph_copy, edge[-1], [*trail, edge]):
                    return True
                graph_copy.add_edge(*edge, 1)

            win_callback(trail)
            if cnt_limit:
                cnt_limit -= 1
            return False

        return dfs(self.graph, node)
    
    

# def is_win_dfs(self, graph: UnlabeledMultiDiGraph, node: any, trail=None, sort_key=None):
#     if trail == None:
#         trail = []

#     if type(node) != BipartiteNode:
#         node = BipartiteNode(node, 0)

#     graph_copy = reachable_graph(graph, node)
#     node_type = self.fastly_classify(graph_copy, verbose=0)

#     # Ending State
#     if node in node_type:
#         if node_type[node] == WIN:
#             return true
#         else:
#             return false

#     edges = moves(graph_copy, node)
#     edges.sort(key=lambda x: len(
#         moves(graph_copy, x[-1])) if sort_key == None else sort_key)

#     for edge in edges:

#         graph_copy.remove_edge(*edge, 1)
#         if not is_win_dfs(graph_copy, edge[-1], [*trail, edge]):
#             return True
#         graph_copy.add_edge(*edge, 1)

#     return False


def get_unique_out_edges(graph: UnlabeledMultiDiGraph):
    nodes = [node for node, deg in graph.out_degree() if node.index ==
             0 and deg == 1]
    edges = [list(graph.out_edges(node))[0] for node in nodes]
    return edges


def reachable_graph(graph: UnlabeledMultiDiGraph, node: any) -> UnlabeledMultiDiGraph:
    if type(node) != BipartiteNode:
        node = BipartiteNode(node, 0)
    reachable_nodes = descendants(graph, node) | {node}
    subgraph = graph.subgraph(reachable_nodes).copy()
    return subgraph


def get_major_graph(graph: UnlabeledMultiDiGraph) -> UnlabeledMultiDiGraph:
    scc_list = list(strongly_connected_components(graph))
    scc_graph = condensation(graph, scc_list)
    leaf_scc_indices = {
        n for n in scc_graph if scc_graph.out_degree(n) == 0}
    leaf_sccs = [scc_list[i] for i in leaf_scc_indices]

    if len(leaf_sccs) != 1:
        raise Exception("주요 루트 없음")

    return graph.subgraph(leaf_sccs[0]).copy()


def moves(graph: UnlabeledMultiDiGraph, node: any):
    if type(node) != BipartiteNode:
        node = BipartiteNode(node, 0)

    return [(succ0, succ1)
            for succ0 in graph.successors(node)
            for succ1 in graph.successors(succ0)]
