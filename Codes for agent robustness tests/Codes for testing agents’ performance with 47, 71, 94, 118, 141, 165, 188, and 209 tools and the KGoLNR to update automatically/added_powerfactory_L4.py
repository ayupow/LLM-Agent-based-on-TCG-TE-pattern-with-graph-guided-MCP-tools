# added_powerfactory_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from get_config import get_config
from import_project import import_project
from ping import ping
from run_custom_case import run_custom_case
from run_short_circuit import run_short_circuit

mcp = FastMCP(name="added_powerfactory_L4")

mcp.add_tool(get_config,
    name="get_config",
    description="Tool: get_config (from powerfactory server)."
)

mcp.add_tool(import_project,
    name="import_project",
    description="Tool: import_project (from powerfactory server)."
)

mcp.add_tool(ping,
    name="ping",
    description="Tool: ping (from powerfactory server)."
)

mcp.add_tool(run_custom_case,
    name="run_custom_case",
    description="Tool: run_custom_case (from powerfactory server)."
)

mcp.add_tool(run_short_circuit,
    name="run_short_circuit",
    description="Tool: run_short_circuit (from powerfactory server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
