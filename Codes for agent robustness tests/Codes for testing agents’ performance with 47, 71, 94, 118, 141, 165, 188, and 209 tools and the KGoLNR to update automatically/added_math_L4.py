# added_math_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from ceiling import ceiling
from division import division
from math_arcsin import math_arcsin
from math_sin import math_sin
from mean import mean
from median import median

mcp = FastMCP(name="added_math_L4")

mcp.add_tool(ceiling,
    name="ceiling",
    description="Tool: ceiling (from math server)."
)

mcp.add_tool(division,
    name="division",
    description="Tool: division (from math server)."
)

mcp.add_tool(math_arcsin,
    name="math_arcsin",
    description="Tool: math_arcsin (from math server)."
)

mcp.add_tool(math_sin,
    name="math_sin",
    description="Tool: math_sin (from math server)."
)

mcp.add_tool(mean,
    name="mean",
    description="Tool: mean (from math server)."
)

mcp.add_tool(median,
    name="median",
    description="Tool: median (from math server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
