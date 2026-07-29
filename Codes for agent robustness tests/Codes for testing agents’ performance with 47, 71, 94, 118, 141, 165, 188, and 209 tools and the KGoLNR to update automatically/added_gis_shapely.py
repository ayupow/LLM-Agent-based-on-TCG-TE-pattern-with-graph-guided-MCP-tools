# added_gis_shapely — MCP Server
# Auto-generated from tools_gis_shapely/ individual tool files

from mcp.server.fastmcp import FastMCP

from buffer import buffer
from convex_hull import convex_hull
from difference import difference
from envelope import envelope
from geojson_to_geometry import geojson_to_geometry
from geometry_to_geojson import geometry_to_geojson
from get_area import get_area
from get_bounds import get_bounds
from get_centroid import get_centroid
from get_coordinates import get_coordinates
from get_geometry_type import get_geometry_type
from get_length import get_length
from intersection import intersection
from is_valid import is_valid
from make_valid import make_valid
from minimum_rotated_rectangle import minimum_rotated_rectangle
from nearest_point_on_geometry import nearest_point_on_geometry
from normalize_geometry import normalize_geometry
from rotate_geometry import rotate_geometry
from scale_geometry import scale_geometry
from simplify import simplify
from snap_geometry import snap_geometry
from symmetric_difference import symmetric_difference
from translate_geometry import translate_geometry
from triangulate_geometry import triangulate_geometry
from unary_union_geometries import unary_union_geometries
from union import union
from voronoi import voronoi

mcp = FastMCP(name="added_gis_shapely")

mcp.add_tool(buffer,
    name="buffer",
    description="Create a buffer around a geometry at a given distance."
)

mcp.add_tool(convex_hull,
    name="convex_hull",
    description="Calculate the convex hull of a geometry."
)

mcp.add_tool(difference,
    name="difference",
    description="Find the difference between two geometries (geometry1 minus geometry2)."
)

mcp.add_tool(envelope,
    name="envelope",
    description="Get the bounding box (envelope) of a geometry."
)

mcp.add_tool(geojson_to_geometry,
    name="geojson_to_geometry",
    description="Convert a GeoJSON geometry to WKT format."
)

mcp.add_tool(geometry_to_geojson,
    name="geometry_to_geojson",
    description="Convert a WKT geometry to GeoJSON format."
)

mcp.add_tool(get_area,
    name="get_area",
    description="Get the area of a geometry."
)

mcp.add_tool(get_bounds,
    name="get_bounds",
    description="Get the bounds (minx, miny, maxx, maxy) of a geometry."
)

mcp.add_tool(get_centroid,
    name="get_centroid",
    description="Get the centroid (center of mass) of a geometry."
)

mcp.add_tool(get_coordinates,
    name="get_coordinates",
    description="Get all coordinates of a geometry."
)

mcp.add_tool(get_geometry_type,
    name="get_geometry_type",
    description="Get the type of a geometry (Point, LineString, Polygon, etc.)."
)

mcp.add_tool(get_length,
    name="get_length",
    description="Get the length of a geometry (perimeter for polygons)."
)

mcp.add_tool(intersection,
    name="intersection",
    description="Find the intersection of two geometries."
)

mcp.add_tool(is_valid,
    name="is_valid",
    description="Check if a geometry is valid according to OGC rules."
)

mcp.add_tool(make_valid,
    name="make_valid",
    description="Fix an invalid geometry to make it valid."
)

mcp.add_tool(minimum_rotated_rectangle,
    name="minimum_rotated_rectangle",
    description="Get the minimum rotated rectangle of a geometry."
)

mcp.add_tool(nearest_point_on_geometry,
    name="nearest_point_on_geometry",
    description="Find the nearest point on geometry2 to geometry1."
)

mcp.add_tool(normalize_geometry,
    name="normalize_geometry",
    description="Normalize the orientation/order of a geometry (canonical form)."
)

mcp.add_tool(rotate_geometry,
    name="rotate_geometry",
    description="Rotate a geometry around an origin point."
)

mcp.add_tool(scale_geometry,
    name="scale_geometry",
    description="Scale a geometry by x and y factors."
)

mcp.add_tool(simplify,
    name="simplify",
    description="Simplify a geometry by reducing vertices with tolerance."
)

mcp.add_tool(snap_geometry,
    name="snap_geometry",
    description="Snap one geometry to another within a tolerance."
)

mcp.add_tool(symmetric_difference,
    name="symmetric_difference",
    description="Find the symmetric difference (XOR area) between two geometries."
)

mcp.add_tool(translate_geometry,
    name="translate_geometry",
    description="Translate (shift) a geometry by offsets."
)

mcp.add_tool(triangulate_geometry,
    name="triangulate_geometry",
    description="Create a Delaunay triangulation from a geometry."
)

mcp.add_tool(unary_union_geometries,
    name="unary_union_geometries",
    description="Create a union of multiple geometries at once."
)

mcp.add_tool(union,
    name="union",
    description="Combine two geometries into one."
)

mcp.add_tool(voronoi,
    name="voronoi",
    description="Create a Voronoi diagram from input points."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
