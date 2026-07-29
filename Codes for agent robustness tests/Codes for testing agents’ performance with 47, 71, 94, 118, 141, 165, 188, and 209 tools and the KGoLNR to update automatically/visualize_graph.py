# -*- coding: utf-8 -*-
"""Tool: visualize_graph -- NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def visualize_graph(graph: str, layout: str = 'spring'):
    """Create a base64-encoded PNG visualization of the graph.
    Input: graph (str) -- graph name. layout (str='spring') -- 'spring','circular','kamada_kawai'.
    Output: dict with base64 image and format."""
    import base64, io, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    g = _require_graph(graph)
    fig, ax = plt.subplots(figsize=(8, 6))
    pos_map = {"spring": nx.spring_layout, "circular": nx.circular_layout,
               "kamada_kawai": nx.kamada_kawai_layout}
    pos = pos_map.get(layout, nx.spring_layout)(g)
    nx.draw(g, pos, ax=ax, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=500, font_size=10)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    return {"visualization": base64.b64encode(buf.getvalue()).decode(),
            "format": "png", "layout": layout}
