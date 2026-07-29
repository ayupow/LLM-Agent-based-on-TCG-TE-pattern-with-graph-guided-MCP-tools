# added_gis_pysal_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from adbscan import adbscan
from build_and_transform_weights import build_and_transform_weights
from gamma_statistic import gamma_statistic
from getis_ord_g import getis_ord_g
from gm_lag import gm_lag
from morans_i import morans_i

mcp = FastMCP(name="added_gis_pysal_L2")

mcp.add_tool(adbscan,
    name="adbscan",
    description="Tool: adbscan (from gis pysal server)."
)

mcp.add_tool(build_and_transform_weights,
    name="build_and_transform_weights",
    description="Tool: build_and_transform_weights (from gis pysal server)."
)

mcp.add_tool(gamma_statistic,
    name="gamma_statistic",
    description="Tool: gamma_statistic (from gis pysal server)."
)

mcp.add_tool(getis_ord_g,
    name="getis_ord_g",
    description="Tool: getis_ord_g (from gis pysal server)."
)

mcp.add_tool(gm_lag,
    name="gm_lag",
    description="Tool: gm_lag (from gis pysal server)."
)

mcp.add_tool(morans_i,
    name="morans_i",
    description="Tool: morans_i (from gis pysal server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
