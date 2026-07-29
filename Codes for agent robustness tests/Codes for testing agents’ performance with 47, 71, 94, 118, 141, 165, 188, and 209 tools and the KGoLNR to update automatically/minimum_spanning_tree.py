# -*- coding: utf-8 -*-
"""Tool: minimum_spanning_tree -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def minimum_spanning_tree(graph: str, weight: str = 'weight', algorithm: str = 'kruskal'):
    """Find minimum spanning tree of an undirected graph.
    Input: graph (str) -- graph name. weight (str='weight') -- edge weight attribute.
           algorithm (str='kruskal') -- 'kruskal' or 'prim'.
    Output: dict with MST edges and total weight."""
    g = _require_graph(graph)
    if g.is_directed():
        raise ValueError("MST requires undirected graph")
    if algorithm == "prim":
        mst = nx.minimum_spanning_tree(g, weight=weight, algorithm="prim")
    else:
        mst = nx.minimum_spanning_tree(g, weight=weight, algorithm="kruskal")
    edges = [(u, v, g[u][v].get(weight, 1)) for u, v in mst.edges()]
    total = sum(w for _, _, w in edges)
    return {"edges": edges, "total_weight": total}
