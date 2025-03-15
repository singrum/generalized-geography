# Generalized Geography Game Solver

## Install

```console
$ pip install generalized-geography
```

## Example

```console
>>> import generalized_geography as gg
>>> graph = gg.UnlabeledMultiDiGraph()
>>> graph.add_edges_from([(0,1), (0,1), (1,2), (2,3), (3,0), (1,2), (2,3), (0,2)])
>>> node_type = gg.complete_classify(graph)
>>> print("Win Nodes :", [node for node, type in node_type.items() if type == gg.WIN])
Win Nodes : [0, 2]
>>> print("Lose Nodes :", [node for node, type in node_type.items() if type == gg.LOSE])
Lose Nodes : [1, 3]
```
