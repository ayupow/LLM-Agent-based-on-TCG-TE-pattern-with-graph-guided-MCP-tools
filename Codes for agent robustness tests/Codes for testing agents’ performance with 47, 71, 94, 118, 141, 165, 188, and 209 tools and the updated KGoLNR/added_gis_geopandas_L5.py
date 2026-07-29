# added_gis_geopandas_L5 — MCP Server (subset for level L5)
from mcp.server.fastmcp import FastMCP

from append_gpd import append_gpd
from clip_vector import clip_vector
from dissolve_gpd import dissolve_gpd
from merge_gpd import merge_gpd
from write_file_gpd import write_file_gpd

mcp = FastMCP(name="added_gis_geopandas_L5")

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

mcp.add_tool(write_file_gpd,
    name="write_file_gpd",
    description="Tool: write_file_gpd (from gis geopandas server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
