# -*- coding: utf-8 -*-
"""Tool: list_graphs -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def list_graphs():
    """List all stored graphs with summary info.
    Output: dict with list of graph summaries and total count."""
    gs = _get_graphs()
    result = []
    for name, g in gs.items():
        result.append({"name": name, "nodes": g.number_of_nodes(),
                       "edges": g.number_of_edges(), "directed": g.is_directed()})
    return {"graphs": result, "total": len(result)}
