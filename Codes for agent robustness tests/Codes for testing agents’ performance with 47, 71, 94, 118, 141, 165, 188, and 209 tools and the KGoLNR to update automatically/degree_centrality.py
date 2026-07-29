# -*- coding: utf-8 -*-
"""Tool: degree_centrality -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def degree_centrality(graph: str):
    """Calculate degree centrality for all nodes.
    Input: graph (str) -- graph name.
    Output: dict mapping node -> degree centrality value."""
    g = _require_graph(graph)
    return {"centrality": dict(nx.degree_centrality(g))}
