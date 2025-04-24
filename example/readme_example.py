import generalized_geography as gg
import generalized_geography.graph.deg as deg

graph = gg.UnlabeledMultiDiGraph()
graph.add_edges_from([(0, 1), (0, 1), (1, 2), (2, 3),
                     (3, 0), (1, 2), (2, 3), (0, 2)])
node_type = deg.completely_classify(graph)
# node_type = {0: 'W', 1: 'L', 2: 'W', 3: 'L'}
