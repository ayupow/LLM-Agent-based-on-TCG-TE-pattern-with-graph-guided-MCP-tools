# -*- coding: utf-8 -*-
"""Tool: centrality_measures -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def centrality_measures(graph: str, measures: list = None):
    """Calculate multiple centrality measures.
    Input: graph (str) -- graph name. measures (list, optional) -- subset of:
           ['degree','betweenness','closeness','eigenvector']. None = all four.
    Output: dict with per-measure node->value mappings."""
    g = _require_graph(graph)
    if measures is None:
        measures = ['degree', 'betweenness', 'closeness', 'eigenvector']
    result = {}
    if 'degree' in measures:
        result['degree_centrality'] = dict(nx.degree_centrality(g))
    if 'betweenness' in measures:
        result['betweenness_centrality'] = dict(nx.betweenness_centrality(g))
    if 'closeness' in measures:
        result['closeness_centrality'] = dict(nx.closeness_centrality(g))
    if 'eigenvector' in measures:
        try:
            result['eigenvector_centrality'] = dict(nx.eigenvector_centrality(g, max_iter=1000))
        except Exception:
            result['eigenvector_centrality'] = {"error": "failed to converge"}
    return result
