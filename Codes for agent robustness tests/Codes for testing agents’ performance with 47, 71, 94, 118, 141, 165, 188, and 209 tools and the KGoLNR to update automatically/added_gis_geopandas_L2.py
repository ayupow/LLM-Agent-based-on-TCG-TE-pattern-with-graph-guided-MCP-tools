# added_gis_geopandas_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from append_gpd import append_gpd
from explode_gpd import explode_gpd
from sjoin_nearest_gpd import sjoin_nearest_gpd
from write_file_gpd import write_file_gpd

mcp = FastMCP(name="added_gis_geopandas_L2")

mcp.add_tool(append_gpd,
    name="append_gpd",
    description="Tool: append_gpd (from gis geopandas server)."
)

mcp.add_tool(explode_gpd,
    name="explode_gpd",
    description="Tool: explode_gpd (from gis geopandas server)."
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
