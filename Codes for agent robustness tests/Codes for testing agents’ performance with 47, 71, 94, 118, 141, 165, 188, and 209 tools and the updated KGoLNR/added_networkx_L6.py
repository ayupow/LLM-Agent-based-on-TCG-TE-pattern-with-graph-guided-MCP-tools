# added_networkx_L6 — MCP Server (subset for level L6)
from mcp.server.fastmcp import FastMCP

from betweenness_centrality import betweenness_centrality
from cycles_detection import cycles_detection
from pagerank import pagerank
from set_node_attributes import set_node_attributes
from visualize_graph import visualize_graph
from get_info import get_info
from shortest_path import shortest_path
from remove_nodes import remove_nodes
from remove_edges import remove_edges
from matching import matching

mcp = FastMCP(name="added_networkx_L6")

mcp.add_tool(betweenness_centrality,
    name="betweenness_centrality",
    description="Tool: betweenness_centrality (from networkx server)."
)

mcp.add_tool(cycles_detection,
    name="cycles_detection",
    description="Tool: cycles_detection (from networkx server)."
)

mcp.add_tool(pagerank,
    name="pagerank",
    description="Tool: pagerank (from networkx server)."
)

mcp.add_tool(set_node_attributes,
    name="set_node_attributes",
    description="Tool: set_node_attributes (from networkx server)."
)

mcp.add_tool(visualize_graph,
    name="visualize_graph",
    description="Tool: visualize_graph (from networkx server)."
)

mcp.add_tool(get_info,
    name="get_info",
    description="Tool: get_info (from networkx server)."
)

mcp.add_tool(shortest_path,
    name="shortest_path",
    description="Tool: shortest_path (from networkx server)."
)

mcp.add_tool(remove_nodes,
    name="remove_nodes",
    description="Tool: remove_nodes (from networkx server)."
)

mcp.add_tool(remove_edges,
    name="remove_edges",
    description="Tool: remove_edges (from networkx server)."
)

mcp.add_tool(matching,
    name="matching",
    description="Tool: matching (from networkx server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
