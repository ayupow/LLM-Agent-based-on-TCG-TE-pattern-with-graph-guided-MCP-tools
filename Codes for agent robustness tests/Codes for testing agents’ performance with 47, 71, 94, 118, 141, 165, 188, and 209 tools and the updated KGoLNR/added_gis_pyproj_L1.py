# added_gis_pyproj_L1 — MCP Server (subset for level L1)
from mcp.server.fastmcp import FastMCP

from calculate_geodetic_area import calculate_geodetic_area
from calculate_geodetic_distance import calculate_geodetic_distance
from get_utm_crs import get_utm_crs
from get_utm_zone import get_utm_zone
from project_geometry import project_geometry
from transform_coordinates import transform_coordinates

mcp = FastMCP(name="added_gis_pyproj_L1")

mcp.add_tool(calculate_geodetic_area,
    name="calculate_geodetic_area",
    description="Tool: calculate_geodetic_area (from gis pyproj server)."
)

mcp.add_tool(calculate_geodetic_distance,
    name="calculate_geodetic_distance",
    description="Tool: calculate_geodetic_distance (from gis pyproj server)."
)

mcp.add_tool(get_utm_crs,
    name="get_utm_crs",
    description="Tool: get_utm_crs (from gis pyproj server)."
)

mcp.add_tool(get_utm_zone,
    name="get_utm_zone",
    description="Tool: get_utm_zone (from gis pyproj server)."
)

mcp.add_tool(project_geometry,
    name="project_geometry",
    description="Tool: project_geometry (from gis pyproj server)."
)

mcp.add_tool(transform_coordinates,
    name="transform_coordinates",
    description="Tool: transform_coordinates (from gis pyproj server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
