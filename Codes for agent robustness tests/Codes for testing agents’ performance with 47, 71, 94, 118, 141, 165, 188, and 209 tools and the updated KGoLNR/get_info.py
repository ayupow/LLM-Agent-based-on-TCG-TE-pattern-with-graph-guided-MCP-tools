# -*- coding: utf-8 -*-
"""Tool: get_info -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def get_info(graph: str):
    """Get basic information about a graph.
    Input: graph (str) -- graph name.
    Output: dict with nodes, edges, and directed flag."""
    g = _require_graph(graph)
    return {"nodes": g.number_of_nodes(), "edges": g.number_of_edges(),
            "directed": g.is_directed()}
