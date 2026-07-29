# -*- coding: utf-8 -*-
"""Tool: shortest_path -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def shortest_path(graph: str, source, target):
    """Find shortest path between two nodes using BFS/Dijkstra.
    Input: graph (str) -- graph name. source -- start node. target -- end node.
    Output: dict with path (list) and length (int)."""
    g = _require_graph(graph)
    path = nx.shortest_path(g, source, target)
    return {"path": path, "length": len(path) - 1}
