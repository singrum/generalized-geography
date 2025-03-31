import networkx as nx
import generalized_geography as gg
import generalized_geography.game.directed_edge_geography.solver as deg
import matplotlib.pyplot as plt
import random


def get_distinct_choice(arr, k):
    arr_copy = arr.copy()
    random.shuffle(arr_copy)
    return [arr_copy.pop() for _ in range(k)]


node_number = 10

# 랜덤 그래프 생성 후 승패 분류
graph_origin = nx.MultiDiGraph()
graph_origin.add_nodes_from(list(range(node_number)))

graph = gg.UnlabeledMultiDiGraph.from_nx_graph(graph_origin)
node_type = deg.completely_classify(graph, verbose=0)
print("".join([node_type[i] for i in range(node_number)]))

for _ in range(100):
    # 사이클 추가
    random_cycle = get_distinct_choice(list(range(10)), 4)
    nx.add_cycle(graph_origin, random_cycle)
    graph = gg.UnlabeledMultiDiGraph.from_nx_graph(graph_origin)
    node_type = deg.completely_classify(graph, verbose=0)
    print("".join([node_type[i] for i in range(node_number)]))
