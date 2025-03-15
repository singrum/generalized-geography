import networkx as nx
import matplotlib.pyplot as plt
from generalized_geography.solver.directed_edge_geography import *
from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDiGraph
from generalized_geography.utils.constants import *

graph_origin = nx.DiGraph(nx.random_k_out_graph(10,5,5))
# graph_origin = nx.DiGraph(nx.erdos_renyi_graph(10,1,directed = True))

graph_origin = UnlabeledMultiDiGraph.fromNxGraph(graph_origin)
remove_2_cycles(graph_origin)

graph = graph_origin.copy()

node_type = complete_classify(graph)

win_nodes = [node for node in graph_origin.nodes if node in node_type and node_type[node] == WIN]
lose_nodes = [node for node in graph_origin.nodes if node in node_type and node_type[node] == LOSE]
remain_nodes = [node for node in graph_origin.nodes if node not in node_type]

pos = nx.shell_layout(graph_origin)
options = {"node_size": 70}
nx.draw_networkx_nodes(graph_origin, pos, nodelist=win_nodes, node_color="tab:blue", **options)
nx.draw_networkx_nodes(graph_origin, pos, nodelist=lose_nodes, node_color="tab:red",**options)
# nx.draw_networkx_nodes(graph_origin, pos, nodelist=remain_nodes, node_color="tab:green",**options)
nx.draw_networkx_edges(graph_origin, pos, width=1.0, alpha=1,connectionstyle='arc3, rad = 0.1',**options)



plt.show()