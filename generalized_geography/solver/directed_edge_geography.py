import networkx as nx
from collections import deque
from generalized_geography.constants import *



class DEGGraphSolver:
  def __init__(self, G : nx.MultiDiGraph):
    self._G_origin = G
    self._G_copy : nx.MultiDiGraph = G.copy()
    self.type = {node : None for node in G}
    self.pred = {node : None for node in G}

  # classify win, lose node involving loop
  def classify_winlose(self, verbose = 1, order = "fast"):
    if order == "fast":
      self.classify_reusable_winlose(verbose)
      self.remove_2_cycles(verbose)
      self.classify_loop_winlose(verbose)
      
    elif order == "simple":
      self.remove_2_cycles(verbose)
      self.classify_loop_winlose(verbose)

  def classify_loop_winlose(self, verbose = 1):

    if verbose == 1:
      print("Classify loop winlose : ", end="")

    # outedge가 없는 노드들
    lose_sinks = [node for node, deg in self._G_copy.out_degree() if deg == 0]
    # outedge가 loop edge 하나뿐인 노드들
    win_sinks = [node for node, deg in self._G_copy.out_degree() if deg == 1 and self._G_copy.has_edge(node, node)]

    for n in lose_sinks:
      self.type[n] = LOSE
    for n in win_sinks:
      self.type[n] = WIN

    q = deque(lose_sinks + win_sinks)

    while q:
      node = q.popleft()
      if self.type[node] == LOSE:
        preds = [pred for pred in self._G_copy.predecessors(node) if self.type[pred] == None]
        self._G_copy.remove_node(node)
        for pred in preds:
          self.type[pred] = WIN
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
          elif self._G_copy.out_degree(pred) == 1 and self._G_copy.has_edge(pred,pred):
            self.type[pred] = WIN
            self.pred[pred] = node
            q.append(pred)

    if verbose == 1:
      print(len(self.get_nodes_by_type(WIN)),"win,",len(self.get_nodes_by_type(LOSE)), "lose,", len(self.get_nodes_by_type(None)), "remain")

          

  # 재사용룰 필승, 필패 노드 분류
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
    


  def remove_2_cycles(self, verbose = 1):
    if verbose == 1:
      print("Remove 2 cycles : ", end="")
    to_remove = []
    
    # remove self loop even number
    for node in self._G_copy.nodes:
      num = self._G_copy.number_of_edges(node, node)
      to_remove += [(node,node)] * (num // 2) * 2
    distinct_edges = set(self._G_copy.edges())

    # remove 2 loop containing 2 distinct nodes
    for u,v in distinct_edges:
      if u >=v:
        continue
      if (u,v) in to_remove:
        continue
      if self._G_copy.has_edge(v,u):
        delete_num = min(self._G_copy.number_of_edges(u, v),  self._G_copy.number_of_edges(v, u))
        to_remove += [(u,v), (v,u)] * delete_num
    self._G_copy.remove_edges_from(to_remove)   

    if verbose == 1:
      print(len(to_remove), "edges removed")

    
  def get_nodes_by_type(self, node_type):
    return [node for node, type in self.type.items() if type == node_type]
  

  


if __name__ == "__main__":
  G = nx.MultiDiGraph()
  G.add_edges_from([(1,2),(1,2),(2,1),(1,1), (2,2),(2,2)])
  