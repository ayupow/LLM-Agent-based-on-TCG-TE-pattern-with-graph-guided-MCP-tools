# added_gis_data — MCP Server
# Auto-generated from tools_gis_data/ individual tool files

from mcp.server.fastmcp import FastMCP

from calculate_shortest_path import calculate_shortest_path
from compute_s2_ndvi import compute_s2_ndvi
from download_boundaries import download_boundaries
from download_climate_data import download_climate_data
from download_satellite_imagery import download_satellite_imagery
from download_species_occurrences import download_species_occurrences
from download_street_network import download_street_network
from download_worldcover import download_worldcover
from get_species_info import get_species_info

mcp = FastMCP(name="added_gis_data")

mcp.add_tool(calculate_shortest_path,
    name="calculate_shortest_path",
    description="Calculate shortest path between two points on a street network."
)

mcp.add_tool(compute_s2_ndvi,
    name="compute_s2_ndvi",
    description="Compute Sentinel-2 NDVI on-demand from Microsoft Planetary Computer."
)

mcp.add_tool(download_boundaries,
    name="download_boundaries",
    description="Download administrative boundary data for a region from OSM/geoboundaries."
)

mcp.add_tool(download_climate_data,
    name="download_climate_data",
    description="Download climate data (temperature, precipitation) from WorldClim/ERA5."
)

mcp.add_tool(download_satellite_imagery,
    name="download_satellite_imagery",
    description="Download analysis-ready satellite imagery from Planetary Computer (STAC+SAS)."
)

mcp.add_tool(download_species_occurrences,
    name="download_species_occurrences",
    description="Download species occurrence records from GBIF."
)

mcp.add_tool(download_street_network,
    name="download_street_network",
    description="Download street network for a place using osmnx."
)

mcp.add_tool(download_worldcover,
    name="download_worldcover",
    description="Download ESA WorldCover land cover classification data."
)

mcp.add_tool(get_species_info,
    name="get_species_info",
    description="Get taxonomic and ecological info about a species from GBIF."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
