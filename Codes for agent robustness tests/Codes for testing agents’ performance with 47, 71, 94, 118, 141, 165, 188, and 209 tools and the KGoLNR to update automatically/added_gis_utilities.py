# added_gis_utilities — MCP Server
# Auto-generated from tools_gis_utilities/ individual tool files

from mcp.server.fastmcp import FastMCP

from save_results import save_results

mcp = FastMCP(name="added_gis_utilities")

mcp.add_tool(save_results,
    name="save_results",
    description="Universal save/export for GIS tool results to JSON/CSV/YAML/XLSX/SHP/GEOJSON/GeoTIFF."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
