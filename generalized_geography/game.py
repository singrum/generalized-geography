from typing import List

from generalized_geography.app.rule import Rule
from generalized_geography.app.word_dict import WordDict
from generalized_geography.common.unlabeled_multidigraph import UnlabeledMultiDiGraph
from generalized_geography.graph.cdeg import CDEG, BipartiteEdge, get_major_graph
from generalized_geography.vector.encoder import Encoder


class Game:
    word_dict: WordDict
    cdeg = CDEG
    major_graph = UnlabeledMultiDiGraph

    def __init__(self, rule: Rule, words: List[str]):
        self.word_dict = WordDict(rule, words)

        self.cdeg = CDEG(self.word_dict.make_graph())
        self.cdeg.fastly_classify()

        self.major_graph = get_major_graph(self.cdeg.graph)
        self.major_edges = [e for e in self.major_graph.edges(
            data="multiplicity") if e[0].index == 1]
        self.encoder = Encoder(self.major_edges)

    def record_trails(self, path, trails_per_word=100):

        def win_callback(trail: List[BipartiteEdge]):
            text = " ".join([head+tail for (head, _), (tail, _) in trail])
            with open(path, "a", encoding="UTF-8") as f:
                f.write(text + "\n")

        for s, t, _ in self.major_edges:
            print(s.value+t.value)
            graph = self.cdeg.graph.copy()
            graph.remove_edge(s, t, 1)
            cdeg = CDEG(graph)
            try:
                cdeg.is_win(t, win_callback=win_callback,
                            cnt_limit=trails_per_word)
            except:
                pass
