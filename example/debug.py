from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDigraph
import networkx as nx

g = UnlabeledMultiDigraph()
g.add_edge(1,2)
print(g.copy()[1])

