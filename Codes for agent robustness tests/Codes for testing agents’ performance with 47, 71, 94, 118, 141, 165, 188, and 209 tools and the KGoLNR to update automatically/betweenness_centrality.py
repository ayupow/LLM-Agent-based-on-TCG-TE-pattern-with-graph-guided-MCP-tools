# -*- coding: utf-8 -*-
"""Tool: betweenness_centrality -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def betweenness_centrality(graph: str):
    """Calculate betweenness centrality for all nodes.
    Input: graph (str) -- graph name.
    Output: dict mapping node -> betweenness centrality value."""
    g = _require_graph(graph)
    return {"centrality": dict(nx.betweenness_centrality(g))}
