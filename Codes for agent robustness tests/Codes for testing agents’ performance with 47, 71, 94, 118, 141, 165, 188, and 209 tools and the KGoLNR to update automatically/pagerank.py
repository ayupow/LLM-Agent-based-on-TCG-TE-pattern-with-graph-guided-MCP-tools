# -*- coding: utf-8 -*-
"""Tool: pagerank -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def pagerank(graph: str):
    """Calculate PageRank for all nodes.
    Input: graph (str) -- graph name.
    Output: dict mapping node -> PageRank value."""
    g = _require_graph(graph)
    return {"pagerank": dict(nx.pagerank(g))}
