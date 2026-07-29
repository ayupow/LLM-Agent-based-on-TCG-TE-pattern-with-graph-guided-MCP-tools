# -*- coding: utf-8 -*-
"""Tool: remove_edges -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def remove_edges(graph: str, edges: list):
    """Remove edges from a graph.
    Input: graph (str) -- graph name. edges (list) -- [source, target] pairs to remove.
    Output: dict with removed count and remaining edges."""
    g = _require_graph(graph)
    edge_tuples = [tuple(e) for e in edges]
    g.remove_edges_from(edge_tuples)
    return {"removed": len(edge_tuples), "total_edges": g.number_of_edges()}
