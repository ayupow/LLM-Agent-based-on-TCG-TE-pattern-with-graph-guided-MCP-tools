# added_gis_data_L5 — MCP Server (subset for level L5)
from mcp.server.fastmcp import FastMCP

from calculate_shortest_path import calculate_shortest_path
from compute_s2_ndvi import compute_s2_ndvi
from download_boundaries import download_boundaries
from download_satellite_imagery import download_satellite_imagery
from download_species_occurrences import download_species_occurrences
from get_species_info import get_species_info
from download_worldcover import download_worldcover
from download_street_network import download_street_network
from download_climate_data import download_climate_data

mcp = FastMCP(name="added_gis_data_L5")

mcp.add_tool(calculate_shortest_path,
    name="calculate_shortest_path",
    description="Tool: calculate_shortest_path (from gis data server)."
)

mcp.add_tool(compute_s2_ndvi,
    name="compute_s2_ndvi",
    description="Tool: compute_s2_ndvi (from gis data server)."
)

mcp.add_tool(download_boundaries,
    name="download_boundaries",
    description="Tool: download_boundaries (from gis data server)."
)

mcp.add_tool(download_satellite_imagery,
    name="download_satellite_imagery",
    description="Tool: download_satellite_imagery (from gis data server)."
)

mcp.add_tool(download_species_occurrences,
    name="download_species_occurrences",
    description="Tool: download_species_occurrences (from gis data server)."
)

mcp.add_tool(get_species_info,
    name="get_species_info",
    description="Tool: get_species_info (from gis data server)."
)

mcp.add_tool(download_worldcover,
    name="download_worldcover",
    description="Tool: download_worldcover (from gis data server)."
)

mcp.add_tool(download_street_network,
    name="download_street_network",
    description="Tool: download_street_network (from gis data server)."
)

mcp.add_tool(download_climate_data,
    name="download_climate_data",
    description="Tool: download_climate_data (from gis data server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
