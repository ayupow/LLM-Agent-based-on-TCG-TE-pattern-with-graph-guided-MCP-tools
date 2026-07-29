# -*- coding: utf-8 -*-
"""Tool: add_edges -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def add_edges(graph: str, edges: list):
    """Add edges to an existing graph.
    Input: graph (str) -- graph name. edges (list) -- list of [source, target] pairs.
    Output: dict with added count and total edges."""
    g = _require_graph(graph)
    edge_tuples = [tuple(e) for e in edges]
    g.add_edges_from(edge_tuples)
    return {"added": len(edge_tuples), "total": g.number_of_edges()}
