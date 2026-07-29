# added_gis_data_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from compute_s2_ndvi import compute_s2_ndvi
from download_satellite_imagery import download_satellite_imagery
from download_street_network import download_street_network
from download_worldcover import download_worldcover

mcp = FastMCP(name="added_gis_data_L4")

mcp.add_tool(compute_s2_ndvi,
    name="compute_s2_ndvi",
    description="Tool: compute_s2_ndvi (from gis data server)."
)

mcp.add_tool(download_satellite_imagery,
    name="download_satellite_imagery",
    description="Tool: download_satellite_imagery (from gis data server)."
)

mcp.add_tool(download_street_network,
    name="download_street_network",
    description="Tool: download_street_network (from gis data server)."
)

mcp.add_tool(download_worldcover,
    name="download_worldcover",
    description="Tool: download_worldcover (from gis data server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
