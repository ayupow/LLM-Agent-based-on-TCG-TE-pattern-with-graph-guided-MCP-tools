# added_gis_pyproj_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from calculate_geodetic_area import calculate_geodetic_area
from calculate_geodetic_distance import calculate_geodetic_distance
from calculate_geodetic_point import calculate_geodetic_point
from get_geod_info import get_geod_info
from get_utm_crs import get_utm_crs
from project_geometry import project_geometry

mcp = FastMCP(name="added_gis_pyproj_L2")

mcp.add_tool(calculate_geodetic_area,
    name="calculate_geodetic_area",
    description="Tool: calculate_geodetic_area (from gis pyproj server)."
)

mcp.add_tool(calculate_geodetic_distance,
    name="calculate_geodetic_distance",
    description="Tool: calculate_geodetic_distance (from gis pyproj server)."
)

mcp.add_tool(calculate_geodetic_point,
    name="calculate_geodetic_point",
    description="Tool: calculate_geodetic_point (from gis pyproj server)."
)

mcp.add_tool(get_geod_info,
    name="get_geod_info",
    description="Tool: get_geod_info (from gis pyproj server)."
)

mcp.add_tool(get_utm_crs,
    name="get_utm_crs",
    description="Tool: get_utm_crs (from gis pyproj server)."
)

mcp.add_tool(project_geometry,
    name="project_geometry",
    description="Tool: project_geometry (from gis pyproj server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
