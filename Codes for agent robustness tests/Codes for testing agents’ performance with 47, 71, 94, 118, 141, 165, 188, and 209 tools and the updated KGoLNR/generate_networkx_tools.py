# Generate standalone NetworkX MCP tool files from templates
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, 'tools_networkx')

# Each entry: (filename, func_name, params_str, body_code, description)
tools = [
    # === Graph Management ===
    ("create_graph", "create_graph",
     "name: str, directed: bool = False",
     '''    """Create a new graph (undirected or directed).
    Input: name (str) — unique graph identifier. directed (bool=False) — if True, create DiGraph.
    Output: dict with created name and type."""
    g = nx.DiGraph() if directed else nx.Graph()
    gs = _get_graphs()
    if name in gs:
        raise ValueError(f"Graph '{name}' already exists")
    gs[name] = g
    return {"created": name, "type": "directed" if directed else "undirected"}'''),

    ("add_nodes", "add_nodes",
     "graph: str, nodes: list",
     '''    """Add nodes to an existing graph.
    Input: graph (str) — graph name. nodes (list) — list of node IDs (str/int).
    Output: dict with added count and total nodes."""
    g = _require_graph(graph)
    g.add_nodes_from(nodes)
    return {"added": len(nodes), "total": g.number_of_nodes()}'''),

    ("add_edges", "add_edges",
     "graph: str, edges: list",
     '''    """Add edges to an existing graph.
    Input: graph (str) — graph name. edges (list) — list of [source, target] pairs.
    Output: dict with added count and total edges."""
    g = _require_graph(graph)
    edge_tuples = [tuple(e) for e in edges]
    g.add_edges_from(edge_tuples)
    return {"added": len(edge_tuples), "total": g.number_of_edges()}'''),

    ("get_info", "get_info",
     "graph: str",
     '''    """Get basic information about a graph.
    Input: graph (str) — graph name.
    Output: dict with nodes, edges, and directed flag."""
    g = _require_graph(graph)
    return {"nodes": g.number_of_nodes(), "edges": g.number_of_edges(),
            "directed": g.is_directed()}'''),

    ("list_graphs", "list_graphs",
     "",
     '''    """List all stored graphs with summary info.
    Output: dict with list of graph summaries and total count."""
    gs = _get_graphs()
    result = []
    for name, g in gs.items():
        result.append({"name": name, "nodes": g.number_of_nodes(),
                       "edges": g.number_of_edges(), "directed": g.is_directed()})
    return {"graphs": result, "total": len(result)}'''),

    ("delete_graph", "delete_graph",
     "graph: str",
     '''    """Delete a graph from storage.
    Input: graph (str) — graph name to delete.
    Output: dict with deleted graph name."""
    _require_graph(graph)
    del _get_graphs()[graph]
    return {"deleted": graph}'''),

    ("remove_nodes", "remove_nodes",
     "graph: str, nodes: list",
     '''    """Remove nodes from a graph.
    Input: graph (str) — graph name. nodes (list) — node IDs to remove.
    Output: dict with removed count and remaining nodes."""
    g = _require_graph(graph)
    g.remove_nodes_from(nodes)
    return {"removed": len(nodes), "total_nodes": g.number_of_nodes()}'''),

    ("remove_edges", "remove_edges",
     "graph: str, edges: list",
     '''    """Remove edges from a graph.
    Input: graph (str) — graph name. edges (list) — [source, target] pairs to remove.
    Output: dict with removed count and remaining edges."""
    g = _require_graph(graph)
    edge_tuples = [tuple(e) for e in edges]
    g.remove_edges_from(edge_tuples)
    return {"removed": len(edge_tuples), "total_edges": g.number_of_edges()}'''),

    # === Path & Neighbors ===
    ("shortest_path", "shortest_path",
     "graph: str, source, target",
     '''    """Find shortest path between two nodes using BFS/Dijkstra.
    Input: graph (str) — graph name. source — start node. target — end node.
    Output: dict with path (list) and length (int)."""
    g = _require_graph(graph)
    path = nx.shortest_path(g, source, target)
    return {"path": path, "length": len(path) - 1}'''),

    ("get_neighbors", "get_neighbors",
     "graph: str, node",
     '''    """Get all neighbors of a node.
    Input: graph (str) — graph name. node — node to query.
    Output: dict with node, neighbors list, and count."""
    g = _require_graph(graph)
    if node not in g:
        raise ValueError(f"Node '{node}' not found in graph '{graph}'")
    neighbors = list(g.neighbors(node))
    return {"node": node, "neighbors": neighbors, "count": len(neighbors)}'''),

    # === Attributes ===
    ("set_node_attributes", "set_node_attributes",
     "graph: str, attributes: dict",
     '''    """Set attributes on one or more nodes.
    Input: graph (str) — graph name. attributes (dict) — {node: {attr: value}} mapping.
    Output: dict with updated count."""
    g = _require_graph(graph)
    for node, attrs in attributes.items():
        if node not in g:
            raise ValueError(f"Node '{node}' not found")
        for k, v in attrs.items():
            g.nodes[node][k] = v
    return {"updated": len(attributes)}'''),

    ("get_node_attributes", "get_node_attributes",
     "graph: str, node",
     '''    """Get all attributes of a specific node.
    Input: graph (str) — graph name. node — node to query.
    Output: dict with node and its attributes."""
    g = _require_graph(graph)
    if node not in g:
        raise ValueError(f"Node '{node}' not found")
    return {"node": node, "attributes": dict(g.nodes[node])}'''),

    # === Algorithms ===
    ("degree_centrality", "degree_centrality",
     "graph: str",
     '''    """Calculate degree centrality for all nodes.
    Input: graph (str) — graph name.
    Output: dict mapping node -> degree centrality value."""
    g = _require_graph(graph)
    return {"centrality": dict(nx.degree_centrality(g))}'''),

    ("betweenness_centrality", "betweenness_centrality",
     "graph: str",
     '''    """Calculate betweenness centrality for all nodes.
    Input: graph (str) — graph name.
    Output: dict mapping node -> betweenness centrality value."""
    g = _require_graph(graph)
    return {"centrality": dict(nx.betweenness_centrality(g))}'''),

    ("connected_components", "connected_components",
     "graph: str",
     '''    """Find connected components in the graph.
    Input: graph (str) — graph name.
    Output: dict with list of components and count."""
    g = _require_graph(graph)
    if g.is_directed():
        comps = list(nx.weakly_connected_components(g))
    else:
        comps = list(nx.connected_components(g))
    return {"components": [list(c) for c in comps], "count": len(comps)}'''),

    ("pagerank", "pagerank",
     "graph: str",
     '''    """Calculate PageRank for all nodes.
    Input: graph (str) — graph name.
    Output: dict mapping node -> PageRank value."""
    g = _require_graph(graph)
    return {"pagerank": dict(nx.pagerank(g))}'''),

    ("community_detection", "community_detection",
     "graph: str",
     '''    """Detect communities using Louvain method (greedy modularity).
    Input: graph (str) — graph name (undirected recommended).
    Output: dict with communities (list of sets) and modularity score."""
    from networkx.algorithms.community import greedy_modularity_communities
    g = _require_graph(graph)
    comms = list(greedy_modularity_communities(g))
    return {"communities": [list(c) for c in comms], "count": len(comms)}'''),

    # === Advanced ===
    ("clustering_coefficients", "clustering_coefficients",
     "graph: str",
     '''    """Calculate clustering coefficients for all nodes.
    Input: graph (str) — graph name.
    Output: dict mapping node -> clustering coefficient."""
    g = _require_graph(graph)
    return {"clustering": dict(nx.clustering(g))}'''),

    ("graph_statistics", "graph_statistics",
     "graph: str",
     '''    """Calculate comprehensive graph statistics.
    Input: graph (str) — graph name.
    Output: dict with density, diameter, degree stats, etc."""
    import numpy as np
    g = _require_graph(graph)
    info = {"nodes": g.number_of_nodes(), "edges": g.number_of_edges(),
            "directed": g.is_directed(), "density": nx.density(g)}
    degrees = [d for _, d in g.degree()]
    if degrees:
        info["degree_stats"] = {"min": int(np.min(degrees)), "max": int(np.max(degrees)),
                                "mean": float(np.mean(degrees)), "std": float(np.std(degrees))}
    if g.is_directed():
        info["is_dag"] = nx.is_directed_acyclic_graph(g)
    return info'''),

    ("minimum_spanning_tree", "minimum_spanning_tree",
     "graph: str, weight: str = 'weight', algorithm: str = 'kruskal'",
     '''    """Find minimum spanning tree of an undirected graph.
    Input: graph (str) — graph name. weight (str='weight') — edge weight attribute.
           algorithm (str='kruskal') — 'kruskal' or 'prim'.
    Output: dict with MST edges and total weight."""
    g = _require_graph(graph)
    if g.is_directed():
        raise ValueError("MST requires undirected graph")
    if algorithm == "prim":
        mst = nx.minimum_spanning_tree(g, weight=weight, algorithm="prim")
    else:
        mst = nx.minimum_spanning_tree(g, weight=weight, algorithm="kruskal")
    edges = [(u, v, g[u][v].get(weight, 1)) for u, v in mst.edges()]
    total = sum(w for _, _, w in edges)
    return {"edges": edges, "total_weight": total}'''),

    ("cycles_detection", "cycles_detection",
     "graph: str",
     '''    """Detect cycles in a graph.
    Input: graph (str) — graph name.
    Output: dict with cycle basis or DAG status."""
    g = _require_graph(graph)
    if g.is_directed():
        is_dag = nx.is_directed_acyclic_graph(g)
        return {"is_dag": is_dag, "message": "DAG: no cycles" if is_dag else "contains directed cycles"}
    cycles = list(nx.cycle_basis(g))
    return {"cycle_basis": cycles, "count": len(cycles)}'''),

    ("graph_coloring", "graph_coloring",
     "graph: str, strategy: str = 'largest_first'",
     '''    """Color graph vertices using greedy algorithm.
    Input: graph (str) — graph name. strategy (str='largest_first').
    Output: dict with node->color mapping and color count."""
    g = _require_graph(graph)
    coloring = nx.greedy_color(g, strategy=strategy)
    return {"coloring": coloring, "num_colors": max(coloring.values()) + 1 if coloring else 0}'''),

    ("centrality_measures", "centrality_measures",
     "graph: str, measures: list = None",
     '''    """Calculate multiple centrality measures.
    Input: graph (str) — graph name. measures (list, optional) — subset of:
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
    return result'''),

    ("matching", "matching",
     "graph: str, max_cardinality: bool = True",
     '''    """Find maximum weight matching in a graph.
    Input: graph (str) — graph name. max_cardinality (bool=True).
    Output: dict with matching edges and count."""
    g = _require_graph(graph)
    match = nx.max_weight_matching(g, maxcardinality=max_cardinality)
    return {"matching": list(match), "count": len(match)}'''),

    ("maximum_flow", "maximum_flow",
     "graph: str, source, sink, capacity: str = 'capacity'",
     '''    """Calculate maximum flow in a directed graph.
    Input: graph (str) — graph name. source — source node. sink — sink node.
           capacity (str='capacity') — edge attribute for capacity.
    Output: dict with flow value and per-edge flows."""
    g = _require_graph(graph)
    if not g.is_directed():
        raise ValueError("Maximum flow requires a directed graph")
    flow_val, flow_dict = nx.maximum_flow(g, source, sink, capacity=capacity)
    return {"flow_value": flow_val, "flow": {str(k): {str(k2): v2 for k2, v2 in v.items()} for k, v in flow_dict.items()}}'''),

    # === Graph Manipulation ===
    ("topological_sort", "topological_sort",
     "graph: str",
     '''    """Return a topological ordering of a directed acyclic graph.
    Input: graph (str) — graph name (must be a DAG).
    Output: dict with ordered node list."""
    g = _require_graph(graph)
    if not g.is_directed():
        raise ValueError("Topological sort requires a directed graph")
    if not nx.is_directed_acyclic_graph(g):
        raise ValueError("Graph contains cycles; topological sort requires a DAG")
    order = list(nx.topological_sort(g))
    return {"order": order, "count": len(order)}'''),

    ("subgraph", "subgraph",
     "graph: str, nodes: list, new_graph: str",
     '''    """Extract an induced subgraph and store as new graph.
    Input: graph (str) — source graph. nodes (list) — node subset.
           new_graph (str) — name for new subgraph.
    Output: dict with new graph summary."""
    g = _require_graph(graph)
    missing = [n for n in nodes if n not in g]
    if missing:
        raise ValueError(f"Nodes not found: {missing}")
    sub = g.subgraph(nodes).copy()
    gs = _get_graphs()
    if new_graph in gs:
        raise ValueError(f"Graph '{new_graph}' already exists")
    gs[new_graph] = sub
    return {"source": graph, "new_graph": new_graph,
            "nodes": sub.number_of_nodes(), "edges": sub.number_of_edges()}'''),

    ("merge_graphs", "merge_graphs",
     "graph_a: str, graph_b: str, new_graph: str",
     '''    """Compose two graphs into a new graph (union of nodes+edges).
    Input: graph_a (str), graph_b (str) — source graphs.
           new_graph (str) — name for composed graph.
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
            "edges": merged.number_of_edges(), "source_graphs": [graph_a, graph_b]}'''),

    # === I/O & Visualization ===
    ("visualize_graph", "visualize_graph",
     "graph: str, layout: str = 'spring'",
     '''    """Create a base64-encoded PNG visualization of the graph.
    Input: graph (str) — graph name. layout (str='spring') — 'spring','circular','kamada_kawai'.
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
            "format": "png", "layout": layout}'''),

    ("import_csv", "import_csv",
     "graph: str, csv_data: str, directed: bool = False",
     '''    """Import graph from CSV edge list (source,target per line).
    Input: graph (str) — new graph name. csv_data (str) — CSV text.
           directed (bool=False) — create DiGraph if True.
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
            "edges": g.number_of_edges(), "directed": directed}'''),

    ("export_json", "export_json",
     "graph: str",
     '''    """Export graph as JSON in node-link format.
    Input: graph (str) — graph name.
    Output: dict with node-link JSON data."""
    import json
    g = _require_graph(graph)
    data = nx.node_link_data(g, edges="links")
    return {"graph": graph, "data": data}'''),
]

def generate():
    os.makedirs(TARGET, exist_ok=True)
    for filename, func_name, params_str, body in tools:
        code = f'''"""Tool: {func_name} — NetworkX graph operation."""
import networkx as nx
from _helpers_nx import _get_graphs, _require_graph

def {func_name}({params_str}):
{body}
'''
        path = os.path.join(TARGET, f'{filename}.py')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f'  {filename}.py')
    print(f'\nTotal: {len(tools)} networkx tool files generated')

if __name__ == '__main__':
    generate()
