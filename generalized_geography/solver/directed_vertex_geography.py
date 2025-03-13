import networkx as nx
from collections import deque
from generalized_geography.constants import *



class DVGGraphSolver:
  def __init__(self, G : nx.DiGraph):
    self._G_origin = G
    self._G_copy : nx.DiGraph = G.copy()
    self.type = {node : None for node in G}
    self.pred = {node : None for node in G}


  def classify_winlose(self, verbose = 1):
    self.remove_loops()
    self.classify_reusable_winlose(verbose)

  def remove_loops(self, verbose = 1):

    if verbose == 1:
      print("Remove loops : ", end="")

    to_remove = []

    for node in self._G_copy.nodes:
      if self._G_copy.has_edge(node, node):
        to_remove.append((node, node))

    self._G_copy.remove_edges_from(to_remove)

    if verbose == 1:
      print(len(to_remove), "edges removed")

  
  def classify_reusable_winlose(self, verbose = 1):
    
    if verbose == 1:
      print("Classify reusable winlose : ", end="")

    sinks = [node for node, deg in self._G_copy.out_degree() if deg == 0]

    q = deque()

    for sink in sinks:
      self.type[sink] = LOSE
      q.append(sink)
    
    while q:
      
      node = q.popleft()
      
      if self.type[node] == LOSE:
        preds = [pred for pred in self._G_copy.predecessors(node) if self.type[pred] == None]
        self._G_copy.remove_node(node)
        for pred in preds:
          self.type[pred] =WIN
          self.pred[pred] = node
          q.append(pred)
      else:
        preds = [pred for pred in self._G_copy.predecessors(node) if self.type[pred] == None]
        self._G_copy.remove_node(node)
        for pred in preds:
          if self._G_copy.out_degree(pred) == 0 :
            self.type[pred] = LOSE
            self.pred[pred] = node
            q.append(pred)
    if verbose == 1:
      print(len(self.get_nodes_by_type(WIN)),"win,",len(self.get_nodes_by_type(LOSE)), "lose,", len(self.get_nodes_by_type(None)), "remain")
    

  def get_nodes_by_type(self, node_type):
    return [node for node, type in self.type.items() if type == node_type]
  

  


if __name__ == "__main__":
  G = nx.MultiDiGraph()
  G.add_edges_from([(1,2),(1,2),(2,1),(1,1), (2,2),(2,2)])
  

  # print(nx.adjacency_matrix(G))