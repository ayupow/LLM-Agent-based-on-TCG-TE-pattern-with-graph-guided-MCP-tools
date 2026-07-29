# -*- coding: utf-8 -*-
"""Tool: add_nodes -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def add_nodes(graph: str, nodes: list):
    """Add nodes to an existing graph.
    Input: graph (str) -- graph name. nodes (list) -- list of node IDs (str/int).
    Output: dict with added count and total nodes."""
    g = _require_graph(graph)
    g.add_nodes_from(nodes)
    return {"added": len(nodes), "total": g.number_of_nodes()}
