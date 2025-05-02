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
graph.increase_edges_from(graph_origin.edges(data="weight"))
graph_origin = graph

nodes = sorted(graph_origin.nodes())

mat = nx.to_numpy_array(graph_origin, nodelist=nodes,
                        weight="num", dtype=np.int8)


graph = graph_origin.copy()
solver = gg.DEGSolver(graph)
solver.completely_classify()
node_type = solver.winlose

for row in mat:
    [print(e, end="") for e in row]
    print()
print("origin : " + "".join(["W" if node_type[node]
      == gg.WIN else "L" for node in nodes]))
