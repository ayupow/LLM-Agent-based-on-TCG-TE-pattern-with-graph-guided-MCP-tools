# added_networkx_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from betweenness_centrality import betweenness_centrality
from degree_centrality import degree_centrality
from export_json import export_json
from list_graphs import list_graphs
from maximum_flow import maximum_flow
from set_node_attributes import set_node_attributes
from subgraph import subgraph
from topological_sort import topological_sort
from visualize_graph import visualize_graph

mcp = FastMCP(name="added_networkx_L3")

mcp.add_tool(betweenness_centrality,
    name="betweenness_centrality",
    description="Tool: betweenness_centrality (from networkx server)."
)

mcp.add_tool(degree_centrality,
    name="degree_centrality",
    description="Tool: degree_centrality (from networkx server)."
)

mcp.add_tool(export_json,
    name="export_json",
    description="Tool: export_json (from networkx server)."
)

mcp.add_tool(list_graphs,
    name="list_graphs",
    description="Tool: list_graphs (from networkx server)."
)

mcp.add_tool(maximum_flow,
    name="maximum_flow",
    description="Tool: maximum_flow (from networkx server)."
)

mcp.add_tool(set_node_attributes,
    name="set_node_attributes",
    description="Tool: set_node_attributes (from networkx server)."
)

mcp.add_tool(subgraph,
    name="subgraph",
    description="Tool: subgraph (from networkx server)."
)

mcp.add_tool(topological_sort,
    name="topological_sort",
    description="Tool: topological_sort (from networkx server)."
)

mcp.add_tool(visualize_graph,
    name="visualize_graph",
    description="Tool: visualize_graph (from networkx server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
