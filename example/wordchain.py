
import generalized_geography as gg
import generalized_geography.solver.directed_edge_geography as deg
import networkx as nx
import time


# 단어 데이터셋 로드
with open("dataset/oldict.txt", "r", encoding="UTF-8") as f:
    words = [word.strip() for word in f.read().split("\n")]

# 단어 리스트를 그래프로 변환
graph = gg.UnlabeledMultiDiGraph()
graph.add_edges_from([(e[0], e[-1]) for e in words])

# 승패 분류 후 중립 음절만 남김
start = time.time()
deg.fastly_classify(graph)
end = time.time()

print(f"time : {round(end - start, 3)}")
