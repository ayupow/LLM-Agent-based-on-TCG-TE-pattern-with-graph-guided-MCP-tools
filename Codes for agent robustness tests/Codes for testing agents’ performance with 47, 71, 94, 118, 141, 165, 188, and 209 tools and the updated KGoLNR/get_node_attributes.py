# -*- coding: utf-8 -*-
"""Tool: get_node_attributes -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def get_node_attributes(graph: str, node):
    """Get all attributes of a specific node.
    Input: graph (str) -- graph name. node -- node to query.
    Output: dict with node and its attributes."""
    g = _require_graph(graph)
    if node not in g:
        raise ValueError(f"Node '{node}' not found")
    return {"node": node, "attributes": dict(g.nodes[node])}
