# -*- coding: utf-8 -*-
"""Tool: matching -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def matching(graph: str, max_cardinality: bool = True):
    """Find maximum weight matching in a graph.
    Input: graph (str) -- graph name. max_cardinality (bool=True).
    Output: dict with matching edges and count."""
    g = _require_graph(graph)
    match = nx.max_weight_matching(g, maxcardinality=max_cardinality)
    return {"matching": list(match), "count": len(match)}
