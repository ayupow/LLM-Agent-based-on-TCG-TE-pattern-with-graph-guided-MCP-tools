# -*- coding: utf-8 -*-
"""Tool: clustering_coefficients -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def clustering_coefficients(graph: str):
    """Calculate clustering coefficients for all nodes.
    Input: graph (str) -- graph name.
    Output: dict mapping node -> clustering coefficient."""
    g = _require_graph(graph)
    return {"clustering": dict(nx.clustering(g))}
