

from typing import List, Tuple
import numpy as np
from generalized_geography.graph.cdeg import BipartiteEdge, BipartiteNode


class Encoder:
    def __init__(self, edges: List[Tuple[BipartiteNode, BipartiteNode]]):
        self.edge2index = edges
        self.index2edge = {edge: i for i, edge in enumerate(edges)}

    def encode(self, index: int):
        return self.index2edge[index]

    def decode(self, edge: BipartiteEdge):
        return self.edge2index[edge]

    def edges2vec(self, edges: List[BipartiteEdge]):
        vec = np.zeros(len(self.edge2index))
        for edge in edges:
            vec[self.encode(edge)] += 1
        return vec
