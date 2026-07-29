# -*- coding: utf-8 -*-
"""Tool: graph_statistics -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def graph_statistics(graph: str):
    """Calculate comprehensive graph statistics.
    Input: graph (str) -- graph name.
    Output: dict with density, diameter, degree stats, etc."""
    import numpy as np
    g = _require_graph(graph)
    info = {"nodes": g.number_of_nodes(), "edges": g.number_of_edges(),
            "directed": g.is_directed(), "density": nx.density(g)}
    degrees = [d for _, d in g.degree()]
    if degrees:
        info["degree_stats"] = {"min": int(np.min(degrees)), "max": int(np.max(degrees)),
                                "mean": float(np.mean(degrees)), "std": float(np.std(degrees))}
    if g.is_directed():
        info["is_dag"] = nx.is_directed_acyclic_graph(g)
    return info
