# added_gis_shapely_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from buffer import buffer
from convex_hull import convex_hull
from get_bounds import get_bounds
from get_length import get_length
from nearest_point_on_geometry import nearest_point_on_geometry
from symmetric_difference import symmetric_difference

mcp = FastMCP(name="added_gis_shapely_L3")

mcp.add_tool(buffer,
    name="buffer",
    description="Tool: buffer (from gis shapely server)."
)

mcp.add_tool(convex_hull,
    name="convex_hull",
    description="Tool: convex_hull (from gis shapely server)."
)

mcp.add_tool(get_bounds,
    name="get_bounds",
    description="Tool: get_bounds (from gis shapely server)."
)

mcp.add_tool(get_length,
    name="get_length",
    description="Tool: get_length (from gis shapely server)."
)

mcp.add_tool(nearest_point_on_geometry,
    name="nearest_point_on_geometry",
    description="Tool: nearest_point_on_geometry (from gis shapely server)."
)

mcp.add_tool(symmetric_difference,
    name="symmetric_difference",
    description="Tool: symmetric_difference (from gis shapely server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
