from platform import node
import generalized_geography.solver.directed_vertex_geography as dvg
import networkx as nx


def remove_2_cycles(graph: nx.DiGraph, verbose=1):

    if verbose == 1:
        print("Remove 2 cycles : ", end="")

    to_remove = []

    # (a,b), (b,a) 꼴 엣지 검출
    for u, v in [(u, v) for u, v in graph.edges if u > v]:
        if graph.has_edge(v, u):
            to_remove.append((u, v))
            to_remove.append((v, u))

    # 검출한 엣지들 삭제
    graph.remove_edges_from(to_remove)

    if verbose == 1:
        print(len(to_remove), "edges removed")

    # 삭제된 엣지들 반환
    return to_remove


node_number = 10
graph_origin = nx.DiGraph(nx.random_k_out_graph(node_number, 5, 5))
graph = graph_origin.copy()
node_type_origin = dvg.completely_classify(graph)
print(node_type_origin)

remove_2_cycles(graph_origin)
graph = graph_origin.copy()
node_type = dvg.completely_classify(graph)
print(node_type)

print("".join([node_type_origin[i] for i in range(node_number)]))
print("".join([node_type[i] for i in range(node_number)]))
