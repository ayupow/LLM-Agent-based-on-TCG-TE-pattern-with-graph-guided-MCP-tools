# -*- coding: utf-8 -*-
"""Tool: merge_graphs -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def merge_graphs(graph_a: str, graph_b: str, new_graph: str):
    """Compose two graphs into a new graph (union of nodes+edges).
    Input: graph_a (str), graph_b (str) -- source graphs.
           new_graph (str) -- name for composed graph.
    Output: dict with merged graph summary."""
    ga = _require_graph(graph_a)
    gb = _require_graph(graph_b)
    if type(ga) is not type(gb):
        raise ValueError("Cannot merge different graph types (directed vs undirected)")
    merged = nx.compose(ga, gb)
    gs = _get_graphs()
    if new_graph in gs:
        raise ValueError(f"Graph '{new_graph}' already exists")
    gs[new_graph] = merged
    return {"new_graph": new_graph, "nodes": merged.number_of_nodes(),
            "edges": merged.number_of_edges(), "source_graphs": [graph_a, graph_b]}
