# -*- coding: utf-8 -*-
"""Tool: import_csv -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def import_csv(graph: str, csv_data: str, directed: bool = False):
    """Import graph from CSV edge list (source,target per line).
    Input: graph (str) -- new graph name. csv_data (str) -- CSV text.
           directed (bool=False) -- create DiGraph if True.
    Output: dict with imported graph summary."""
    import csv, io
    gs = _get_graphs()
    if graph in gs:
        raise ValueError(f"Graph '{graph}' already exists")
    g = nx.DiGraph() if directed else nx.Graph()
    reader = csv.reader(io.StringIO(csv_data))
    edges = [(row[0].strip(), row[1].strip()) for row in reader if len(row) >= 2]
    g.add_edges_from(edges)
    gs[graph] = g
    return {"imported": graph, "nodes": g.number_of_nodes(),
            "edges": g.number_of_edges(), "directed": directed}
