# -*- coding: utf-8 -*-
"""Tool: get_neighbors -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def get_neighbors(graph: str, node):
    """Get all neighbors of a node.
    Input: graph (str) -- graph name. node -- node to query.
    Output: dict with node, neighbors list, and count."""
    g = _require_graph(graph)
    if node not in g:
        raise ValueError(f"Node '{node}' not found in graph '{graph}'")
    neighbors = list(g.neighbors(node))
    return {"node": node, "neighbors": neighbors, "count": len(neighbors)}
