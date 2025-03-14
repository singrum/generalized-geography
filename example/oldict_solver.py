from generalized_geography.dataset.oldict import load_data
from generalized_geography.solver.directed_edge_geography import *
from generalized_geography.utils.constants import *

import time


graph = load_data()
start = time.time()

classify_reusable_winlose(graph)
remove_2_cycles(graph)
classify_loop_winlose(graph)
remove_2_cycles(graph)

end = time.time()


