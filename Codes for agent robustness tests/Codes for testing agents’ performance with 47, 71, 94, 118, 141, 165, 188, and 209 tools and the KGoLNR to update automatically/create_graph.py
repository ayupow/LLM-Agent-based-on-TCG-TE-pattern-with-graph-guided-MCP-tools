# -*- coding: utf-8 -*-
"""Tool: create_graph -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def create_graph(name: str, directed: bool = False):
    """Create a new graph (undirected or directed).
    Input: name (str) -- unique graph identifier. directed (bool=False) -- if True, create DiGraph.
    Output: dict with created name and type."""
    g = nx.DiGraph() if directed else nx.Graph()
    gs = _get_graphs()
    if name in gs:
        raise ValueError(f"Graph '{name}' already exists")
    gs[name] = g
    return {"created": name, "type": "directed" if directed else "undirected"}
