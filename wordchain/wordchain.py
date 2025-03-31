

import time
import generalized_geography as gg
from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDiGraph
import generalized_geography.solver.changeable_directed_edge_geography as cdeg
import networkx as nx

import change_rules


# 단어 데이터셋 로드
with open("dataset/oldict.txt", "r", encoding="UTF-8") as f:
    words = [word.strip() for word in f.read().split("\n")]


def get_graph(words) -> gg.UnlabeledMultiDiGraph:
    graph = gg.UnlabeledMultiDiGraph()
    chars = set()
    for word in words:
        chars.update(word[0], word[-1])

    chan_edges = sum([
        [(cdeg.BipartiteNode(char, 0), cdeg.BipartiteNode(chan, 1))
         for chan in change_rules.std(char) if chan in chars]
        for char in chars], [])
    word_edges = [(cdeg.BipartiteNode(word[0], 1), cdeg.BipartiteNode(word[-1], 0))
                  for word in words]
    graph.add_edges_from(chan_edges + word_edges)
    return graph


start = time.time()
graph = get_graph(words)
node_type1 = cdeg.classify_reusable_winlose(graph)
cdeg.remove_2_cycles(graph)
node_type2 = cdeg.classify_loop_winlose(graph)
end = time.time()

print(f"{end - start:.5f} sec")

exit()
node_type = {**node_type1, **node_type2}

# 승패 분류 후 중립 음절만 남김
wc = [node.value for (node, t)
      in node_type.items() if t == "W" if node.index == 0]
ww = [node.value for (node, t)
      in node_type.items() if t == "W" if node.index == 1]
print("승리 : " + ", ".join(wc))
lc = [node.value for (node, t)
      in node_type.items() if t == "L" if node.index == 0]
lw = [node.value for (node, t)
      in node_type.items() if t == "L" if node.index == 1]
print("패배 : " + ", ".join(lc))

rc = [value for (value, index) in graph.nodes if index == 0]
rw = [value for (value, index) in graph.nodes if index == 1]
print("루트 : " + ", ".join(rc))
