# added_networkx_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from connected_components import connected_components
from create_graph import create_graph
from get_neighbors import get_neighbors
from get_node_attributes import get_node_attributes
from graph_coloring import graph_coloring
from matching import matching
from merge_graphs import merge_graphs
from minimum_spanning_tree import minimum_spanning_tree
from pagerank import pagerank
from set_node_attributes import set_node_attributes
from subgraph import subgraph

mcp = FastMCP(name="added_networkx_L4")

mcp.add_tool(connected_components,
    name="connected_components",
    description="Tool: connected_components (from networkx server)."
)

mcp.add_tool(create_graph,
    name="create_graph",
    description="Tool: create_graph (from networkx server)."
)

mcp.add_tool(get_neighbors,
    name="get_neighbors",
    description="Tool: get_neighbors (from networkx server)."
)

mcp.add_tool(get_node_attributes,
    name="get_node_attributes",
    description="Tool: get_node_attributes (from networkx server)."
)

mcp.add_tool(graph_coloring,
    name="graph_coloring",
    description="Tool: graph_coloring (from networkx server)."
)

mcp.add_tool(matching,
    name="matching",
    description="Tool: matching (from networkx server)."
)

mcp.add_tool(merge_graphs,
    name="merge_graphs",
    description="Tool: merge_graphs (from networkx server)."
)

mcp.add_tool(minimum_spanning_tree,
    name="minimum_spanning_tree",
    description="Tool: minimum_spanning_tree (from networkx server)."
)

mcp.add_tool(pagerank,
    name="pagerank",
    description="Tool: pagerank (from networkx server)."
)

mcp.add_tool(set_node_attributes,
    name="set_node_attributes",
    description="Tool: set_node_attributes (from networkx server)."
)

mcp.add_tool(subgraph,
    name="subgraph",
    description="Tool: subgraph (from networkx server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
