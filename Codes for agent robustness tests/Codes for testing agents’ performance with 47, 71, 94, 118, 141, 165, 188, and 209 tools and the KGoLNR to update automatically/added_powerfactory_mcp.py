# added_powerfactory_mcp — MCP Server
# Auto-generated from tools_powerfactory/ individual tool files

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

mcp = FastMCP(name="added_powerfactory_mcp")

mcp.add_tool(close_digsilent,
    name="close_digsilent",
    description="Close the DIgSILENT PowerFactory API session."
)

mcp.add_tool(create_study_case,
    name="create_study_case",
    description="Create and activate a study case without running simulation."
)

mcp.add_tool(get_config,
    name="get_config",
    description="Return the active simulation_config.json as a JSON string."
)

mcp.add_tool(import_project,
    name="import_project",
    description="Import a DIgSILENT PowerFactory project from a .pfd file and activate it."
)

mcp.add_tool(modify_parameter,
    name="modify_parameter",
    description="Set an attribute on all PowerFactory objects matching a query."
)

mcp.add_tool(ping,
    name="ping",
    description="Health check — returns 'pong' to verify MCP server is reachable."
)

mcp.add_tool(read_results_csv,
    name="read_results_csv",
    description="Read RMS simulation results CSV. Auto-discovers latest file."
)

mcp.add_tool(run_custom_case,
    name="run_custom_case",
    description="Run a single custom fault case with parameters at call-time."
)

mcp.add_tool(run_loadflow,
    name="run_loadflow",
    description="Run a load flow calculation (ComLdf) on the active study case."
)

mcp.add_tool(run_short_circuit,
    name="run_short_circuit",
    description="Run a short-circuit calculation (ComShc) on the active study case."
)

mcp.add_tool(run_simulation,
    name="run_simulation",
    description="Run full RMS simulation pipeline: connect → load flow → RMS → CSV → plots."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
