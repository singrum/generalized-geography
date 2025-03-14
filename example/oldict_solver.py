from generalized_geography.dataset.oldict import load_data
from generalized_geography.solver.directed_edge_geography import DEGGraphSolver
from generalized_geography.utils.constants import *

import math
import time


G = load_data()

solver = DEGGraphSolver(G)
start = time.time()
solver.classify_winlose(order="simple")
end = time.time()
print(end - start)


solver = DEGGraphSolver(G)
start = time.time()
solver.classify_winlose(order="fast")
end = time.time()
print(end - start)

