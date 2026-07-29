# -*- coding: utf-8 -*-
"""Tool: cycles_detection -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def cycles_detection(graph: str):
    """Detect cycles in a graph.
    Input: graph (str) -- graph name.
    Output: dict with cycle basis or DAG status."""
    g = _require_graph(graph)
    if g.is_directed():
        is_dag = nx.is_directed_acyclic_graph(g)
        return {"is_dag": is_dag, "message": "DAG: no cycles" if is_dag else "contains directed cycles"}
    cycles = list(nx.cycle_basis(g))
    return {"cycle_basis": cycles, "count": len(cycles)}
