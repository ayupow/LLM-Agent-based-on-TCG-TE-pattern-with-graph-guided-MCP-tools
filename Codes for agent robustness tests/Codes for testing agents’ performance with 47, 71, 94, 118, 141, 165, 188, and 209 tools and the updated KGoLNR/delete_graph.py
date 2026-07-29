# -*- coding: utf-8 -*-
"""Tool: delete_graph -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def delete_graph(graph: str):
    """Delete a graph from storage.
    Input: graph (str) -- graph name to delete.
    Output: dict with deleted graph name."""
    _require_graph(graph)
    del _get_graphs()[graph]
    return {"deleted": graph}
