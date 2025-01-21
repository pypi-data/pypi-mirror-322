# Ubergraph

This is a package used to wrap [pygraphviz](https://pypi.org/project/pygraphviz/) to create ubergraphs.

Ubergraphs are based upon [the paper](https://arxiv.org/pdf/1704.05547.pdf).

# Importing ubergraph

from ubergraph import ubergraph

# Functions

## Create an ubergraph

You can create an ubergraph which is simply a directed graph in pygraphviz.

```python
u = ubergraph.ubergraph()
```

## Add a node to the ubergraph

You can add nodes to your ubergraph.

```python
u = ubergraph.add_node(u, "node")
```

## Add an edge to the ubergraph

You can add edges to your ubergraph.
The lists may be empty.
Any undefined nodes or edges will be added to the ubergraph.

```python
u = ubergraph.add_edge(u, "edge", list_of_from_nodes, list_of_to_nodes, list_of_from_edges, list_of_to_edges)
```

## Get the nodes in the ubergraph

You can get the nodes in your ubergraph.

```python
nodes = ubergraph.get_nodes(u)
```

## Get the edges in the ubergraph

You can get the edges in your ubergraph.

```python
edges = ubergraph.get_edges(u)
```

## MAY BE BUGGY: Get the nodes and edges from a node or edge

```python
froms = get_from(u, node_or_edge)
```

## MAY BE BUGGY: Get the nodes and edges to a node or edge

```python
tos = get_to(u, node_or_edge)
```

## MAY BE BUGGY: Get the edges that a node or edge is in

```python
in_edges = get_in_edges(u, node_or_edge)
```

## MAY BE BUGGY: Get the edges that is in a node or edge

```python
out_edges = get_out_edges(u, node_or_edge)
```

## View our ubergraph

Because our ubergraph, u, is a pygraphviz object we can view it by setting the layout (one of https://graphviz.org/docs/layouts/) and then drawing it:
```python
u.layout("circo") # could be other layouts from https://graphviz.org/docs/layouts/
u.draw("filename.png")
```