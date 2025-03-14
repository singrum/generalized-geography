from networkx.classes.digraph import DiGraph
from networkx.exception import NetworkXError

class UnlabeledMultiDigraph(DiGraph):
  @classmethod
  def fromNxGraph(self, mdg):
    c = self()
    c.add_edges_from(mdg.edges())
    return c

  def edge_dict(self):
    return {"multiplicity" : 1}
  edge_attr_dict_factory = edge_dict

  def __init__(self):
    super().__init__()
  
  def add_edge(self, u, v, num = 1):
    if self.has_edge(u, v):
      self[u][v]['multiplicity'] += num
    else:
      super().add_edge(u, v, multiplicity = num)

  def add_edges_from(self, ebunch_to_add):
    for e in ebunch_to_add:
      ne = len(e)
      if ne == 3:
        u,v,multiplicity = e
      elif ne ==2:
        u,v = e
        multiplicity = 1
      else:
        raise NetworkXError("")
      self.add_edge(u,v, multiplicity)
  
  def remove_edge(self, u, v, num = None):
    if self.has_edge(u, v):
      if num != None and self[u][v]['multiplicity'] > num:
        self[u][v]['multiplicity'] -= num
      else:
        super().remove_edge(u, v)
  
  def remove_edges_from(self, ebunch):
    for e in ebunch:
      ne = len(e)
      if ne == 3:
        u,v,multiplicity = e
      elif ne ==2:
        u,v = e
        multiplicity = 1
      else:
        raise NetworkXError("")  
      self.remove_edge(u,v,multiplicity)

  def get_multiplicity(self, u, v):
    
    return self[u][v]['multiplicity'] if self.has_edge(u, v) else 0

  
  
