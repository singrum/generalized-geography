import generalized_geography.solver.directed_vertex_geography as dvg
import networkx as nx

graph_origin = nx.DiGraph(nx.random_k_out_graph(10, 5, 5))
node_type = dvg.completely_classify(graph_origin)
print(node_type)
