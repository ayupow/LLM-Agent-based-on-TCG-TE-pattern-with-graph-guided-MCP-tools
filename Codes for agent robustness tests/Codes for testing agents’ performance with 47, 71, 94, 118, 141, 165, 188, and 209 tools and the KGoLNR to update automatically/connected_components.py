# -*- coding: utf-8 -*-
"""Tool: connected_components -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def connected_components(graph: str):
    """Find connected components in the graph.
    Input: graph (str) -- graph name.
    Output: dict with list of components and count."""
    g = _require_graph(graph)
    if g.is_directed():
        comps = list(nx.weakly_connected_components(g))
    else:
        comps = list(nx.connected_components(g))
    return {"components": [list(c) for c in comps], "count": len(comps)}
