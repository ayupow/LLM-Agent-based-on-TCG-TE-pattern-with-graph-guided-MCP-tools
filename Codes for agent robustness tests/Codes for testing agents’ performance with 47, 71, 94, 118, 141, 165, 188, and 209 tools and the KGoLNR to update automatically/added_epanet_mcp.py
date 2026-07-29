# added_epanet_mcp — EPANET Water Network Simulation MCP Server
from mcp.server.fastmcp import FastMCP

from run_epanet_simulation import run_epanet_simulation
from modify_network import modify_network
from plot_network import plot_network
from plot_pressures import plot_pressures
from plot_velocities import plot_velocities
from get_pressures_less_than import get_pressures_less_than
from get_pipes_over import get_pipes_over

mcp = FastMCP(name="added_epanet_mcp")

mcp.add_tool(run_epanet_simulation,
    name="run_epanet_simulation",
    description="Run a full EPANET hydraulic simulation on any network. Returns node count, pipe count, min pressure, and max velocity."
)
mcp.add_tool(modify_network,
    name="modify_network",
    description="Apply engineering interventions to a water network: open/close pipes, add/delete pipes, set diameters. Saves modified .inp file."
)
mcp.add_tool(plot_network,
    name="plot_network",
    description="Generate a PNG visualization of the EPANET network layout (nodes and pipes)."
)
mcp.add_tool(plot_pressures,
    name="plot_pressures",
    description="Plot node pressures with optional critical-node filtering below a threshold. Returns PNG image and text summary."
)
mcp.add_tool(plot_velocities,
    name="plot_velocities",
    description="Plot pipe velocities, highlighting stagnant/low-flow pipes below a threshold. Returns PNG image and text summary."
)
mcp.add_tool(get_pressures_less_than,
    name="get_pressures_less_than",
    description="List all EPANET nodes with pressure below a given threshold (Meters)."
)
mcp.add_tool(get_pipes_over,
    name="get_pipes_over",
    description="List all EPANET pipes with velocity above a given threshold (m/s)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
