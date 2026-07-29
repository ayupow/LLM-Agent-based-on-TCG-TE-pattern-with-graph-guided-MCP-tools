# -*- coding: utf-8 -*-
"""Tool: set_node_attributes -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def set_node_attributes(graph: str, attributes: dict):
    """Set attributes on one or more nodes.
    Input: graph (str) -- graph name. attributes (dict) -- {node: {attr: value}} mapping.
    Output: dict with updated count."""
    g = _require_graph(graph)
    for node, attrs in attributes.items():
        if node not in g:
            raise ValueError(f"Node '{node}' not found")
        for k, v in attrs.items():
            g.nodes[node][k] = v
    return {"updated": len(attributes)}
