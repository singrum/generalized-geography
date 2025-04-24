import networkx as nx
import generalized_geography as gg
import generalized_geography.graph.deg as deg
import matplotlib.pyplot as plt

# 랜덤 그래프 생성
graph_origin = nx.DiGraph(nx.random_k_out_graph(10, 5, 5))

# 그래프를 UnlabeledMultiDiGraph형식으로 변환
graph_origin = gg.UnlabeledMultiDiGraph.from_nx_graph(graph_origin)
deg.remove_2_cycles(graph_origin)

# 그래프 복사
graph = graph_origin.copy()

# 모든 노드드의 승/패 여부를 알아냄
node_type = deg.completely_classify(graph)

# 필승 노드, 필패 노드를 각각 모아서 리스트로 만듦
win_nodes = [node for node in graph_origin.nodes if node_type[node] == "W"]
lose_nodes = [node for node in graph_origin.nodes if node_type[node] == "L"]

# 그래프 출력
pos = nx.shell_layout(graph_origin)
options = {"node_size": 70}
nx.draw_networkx_nodes(graph_origin, pos, nodelist=win_nodes,
                       node_color="tab:blue", **options)
nx.draw_networkx_nodes(graph_origin, pos, nodelist=lose_nodes,
                       node_color="tab:red", **options)
nx.draw_networkx_edges(graph_origin, pos, width=1.0,
                       alpha=1, connectionstyle='arc3, rad = 0.1', **options)

plt.show()
