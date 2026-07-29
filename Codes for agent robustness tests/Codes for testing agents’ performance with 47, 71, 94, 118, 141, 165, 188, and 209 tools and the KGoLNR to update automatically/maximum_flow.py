# -*- coding: utf-8 -*-
"""Tool: maximum_flow -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def maximum_flow(graph: str, source, sink, capacity: str = 'capacity'):
    """Calculate maximum flow in a directed graph.
    Input: graph (str) -- graph name. source -- source node. sink -- sink node.
           capacity (str='capacity') -- edge attribute for capacity.
    Output: dict with flow value and per-edge flows."""
    g = _require_graph(graph)
    if not g.is_directed():
        raise ValueError("Maximum flow requires a directed graph")
    flow_val, flow_dict = nx.maximum_flow(g, source, sink, capacity=capacity)
    return {"flow_value": flow_val, "flow": {str(k): {str(k2): v2 for k2, v2 in v.items()} for k, v in flow_dict.items()}}
