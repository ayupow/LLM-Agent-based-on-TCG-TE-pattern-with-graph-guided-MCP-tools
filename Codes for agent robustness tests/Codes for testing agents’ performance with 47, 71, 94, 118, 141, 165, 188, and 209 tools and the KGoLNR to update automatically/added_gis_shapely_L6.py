# added_gis_shapely_L6 — MCP Server (subset for level L6)
from mcp.server.fastmcp import FastMCP

from convex_hull import convex_hull
from geojson_to_geometry import geojson_to_geometry
from geometry_to_geojson import geometry_to_geojson
from get_bounds import get_bounds
from get_centroid import get_centroid
from get_geometry_type import get_geometry_type
from get_length import get_length
from is_valid import is_valid
from make_valid import make_valid
from minimum_rotated_rectangle import minimum_rotated_rectangle
from nearest_point_on_geometry import nearest_point_on_geometry
from normalize_geometry import normalize_geometry
from scale_geometry import scale_geometry
from simplify import simplify
from translate_geometry import translate_geometry
from triangulate_geometry import triangulate_geometry
from unary_union_geometries import unary_union_geometries
from voronoi import voronoi
from buffer import buffer
from union import union
from envelope import envelope
from symmetric_difference import symmetric_difference
from intersection import intersection
from snap_geometry import snap_geometry
from get_coordinates import get_coordinates
from rotate_geometry import rotate_geometry
from difference import difference
from get_area import get_area

mcp = FastMCP(name="added_gis_shapely_L6")

mcp.add_tool(convex_hull,
    name="convex_hull",
    description="Tool: convex_hull (from gis shapely server)."
)

mcp.add_tool(geojson_to_geometry,
    name="geojson_to_geometry",
    description="Tool: geojson_to_geometry (from gis shapely server)."
)

mcp.add_tool(geometry_to_geojson,
    name="geometry_to_geojson",
    description="Tool: geometry_to_geojson (from gis shapely server)."
)

mcp.add_tool(get_bounds,
    name="get_bounds",
    description="Tool: get_bounds (from gis shapely server)."
)

mcp.add_tool(get_centroid,
    name="get_centroid",
    description="Tool: get_centroid (from gis shapely server)."
)

mcp.add_tool(get_geometry_type,
    name="get_geometry_type",
    description="Tool: get_geometry_type (from gis shapely server)."
)

mcp.add_tool(get_length,
    name="get_length",
    description="Tool: get_length (from gis shapely server)."
)

mcp.add_tool(is_valid,
    name="is_valid",
    description="Tool: is_valid (from gis shapely server)."
)

mcp.add_tool(make_valid,
    name="make_valid",
    description="Tool: make_valid (from gis shapely server)."
)

mcp.add_tool(minimum_rotated_rectangle,
    name="minimum_rotated_rectangle",
    description="Tool: minimum_rotated_rectangle (from gis shapely server)."
)

mcp.add_tool(nearest_point_on_geometry,
    name="nearest_point_on_geometry",
    description="Tool: nearest_point_on_geometry (from gis shapely server)."
)

mcp.add_tool(normalize_geometry,
    name="normalize_geometry",
    description="Tool: normalize_geometry (from gis shapely server)."
)

mcp.add_tool(scale_geometry,
    name="scale_geometry",
    description="Tool: scale_geometry (from gis shapely server)."
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

mcp.add_tool(buffer,
    name="buffer",
    description="Tool: buffer (from gis shapely server)."
)

mcp.add_tool(union,
    name="union",
    description="Tool: union (from gis shapely server)."
)

mcp.add_tool(envelope,
    name="envelope",
    description="Tool: envelope (from gis shapely server)."
)

mcp.add_tool(symmetric_difference,
    name="symmetric_difference",
    description="Tool: symmetric_difference (from gis shapely server)."
)

mcp.add_tool(intersection,
    name="intersection",
    description="Tool: intersection (from gis shapely server)."
)

mcp.add_tool(snap_geometry,
    name="snap_geometry",
    description="Tool: snap_geometry (from gis shapely server)."
)

mcp.add_tool(get_coordinates,
    name="get_coordinates",
    description="Tool: get_coordinates (from gis shapely server)."
)

mcp.add_tool(rotate_geometry,
    name="rotate_geometry",
    description="Tool: rotate_geometry (from gis shapely server)."
)

mcp.add_tool(difference,
    name="difference",
    description="Tool: difference (from gis shapely server)."
)

mcp.add_tool(get_area,
    name="get_area",
    description="Tool: get_area (from gis shapely server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
