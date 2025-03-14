from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDigraph
import networkx as nx

def load_data():
  with open("generalized_geography/dataset/oldict.txt", "r", encoding="UTF-8") as f:
    return to_DEG([word.strip() for word in f.read().split("\n")])
  
def to_DEG(words):
  G = UnlabeledMultiDigraph()
  G.add_edges_from([(e[0], e[-1]) for e in words])
  
  return G

