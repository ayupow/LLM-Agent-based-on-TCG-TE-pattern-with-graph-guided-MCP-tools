# added_gis_visualize_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from create_web_map import create_web_map

mcp = FastMCP(name="added_gis_visualize_L3")

mcp.add_tool(create_web_map,
    name="create_web_map",
    description="Tool: create_web_map (from gis visualize server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
