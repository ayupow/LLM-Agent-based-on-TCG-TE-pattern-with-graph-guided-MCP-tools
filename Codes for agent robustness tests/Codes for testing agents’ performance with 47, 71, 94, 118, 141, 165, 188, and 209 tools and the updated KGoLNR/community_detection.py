# -*- coding: utf-8 -*-
"""Tool: community_detection -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def community_detection(graph: str):
    """Detect communities using Louvain method (greedy modularity).
    Input: graph (str) -- graph name (undirected recommended).
    Output: dict with communities (list of sets) and modularity score."""
    from networkx.algorithms.community import greedy_modularity_communities
    g = _require_graph(graph)
    comms = list(greedy_modularity_communities(g))
    return {"communities": [list(c) for c in comms], "count": len(comms)}
