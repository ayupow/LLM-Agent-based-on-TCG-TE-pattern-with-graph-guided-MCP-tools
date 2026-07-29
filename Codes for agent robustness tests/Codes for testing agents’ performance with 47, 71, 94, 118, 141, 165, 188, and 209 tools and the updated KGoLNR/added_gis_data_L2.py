# added_gis_data_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from download_climate_data import download_climate_data
from download_worldcover import download_worldcover

mcp = FastMCP(name="added_gis_data_L2")

mcp.add_tool(download_climate_data,
    name="download_climate_data",
    description="Tool: download_climate_data (from gis data server)."
)

mcp.add_tool(download_worldcover,
    name="download_worldcover",
    description="Tool: download_worldcover (from gis data server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
