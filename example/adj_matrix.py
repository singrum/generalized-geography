import networkx as nx
import generalized_geography as gg
import matplotlib.pyplot as plt
import numpy as np
# 랜덤 그래프 생성
arr = np.array(
    [[4, 0, 0, 1, 1, 1, 1, 0, 1, 1],
     [2, 0, 0, 2, 0, 1, 0, 1, 3, 1],
     [2, 0, 0, 2, 0, 0, 0, 2, 2, 2],
     [1, 1, 1, 3, 0, 1, 0, 2, 1, 0],
     [2, 0, 2, 0, 0, 3, 0, 0, 2, 1],
     [4, 3, 0, 0, 0, 0, 0, 1, 2, 0],
     [2, 0, 0, 3, 0, 0, 0, 3, 0, 2],
     [3, 2, 2, 0, 1, 0, 0, 0, 1, 1],
     [1, 0, 0, 1, 0, 1, 0, 3, 2, 2],
     [0, 1, 2, 0, 0, 2, 1, 2, 0, 2]])
nodes = list(range(10))
graph_origin = nx.from_numpy_array(arr, create_using=nx.DiGraph)
graph = gg.UnlabeledMultiDiGraph()
graph.add_edges_from(graph_origin.edges(data="weight"))
graph_origin = graph

nodes = sorted(graph_origin.nodes())

mat = nx.to_numpy_array(graph_origin, nodelist=nodes,
                        weight="multiplicity", dtype=np.int8)


graph = graph_origin.copy()
node_type = gg.completely_classify(graph, verbose=0)

for row in mat:
    [print(e, end="") for e in row]
    print()
print("origin : " + "".join([node_type[node] for node in nodes]))

for u, v in graph_origin.edges:
    print(f"{u} -> {v}")
    for i in range(10):
        graph = graph_origin.copy()
        graph.add_edge(u, v, i)
        node_type = gg.completely_classify(graph, verbose=0)
        print("".join([node_type[node] for node in nodes]))
