# -*- coding: utf-8 -*-
"""Tool: remove_nodes -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def remove_nodes(graph: str, nodes: list):
    """Remove nodes from a graph.
    Input: graph (str) -- graph name. nodes (list) -- node IDs to remove.
    Output: dict with removed count and remaining nodes."""
    g = _require_graph(graph)
    g.remove_nodes_from(nodes)
    return {"removed": len(nodes), "total_nodes": g.number_of_nodes()}
