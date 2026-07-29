# added_gis_visualize_L1 — MCP Server (subset for level L1)
from mcp.server.fastmcp import FastMCP

from create_map import create_map
from create_web_map import create_web_map

mcp = FastMCP(name="added_gis_visualize_L1")

mcp.add_tool(create_map,
    name="create_map",
    description="Tool: create_map (from gis visualize server)."
)

mcp.add_tool(create_web_map,
    name="create_web_map",
    description="Tool: create_web_map (from gis visualize server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
