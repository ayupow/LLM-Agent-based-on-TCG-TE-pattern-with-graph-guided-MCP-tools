# added_gis_geopandas_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from append_gpd import append_gpd
from clip_vector import clip_vector
from dissolve_gpd import dissolve_gpd
from merge_gpd import merge_gpd
from overlay_gpd import overlay_gpd
from point_in_polygon import point_in_polygon
from sjoin_gpd import sjoin_gpd
from sjoin_nearest_gpd import sjoin_nearest_gpd
from write_file_gpd import write_file_gpd

mcp = FastMCP(name="added_gis_geopandas_L4")

mcp.add_tool(append_gpd,
    name="append_gpd",
    description="Tool: append_gpd (from gis geopandas server)."
)

mcp.add_tool(clip_vector,
    name="clip_vector",
    description="Tool: clip_vector (from gis geopandas server)."
)

mcp.add_tool(dissolve_gpd,
    name="dissolve_gpd",
    description="Tool: dissolve_gpd (from gis geopandas server)."
)

mcp.add_tool(merge_gpd,
    name="merge_gpd",
    description="Tool: merge_gpd (from gis geopandas server)."
)

mcp.add_tool(overlay_gpd,
    name="overlay_gpd",
    description="Tool: overlay_gpd (from gis geopandas server)."
)

mcp.add_tool(point_in_polygon,
    name="point_in_polygon",
    description="Tool: point_in_polygon (from gis geopandas server)."
)

mcp.add_tool(sjoin_gpd,
    name="sjoin_gpd",
    description="Tool: sjoin_gpd (from gis geopandas server)."
)

mcp.add_tool(sjoin_nearest_gpd,
    name="sjoin_nearest_gpd",
    description="Tool: sjoin_nearest_gpd (from gis geopandas server)."
)

mcp.add_tool(write_file_gpd,
    name="write_file_gpd",
    description="Tool: write_file_gpd (from gis geopandas server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
