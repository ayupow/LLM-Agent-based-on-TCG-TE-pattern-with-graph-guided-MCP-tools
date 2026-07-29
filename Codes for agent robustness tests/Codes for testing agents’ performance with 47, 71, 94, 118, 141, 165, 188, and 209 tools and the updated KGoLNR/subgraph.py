# -*- coding: utf-8 -*-
"""Tool: subgraph -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def subgraph(graph: str, nodes: list, new_graph: str):
    """Extract an induced subgraph and store as new graph.
    Input: graph (str) -- source graph. nodes (list) -- node subset.
           new_graph (str) -- name for new subgraph.
    Output: dict with new graph summary."""
    g = _require_graph(graph)
    missing = [n for n in nodes if n not in g]
    if missing:
        raise ValueError(f"Nodes not found: {missing}")
    sub = g.subgraph(nodes).copy()
    gs = _get_graphs()
    if new_graph in gs:
        raise ValueError(f"Graph '{new_graph}' already exists")
    gs[new_graph] = sub
    return {"source": graph, "new_graph": new_graph,
            "nodes": sub.number_of_nodes(), "edges": sub.number_of_edges()}
