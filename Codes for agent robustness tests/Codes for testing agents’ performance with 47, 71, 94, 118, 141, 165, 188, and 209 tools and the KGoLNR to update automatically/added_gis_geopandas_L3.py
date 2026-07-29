# added_gis_geopandas_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from dissolve_gpd import dissolve_gpd
from merge_gpd import merge_gpd
from sjoin_nearest_gpd import sjoin_nearest_gpd

mcp = FastMCP(name="added_gis_geopandas_L3")

mcp.add_tool(dissolve_gpd,
    name="dissolve_gpd",
    description="Tool: dissolve_gpd (from gis geopandas server)."
)

mcp.add_tool(merge_gpd,
    name="merge_gpd",
    description="Tool: merge_gpd (from gis geopandas server)."
)

mcp.add_tool(sjoin_nearest_gpd,
    name="sjoin_nearest_gpd",
    description="Tool: sjoin_nearest_gpd (from gis geopandas server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
