

import time
from typing import List
import generalized_geography as gg


# 단어 데이터셋 로드

with open("dataset/oldict.txt", "r", encoding="UTF-8") as f:
    words = [word.strip() for word in f.read().split("\n")]

rule = gg.Rule(0, -1, gg.std)
word_dict = gg.WordDict(rule, words)
graph = word_dict.make_graph()
solver = gg.CDEGSolver(graph)

print({n.value: solver.winlose[n] for n in solver.winlose if n.index == 0})
