# -*- coding: utf-8 -*-
"""Tool: export_json -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def export_json(graph: str):
    """Export graph as JSON in node-link format.
    Input: graph (str) -- graph name.
    Output: dict with node-link JSON data."""
    import json
    g = _require_graph(graph)
    data = nx.node_link_data(g, edges="links")
    return {"graph": graph, "data": data}
