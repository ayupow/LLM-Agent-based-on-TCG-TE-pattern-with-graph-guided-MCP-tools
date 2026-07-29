# added_powerfactory_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from close_digsilent import close_digsilent
from create_study_case import create_study_case
from get_config import get_config
from import_project import import_project
from modify_parameter import modify_parameter
from ping import ping
from read_results_csv import read_results_csv
from run_custom_case import run_custom_case
from run_loadflow import run_loadflow
from run_short_circuit import run_short_circuit
from run_simulation import run_simulation

mcp = FastMCP(name="added_powerfactory_L2")

mcp.add_tool(close_digsilent,
    name="close_digsilent",
    description="Tool: close_digsilent (from powerfactory server)."
)

mcp.add_tool(create_study_case,
    name="create_study_case",
    description="Tool: create_study_case (from powerfactory server)."
)

mcp.add_tool(get_config,
    name="get_config",
    description="Tool: get_config (from powerfactory server)."
)

mcp.add_tool(import_project,
    name="import_project",
    description="Tool: import_project (from powerfactory server)."
)

mcp.add_tool(modify_parameter,
    name="modify_parameter",
    description="Tool: modify_parameter (from powerfactory server)."
)

mcp.add_tool(ping,
    name="ping",
    description="Tool: ping (from powerfactory server)."
)

mcp.add_tool(read_results_csv,
    name="read_results_csv",
    description="Tool: read_results_csv (from powerfactory server)."
)

mcp.add_tool(run_custom_case,
    name="run_custom_case",
    description="Tool: run_custom_case (from powerfactory server)."
)

mcp.add_tool(run_loadflow,
    name="run_loadflow",
    description="Tool: run_loadflow (from powerfactory server)."
)

mcp.add_tool(run_short_circuit,
    name="run_short_circuit",
    description="Tool: run_short_circuit (from powerfactory server)."
)

mcp.add_tool(run_simulation,
    name="run_simulation",
    description="Tool: run_simulation (from powerfactory server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
