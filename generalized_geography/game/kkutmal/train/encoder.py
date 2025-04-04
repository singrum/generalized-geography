

from typing import Tuple

from generalized_geography.game.kkutmal.graph.solver import BipartiteNode


class Encoder:
    def __init__(self, edges: list[Tuple[BipartiteNode, BipartiteNode]]):
        self.edges_map = edges
        self.index_map = {edge: i for i, edge in enumerate(edges)}

    def encode(self, index: int):
        return self.index_map[index]

    def decode(self, edge: Tuple[BipartiteNode, BipartiteNode]):
        return self.edges_map[edge]
