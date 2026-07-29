# -*- coding: utf-8 -*-
"""Tool: topological_sort -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def topological_sort(graph: str):
    """Return a topological ordering of a directed acyclic graph.
    Input: graph (str) -- graph name (must be a DAG).
    Output: dict with ordered node list."""
    g = _require_graph(graph)
    if not g.is_directed():
        raise ValueError("Topological sort requires a directed graph")
    if not nx.is_directed_acyclic_graph(g):
        raise ValueError("Graph contains cycles; topological sort requires a DAG")
    order = list(nx.topological_sort(g))
    return {"order": order, "count": len(order)}
