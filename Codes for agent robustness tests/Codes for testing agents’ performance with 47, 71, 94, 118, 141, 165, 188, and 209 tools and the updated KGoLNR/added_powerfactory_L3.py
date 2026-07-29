# added_powerfactory_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from get_config import get_config
from read_results_csv import read_results_csv
from run_short_circuit import run_short_circuit

mcp = FastMCP(name="added_powerfactory_L3")

mcp.add_tool(get_config,
    name="get_config",
    description="Tool: get_config (from powerfactory server)."
)

mcp.add_tool(read_results_csv,
    name="read_results_csv",
    description="Tool: read_results_csv (from powerfactory server)."
)

mcp.add_tool(run_short_circuit,
    name="run_short_circuit",
    description="Tool: run_short_circuit (from powerfactory server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
