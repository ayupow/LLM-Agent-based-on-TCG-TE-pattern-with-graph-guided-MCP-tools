# -*- coding: utf-8 -*-
"""Tool: graph_coloring -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def graph_coloring(graph: str, strategy: str = 'largest_first'):
    """Color graph vertices using greedy algorithm.
    Input: graph (str) -- graph name. strategy (str='largest_first').
    Output: dict with node->color mapping and color count."""
    g = _require_graph(graph)
    coloring = nx.greedy_color(g, strategy=strategy)
    return {"coloring": coloring, "num_colors": max(coloring.values()) + 1 if coloring else 0}
