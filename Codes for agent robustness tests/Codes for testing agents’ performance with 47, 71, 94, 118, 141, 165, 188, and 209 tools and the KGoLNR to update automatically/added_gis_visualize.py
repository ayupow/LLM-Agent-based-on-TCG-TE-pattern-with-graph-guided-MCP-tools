# added_gis_visualize — MCP Server
# Auto-generated from tools_gis_visualize/ individual tool files

from mcp.server.fastmcp import FastMCP

from create_map import create_map
from create_web_map import create_web_map

mcp = FastMCP(name="added_gis_visualize")

mcp.add_tool(create_map,
    name="create_map",
    description="Create a static map visualization from geospatial data (PNG/HTML)."
)

mcp.add_tool(create_web_map,
    name="create_web_map",
    description="Create an interactive web map using folium/leaflet (HTML)."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
