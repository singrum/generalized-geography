import networkx as nx
from collections import deque
from generalized_geography.utils.constants import *
from generalized_geography.classes.unlabeled_multidigraph import UnlabeledMultiDigraph


  
def remove_2_cycles(graph : UnlabeledMultiDigraph, verbose = 1):

  if verbose == 1:
    print("Remove 2 cycles : ", end="")

  
  cycle_graph = UnlabeledMultiDigraph()

  
  
  # remove self loop even number
  for node in graph.nodes:
    m = graph.get_multiplicity(node,node)
    
    if m >= 2:
      
      cycle_graph.add_edge(node, node, num = m - m % 2)
  

  # remove 2 loop containing 2 distinct nodes
  for u,v in [(u,v) for u,v in graph.edges if u > v]:
    if graph.has_edge(v,u):
      delete_num = min(graph.get_multiplicity(u, v),  graph.get_multiplicity(v, u))
      cycle_graph.add_edge(u, v, delete_num)
      cycle_graph.add_edge(v, u, delete_num)

  graph.remove_edges_from(cycle_graph.edges(data = "multiplicity"))
  
  if verbose == 1:
    print(sum([m for _,_,m in cycle_graph.edges(data = "multiplicity")]), "edges removed")
  
  return cycle_graph


def classify_reusable_winlose(graph : UnlabeledMultiDigraph, verbose = 1):
  if verbose == 1:
    print("Classify reusable winlose : ", end="")
  
  sinks = [node for node, deg in graph.out_degree() if deg == 0]
  node_type = {}
  path_graph = nx.DiGraph()

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


def classify_loop_winlose(graph : UnlabeledMultiDigraph, verbose = 1):
  
  if verbose == 1:
    print("Classify loop winlose : ", end="")
  
  node_type = {}
  path_graph = nx.DiGraph()

  # outedge가 없는 노드들
  lose_sinks = [node for node, deg in graph.out_degree() if deg == 0]
  # outedge가 loop edge 하나뿐인 노드들
  win_sinks = [node for node, deg in graph.out_degree() if deg == 1 and graph.has_edge(node, node)]
  
  

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
    
  return 

if __name__ == "__main__":
  G = nx.MultiDiGraph()
  G.add_edges_from([(1,2),(1,2),(2,1),(1,1), (2,2),(2,2)])
  