

from generalized_geography.common.unlabeled_multidigraph import UnlabeledMultiDiGraph
from generalized_geography.game.kkutmal.graph.solver import fastly_classify, get_major_graph
from generalized_geography.game.kkutmal.train.encoder import Encoder


class Game:
    def __init__(self, graph: UnlabeledMultiDiGraph):
        self.original_graph = graph
        self.node_type = fastly_classify(graph)
        self.major_graph = get_major_graph(graph)
        self.encoder = Encoder(
            [e for e in self.major_graph.edges if e[0].index == 1])
