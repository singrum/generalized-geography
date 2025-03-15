import networkx as nx
from collections import deque
from generalized_geography.utils.constants import *
from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDiGraph


def fast_classify(graph : UnlabeledMultiDiGraph, verbose = 1):
  node_type1, _ = classify_reusable_winlose(graph, verbose)
  remove_2_cycles(graph, verbose)
  node_type2, _ = classify_loop_winlose(graph, verbose)
  node_type1
  return {**node_type1, **node_type2}
  
def complete_classify(graph : UnlabeledMultiDiGraph, verbose = 1):
  node_type1 = fast_classify(graph,verbose)
  node_type2 = classify_dfs_winlose(graph)
  return {**node_type1, **node_type2}

def remove_2_cycles(graph : UnlabeledMultiDiGraph, verbose = 1):

  if verbose == 1:
    print("Remove 2 cycles : ", end="")

  
  to_remove = []

  # remove self loop even number
  for node in graph.nodes:
    m = graph.get_multiplicity(node,node)
    
    if m >= 2:
      
      to_remove.append((node, node, m - m % 2))
  

  # remove 2 loop containing 2 distinct nodes
  for u,v in [(u,v) for u,v in graph.edges if u > v]:
    if graph.has_edge(v,u):
      delete_num = min(graph.get_multiplicity(u, v),  graph.get_multiplicity(v, u))
      to_remove.append((u, v, delete_num))
      to_remove.append((v, u, delete_num))

  graph.remove_edges_from(to_remove)
  
  if verbose == 1:
    print(sum([m for _,_,m in to_remove]), "edges removed")
  
  return to_remove


def classify_reusable_winlose(graph : UnlabeledMultiDiGraph, verbose = 1, sinks = None):
  if verbose == 1:
    print("Classify reusable winlose : ", end="")
  
  node_type = {}
  path_graph = nx.DiGraph()

  if not sinks:
    sinks = [node for node, deg in graph.out_degree() if deg == 0]
  
  q = deque()
  for sink in sinks:
    node_type[sink] = LOSE
    q.append(sink)
  
  while q:
    
    node = q.popleft()
    
    if node_type[node] == LOSE:
      preds = [pred for pred in graph.predecessors(node) if pred not in node_type]
      graph.remove_node(node)
      for pred in preds:
        node_type[pred] =WIN
        path_graph.add_edge(pred, node)
        q.append(pred)
    else:
      preds = [pred for pred in graph.predecessors(node) if pred not in node_type]
      graph.remove_node(node)
      for pred in preds:
        if graph.out_degree(pred) == 0 :
          node_type[pred] = LOSE
          path_graph.add_edge(pred, node)
          q.append(pred)

  if verbose == 1:
    win_nodes = [node for node in node_type if node_type[node] == WIN]
    lose_nodes = [node for node in node_type if node_type[node] == LOSE]
    
    print(len(win_nodes),"win,",len(lose_nodes), "lose,", len(graph), "remain")
  return node_type, path_graph


def classify_loop_winlose(graph : UnlabeledMultiDiGraph, verbose = 1, lose_sinks = None, win_sinks = None):
  
  if verbose == 1:
    print("Classify loop winlose : ", end="")
  
  node_type = {}
  path_graph = nx.DiGraph()

  # outedge가 없는 노드들
  if not lose_sinks:
    lose_sinks = [node for node, deg in graph.out_degree() if deg == 0]
  # outedge가 loop edge 하나뿐인 노드들
  if not win_sinks:
    win_sinks = win_sinks if win_sinks else [node for node, deg in graph.out_degree() if deg == 1 and graph.has_edge(node, node)]
  
  

  for n in lose_sinks:
    node_type[n] = LOSE
  for n in win_sinks:
    node_type[n] = WIN

  q = deque(lose_sinks + win_sinks)

  while q:
    node = q.popleft()
    if node_type[node] == LOSE:
      preds = [pred for pred in graph.predecessors(node) if pred not in node_type]
      graph.remove_node(node)
      for pred in preds:
        node_type[pred] = WIN
        path_graph.add_edge(pred, node)
        q.append(pred)
      
    else:
      preds = [pred for pred in graph.predecessors(node) if pred not in node_type]
      graph.remove_node(node)
      for pred in preds:
        if graph.out_degree(pred) == 0 :
          node_type[pred] = LOSE
          path_graph.add_edge(pred, node)
          q.append(pred)
        elif graph.out_degree(pred) == 1 and graph.get_multiplicity(pred,pred) == 1:
          node_type[pred] = WIN
          path_graph.add_edge(pred, pred)
          path_graph.add_edge(pred, node)
          q.append(pred)

  if verbose == 1:
    win_nodes = [node for node in node_type if node_type[node] == WIN]
    lose_nodes = [node for node in node_type if node_type[node] == LOSE]
    print(len(win_nodes),"win,",len(lose_nodes), "lose,", len(graph), "remain")
    
  return node_type, path_graph

def get_critical_edges(graph : UnlabeledMultiDiGraph):
  result = []
  for node in graph.nodes:
    outdeg = graph.multi_out_degree(node)
    
    if outdeg == 1:
      result.append(list(graph.out_edges(node))[0])

    elif outdeg == 2:
      edges = list(graph.out_edges(node,data = "multiplicity"))
      
      if len(edges) == 1:
        continue

      if edges[1] == node:
        result.append((edges[0][0], edges[0][1]))
      
      elif edges[0] == node:
        result.append((edges[1][0], edges[1][1]))

  return result




def is_win_dfs(graph : UnlabeledMultiDiGraph, node):
  graph_copy = graph.copy()
  node_type = fast_classify(graph, verbose=0)

  if node in node_type:
    if node_type[node] == WIN:
      return True
    else:
      return False
  
  for succ in graph.successors(node):
    graph_copy = graph.copy()
    graph_copy.remove_edge(node, succ)
    if not is_win_dfs(graph_copy, succ):
      return True
  return False

def classify_dfs_winlose(graph : UnlabeledMultiDiGraph):
  return {node : WIN if is_win_dfs(graph, node) else LOSE for node in graph}


if __name__ == "__main__":
  G = nx.MultiDiGraph()
  G.add_edges_from([(1,2),(1,2),(2,1),(1,1), (2,2),(2,2)])
  