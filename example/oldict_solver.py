from generalized_geography.dataset.oldict import load_data
from generalized_geography.solver.directed_edge_geography import DEGGraphSolver
from generalized_geography.constants import *
G = load_data()
solver = DEGGraphSolver(G)
solver.classify_winlose()

# wins = sorted(solver.get_nodes_by_type(WIN))
# print("".join(wins))
# print("".join(sorted(solver.get_nodes_by_type(LOSE))))
# print("".join(sorted(solver.get_nodes_by_type(None))))
