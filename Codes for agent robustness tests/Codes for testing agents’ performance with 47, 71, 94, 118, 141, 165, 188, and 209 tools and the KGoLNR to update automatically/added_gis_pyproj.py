# added_gis_pyproj — MCP Server
# Auto-generated from tools_gis_pyproj/ individual tool files

from mcp.server.fastmcp import FastMCP

from calculate_geodetic_area import calculate_geodetic_area
from calculate_geodetic_distance import calculate_geodetic_distance
from calculate_geodetic_point import calculate_geodetic_point
from get_available_crs import get_available_crs
from get_crs_info import get_crs_info
from get_geocentric_crs import get_geocentric_crs
from get_geod_info import get_geod_info
from get_utm_crs import get_utm_crs
from get_utm_zone import get_utm_zone
from project_geometry import project_geometry
from transform_coordinates import transform_coordinates

mcp = FastMCP(name="added_gis_pyproj")

mcp.add_tool(calculate_geodetic_area,
    name="calculate_geodetic_area",
    description="Calculate geodesic area of a polygon on the Earth's surface."
)

mcp.add_tool(calculate_geodetic_distance,
    name="calculate_geodetic_distance",
    description="Calculate geodetic (great-circle) distance between two points."
)

mcp.add_tool(calculate_geodetic_point,
    name="calculate_geodetic_point",
    description="Calculate destination point given start, azimuth, and distance."
)

mcp.add_tool(get_available_crs,
    name="get_available_crs",
    description="Get the list of available coordinate reference systems."
)

mcp.add_tool(get_crs_info,
    name="get_crs_info",
    description="Get detailed information about a coordinate reference system."
)

mcp.add_tool(get_geocentric_crs,
    name="get_geocentric_crs",
    description="Get geocentric CRS (ECEF) for given coordinates."
)

mcp.add_tool(get_geod_info,
    name="get_geod_info",
    description="Get information about a geodetic ellipsoid."
)

mcp.add_tool(get_utm_crs,
    name="get_utm_crs",
    description="Get UTM CRS string for given coordinates."
)

mcp.add_tool(get_utm_zone,
    name="get_utm_zone",
    description="Get UTM zone number and letter for given coordinates."
)

mcp.add_tool(project_geometry,
    name="project_geometry",
    description="Project a geometry from one CRS to another."
)

mcp.add_tool(transform_coordinates,
    name="transform_coordinates",
    description="Transform coordinates between two coordinate reference systems (CRS)."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
