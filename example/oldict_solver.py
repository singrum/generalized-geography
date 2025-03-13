from generalized_geography.dataset.oldict import load_data
from generalized_geography.solver.directed_edge_geography import DEGGraphSolver
from generalized_geography.constants import *

import math
import time


G = load_data()
solver = DEGGraphSolver(G)
start = time.time()
solver.classify_reusable_winlose()
solver.remove_2_cycles()
solver.classify_loop_winlose()
end = time.time()

print(end - start)
solver = DEGGraphSolver(G)
start = time.time()
solver.classify_loop_winlose()
solver.remove_2_cycles()
solver.classify_loop_winlose()
end = time.time()
print(end - start)
# solver.classify_winlose()

