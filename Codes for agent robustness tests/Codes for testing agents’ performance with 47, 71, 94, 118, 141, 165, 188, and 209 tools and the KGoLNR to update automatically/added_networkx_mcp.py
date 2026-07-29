# added_networkx_mcp — MCP Server
# Auto-generated from tools_networkx/ individual tool files

from mcp.server.fastmcp import FastMCP

from add_edges import add_edges
from add_nodes import add_nodes
from betweenness_centrality import betweenness_centrality
from centrality_measures import centrality_measures
from clustering_coefficients import clustering_coefficients
from community_detection import community_detection
from connected_components import connected_components
from create_graph import create_graph
from cycles_detection import cycles_detection
from degree_centrality import degree_centrality
from delete_graph import delete_graph
from export_json import export_json
from get_info import get_info
from get_neighbors import get_neighbors
from get_node_attributes import get_node_attributes
from graph_coloring import graph_coloring
from graph_statistics import graph_statistics
from import_csv import import_csv
from list_graphs import list_graphs
from matching import matching
from maximum_flow import maximum_flow
from merge_graphs import merge_graphs
from minimum_spanning_tree import minimum_spanning_tree
from pagerank import pagerank
from remove_edges import remove_edges
from remove_nodes import remove_nodes
from set_node_attributes import set_node_attributes
from shortest_path import shortest_path
from subgraph import subgraph
from topological_sort import topological_sort
from visualize_graph import visualize_graph

mcp = FastMCP(name="added_networkx_mcp")

mcp.add_tool(add_edges,
    name="add_edges",
    description="Add edges to an existing graph."
)

mcp.add_tool(add_nodes,
    name="add_nodes",
    description="Add nodes to an existing graph."
)

mcp.add_tool(betweenness_centrality,
    name="betweenness_centrality",
    description="Calculate betweenness centrality for all nodes."
)

mcp.add_tool(centrality_measures,
    name="centrality_measures",
    description="Calculate multiple centrality measures (degree/betweenness/closeness/eigenvector)."
)

mcp.add_tool(clustering_coefficients,
    name="clustering_coefficients",
    description="Calculate clustering coefficients for all nodes."
)

mcp.add_tool(community_detection,
    name="community_detection",
    description="Detect communities using Louvain (greedy modularity) method."
)

mcp.add_tool(connected_components,
    name="connected_components",
    description="Find connected components in the graph."
)

mcp.add_tool(create_graph,
    name="create_graph",
    description="Create a new graph (undirected or directed)."
)

mcp.add_tool(cycles_detection,
    name="cycles_detection",
    description="Detect cycles: cycle basis for undirected, DAG check for directed."
)

mcp.add_tool(degree_centrality,
    name="degree_centrality",
    description="Calculate degree centrality for all nodes."
)

mcp.add_tool(delete_graph,
    name="delete_graph",
    description="Delete a graph from storage."
)

mcp.add_tool(export_json,
    name="export_json",
    description="Export graph as JSON in node-link format."
)

mcp.add_tool(get_info,
    name="get_info",
    description="Get basic graph information (nodes, edges, directed)."
)

mcp.add_tool(get_neighbors,
    name="get_neighbors",
    description="Get all neighbors of a node."
)

mcp.add_tool(get_node_attributes,
    name="get_node_attributes",
    description="Get all attributes of a specific node."
)

mcp.add_tool(graph_coloring,
    name="graph_coloring",
    description="Color graph vertices using greedy algorithm."
)

mcp.add_tool(graph_statistics,
    name="graph_statistics",
    description="Calculate comprehensive graph statistics (density, diameter, degree distribution)."
)

mcp.add_tool(import_csv,
    name="import_csv",
    description="Import graph from CSV edge list (source,target per line)."
)

mcp.add_tool(list_graphs,
    name="list_graphs",
    description="List all stored graphs with summary info."
)

mcp.add_tool(matching,
    name="matching",
    description="Find maximum weight matching in a graph."
)

mcp.add_tool(maximum_flow,
    name="maximum_flow",
    description="Calculate maximum flow in a directed graph."
)

mcp.add_tool(merge_graphs,
    name="merge_graphs",
    description="Compose two graphs into a new graph (union of nodes and edges)."
)

mcp.add_tool(minimum_spanning_tree,
    name="minimum_spanning_tree",
    description="Find minimum spanning tree of an undirected graph."
)

mcp.add_tool(pagerank,
    name="pagerank",
    description="Calculate PageRank for all nodes."
)

mcp.add_tool(remove_edges,
    name="remove_edges",
    description="Remove edges from a graph."
)

mcp.add_tool(remove_nodes,
    name="remove_nodes",
    description="Remove nodes from a graph."
)

mcp.add_tool(set_node_attributes,
    name="set_node_attributes",
    description="Set attributes on one or more nodes."
)

mcp.add_tool(shortest_path,
    name="shortest_path",
    description="Find shortest path between two nodes using BFS/Dijkstra."
)

mcp.add_tool(subgraph,
    name="subgraph",
    description="Extract an induced subgraph and store as a new graph."
)

mcp.add_tool(topological_sort,
    name="topological_sort",
    description="Return a topological ordering of a directed acyclic graph."
)

mcp.add_tool(visualize_graph,
    name="visualize_graph",
    description="Create a base64-encoded PNG visualization of the graph."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
