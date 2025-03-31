

import time
import generalized_geography as gg
import generalized_geography.game.kkutmal as km


# 단어 데이터셋 로드
with open("dataset/oldict.txt", "r", encoding="UTF-8") as f:
    words = [word.strip() for word in f.read().split("\n")]

word_dict = km.WordDict(km.Rule(0, -1, km.std), words)
graph = word_dict.to_graph()
node_type = km.fastly_classify(graph)

start = time.time()
print(km.is_win_dfs(graph, "업"))
end = time.time()
print(end - start)


# 승패 분류 후 중립 음절만 남김
# wc = [node.value for (node, t)
#       in node_type.items() if t == "W" if node.index == 0]
# ww = [node.value for (node, t)
#       in node_type.items() if t == "W" if node.index == 1]
# print("승리 : " + ", ".join(wc))
# lc = [node.value for (node, t)
#       in node_type.items() if t == "L" if node.index == 0]
# lw = [node.value for (node, t)
#       in node_type.items() if t == "L" if node.index == 1]
# print("패배 : " + ", ".join(lc))

# rc = [value for (value, index) in graph.nodes if index == 0]
# rw = [value for (value, index) in graph.nodes if index == 1]
# print("루트 : " + ", ".join(rc))
