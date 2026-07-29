# added_networkx_L7 — MCP Server (subset for level L7)
from mcp.server.fastmcp import FastMCP

from community_detection import community_detection
from create_graph import create_graph
from get_info import get_info
from list_graphs import list_graphs
from matching import matching
from maximum_flow import maximum_flow
from minimum_spanning_tree import minimum_spanning_tree
from pagerank import pagerank
from remove_edges import remove_edges
from remove_nodes import remove_nodes
from cycles_detection import cycles_detection
from import_csv import import_csv
from delete_graph import delete_graph
from add_nodes import add_nodes
from export_json import export_json
from connected_components import connected_components
from visualize_graph import visualize_graph
from subgraph import subgraph
from add_edges import add_edges
from get_node_attributes import get_node_attributes
from graph_statistics import graph_statistics
from set_node_attributes import set_node_attributes
from get_neighbors import get_neighbors
from shortest_path import shortest_path
from centrality_measures import centrality_measures
from clustering_coefficients import clustering_coefficients
from merge_graphs import merge_graphs
from degree_centrality import degree_centrality
from graph_coloring import graph_coloring
from topological_sort import topological_sort
from betweenness_centrality import betweenness_centrality

mcp = FastMCP(name="added_networkx_L7")

mcp.add_tool(community_detection,
    name="community_detection",
    description="Tool: community_detection (from networkx server)."
)

mcp.add_tool(create_graph,
    name="create_graph",
    description="Tool: create_graph (from networkx server)."
)

mcp.add_tool(get_info,
    name="get_info",
    description="Tool: get_info (from networkx server)."
)

mcp.add_tool(list_graphs,
    name="list_graphs",
    description="Tool: list_graphs (from networkx server)."
)

mcp.add_tool(matching,
    name="matching",
    description="Tool: matching (from networkx server)."
)

mcp.add_tool(maximum_flow,
    name="maximum_flow",
    description="Tool: maximum_flow (from networkx server)."
)

mcp.add_tool(minimum_spanning_tree,
    name="minimum_spanning_tree",
    description="Tool: minimum_spanning_tree (from networkx server)."
)

mcp.add_tool(pagerank,
    name="pagerank",
    description="Tool: pagerank (from networkx server)."
)

mcp.add_tool(remove_edges,
    name="remove_edges",
    description="Tool: remove_edges (from networkx server)."
)

mcp.add_tool(remove_nodes,
    name="remove_nodes",
    description="Tool: remove_nodes (from networkx server)."
)

mcp.add_tool(cycles_detection,
    name="cycles_detection",
    description="Tool: cycles_detection (from networkx server)."
)

mcp.add_tool(import_csv,
    name="import_csv",
    description="Tool: import_csv (from networkx server)."
)

mcp.add_tool(delete_graph,
    name="delete_graph",
    description="Tool: delete_graph (from networkx server)."
)

mcp.add_tool(add_nodes,
    name="add_nodes",
    description="Tool: add_nodes (from networkx server)."
)

mcp.add_tool(export_json,
    name="export_json",
    description="Tool: export_json (from networkx server)."
)

mcp.add_tool(connected_components,
    name="connected_components",
    description="Tool: connected_components (from networkx server)."
)

mcp.add_tool(visualize_graph,
    name="visualize_graph",
    description="Tool: visualize_graph (from networkx server)."
)

mcp.add_tool(subgraph,
    name="subgraph",
    description="Tool: subgraph (from networkx server)."
)

mcp.add_tool(add_edges,
    name="add_edges",
    description="Tool: add_edges (from networkx server)."
)

mcp.add_tool(get_node_attributes,
    name="get_node_attributes",
    description="Tool: get_node_attributes (from networkx server)."
)

mcp.add_tool(graph_statistics,
    name="graph_statistics",
    description="Tool: graph_statistics (from networkx server)."
)

mcp.add_tool(set_node_attributes,
    name="set_node_attributes",
    description="Tool: set_node_attributes (from networkx server)."
)

mcp.add_tool(get_neighbors,
    name="get_neighbors",
    description="Tool: get_neighbors (from networkx server)."
)

mcp.add_tool(shortest_path,
    name="shortest_path",
    description="Tool: shortest_path (from networkx server)."
)

mcp.add_tool(centrality_measures,
    name="centrality_measures",
    description="Tool: centrality_measures (from networkx server)."
)

mcp.add_tool(clustering_coefficients,
    name="clustering_coefficients",
    description="Tool: clustering_coefficients (from networkx server)."
)

mcp.add_tool(merge_graphs,
    name="merge_graphs",
    description="Tool: merge_graphs (from networkx server)."
)

mcp.add_tool(degree_centrality,
    name="degree_centrality",
    description="Tool: degree_centrality (from networkx server)."
)

mcp.add_tool(graph_coloring,
    name="graph_coloring",
    description="Tool: graph_coloring (from networkx server)."
)

mcp.add_tool(topological_sort,
    name="topological_sort",
    description="Tool: topological_sort (from networkx server)."
)

mcp.add_tool(betweenness_centrality,
    name="betweenness_centrality",
    description="Tool: betweenness_centrality (from networkx server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
