
from generalized_geography.solver.directed_edge_geography import *
from generalized_geography.utils.constants import *
from networkx.algorithms.components.strongly_connected import strongly_connected_components
from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDiGraph
import time

# 단어 데이터셋 로드
with open("dataset/oldict.txt", "r", encoding="UTF-8") as f:
    words = [word.strip() for word in f.read().split("\n")]

# 단어 리스트를 그래프로 변환
graph = UnlabeledMultiDiGraph()
graph.add_edges_from([(e[0], e[-1]) for e in words])

# 승패 분류 후 중립 음절만 남김
start = time.time()
classify_reusable_winlose(graph)
remove_2_cycles(graph)
classify_loop_winlose(graph)
end = time.time()

print(f"time : {round(end - start,3)}")


max_scc = list(strongly_connected_components(graph))[0]


# print(end-start)

