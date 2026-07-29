# added_gis_shapely_L5 — MCP Server (subset for level L5)
from mcp.server.fastmcp import FastMCP

from buffer import buffer
from convex_hull import convex_hull
from envelope import envelope
from geometry_to_geojson import geometry_to_geojson
from get_area import get_area
from get_length import get_length
from intersection import intersection
from is_valid import is_valid
from minimum_rotated_rectangle import minimum_rotated_rectangle
from nearest_point_on_geometry import nearest_point_on_geometry
from rotate_geometry import rotate_geometry
from simplify import simplify
from translate_geometry import translate_geometry
from triangulate_geometry import triangulate_geometry
from unary_union_geometries import unary_union_geometries
from voronoi import voronoi

mcp = FastMCP(name="added_gis_shapely_L5")

mcp.add_tool(buffer,
    name="buffer",
    description="Tool: buffer (from gis shapely server)."
)

mcp.add_tool(convex_hull,
    name="convex_hull",
    description="Tool: convex_hull (from gis shapely server)."
)

mcp.add_tool(envelope,
    name="envelope",
    description="Tool: envelope (from gis shapely server)."
)

mcp.add_tool(geometry_to_geojson,
    name="geometry_to_geojson",
    description="Tool: geometry_to_geojson (from gis shapely server)."
)

mcp.add_tool(get_area,
    name="get_area",
    description="Tool: get_area (from gis shapely server)."
)

mcp.add_tool(get_length,
    name="get_length",
    description="Tool: get_length (from gis shapely server)."
)

mcp.add_tool(intersection,
    name="intersection",
    description="Tool: intersection (from gis shapely server)."
)

mcp.add_tool(is_valid,
    name="is_valid",
    description="Tool: is_valid (from gis shapely server)."
)

mcp.add_tool(minimum_rotated_rectangle,
    name="minimum_rotated_rectangle",
    description="Tool: minimum_rotated_rectangle (from gis shapely server)."
)

mcp.add_tool(nearest_point_on_geometry,
    name="nearest_point_on_geometry",
    description="Tool: nearest_point_on_geometry (from gis shapely server)."
)

mcp.add_tool(rotate_geometry,
    name="rotate_geometry",
    description="Tool: rotate_geometry (from gis shapely server)."
)

mcp.add_tool(simplify,
    name="simplify",
    description="Tool: simplify (from gis shapely server)."
)

mcp.add_tool(translate_geometry,
    name="translate_geometry",
    description="Tool: translate_geometry (from gis shapely server)."
)

mcp.add_tool(triangulate_geometry,
    name="triangulate_geometry",
    description="Tool: triangulate_geometry (from gis shapely server)."
)

mcp.add_tool(unary_union_geometries,
    name="unary_union_geometries",
    description="Tool: unary_union_geometries (from gis shapely server)."
)

mcp.add_tool(voronoi,
    name="voronoi",
    description="Tool: voronoi (from gis shapely server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
