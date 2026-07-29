# added_gis_utilities_L6 — MCP Server (subset for level L6)
from mcp.server.fastmcp import FastMCP

from save_results import save_results

mcp = FastMCP(name="added_gis_utilities_L6")

mcp.add_tool(save_results,
    name="save_results",
    description="Tool: save_results (from gis utilities server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
