# added_gis_pyproj_L5 — MCP Server (subset for level L5)
from mcp.server.fastmcp import FastMCP

from calculate_geodetic_area import calculate_geodetic_area
from get_available_crs import get_available_crs
from get_utm_zone import get_utm_zone
from project_geometry import project_geometry

mcp = FastMCP(name="added_gis_pyproj_L5")

mcp.add_tool(calculate_geodetic_area,
    name="calculate_geodetic_area",
    description="Tool: calculate_geodetic_area (from gis pyproj server)."
)

mcp.add_tool(get_available_crs,
    name="get_available_crs",
    description="Tool: get_available_crs (from gis pyproj server)."
)

mcp.add_tool(get_utm_zone,
    name="get_utm_zone",
    description="Tool: get_utm_zone (from gis pyproj server)."
)

mcp.add_tool(project_geometry,
    name="project_geometry",
    description="Tool: project_geometry (from gis pyproj server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
