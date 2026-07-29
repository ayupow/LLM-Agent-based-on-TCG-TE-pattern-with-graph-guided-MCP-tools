# added_math_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from add import add
from division import division
from floor import floor
from math_arccos import math_arccos
from math_arcsin import math_arcsin
from math_cos import math_cos
from math_round import math_round
from math_sin import math_sin
from math_tan import math_tan
from max_list import max_list
from mean import mean
from median import median
from min_list import min_list
from mode import mode
from modulo import modulo
from multiply import multiply

mcp = FastMCP(name="added_math_L3")

mcp.add_tool(add,
    name="add",
    description="Tool: add (from math server)."
)

mcp.add_tool(division,
    name="division",
    description="Tool: division (from math server)."
)

mcp.add_tool(floor,
    name="floor",
    description="Tool: floor (from math server)."
)

mcp.add_tool(math_arccos,
    name="math_arccos",
    description="Tool: math_arccos (from math server)."
)

mcp.add_tool(math_arcsin,
    name="math_arcsin",
    description="Tool: math_arcsin (from math server)."
)

mcp.add_tool(math_cos,
    name="math_cos",
    description="Tool: math_cos (from math server)."
)

mcp.add_tool(math_round,
    name="math_round",
    description="Tool: math_round (from math server)."
)

mcp.add_tool(math_sin,
    name="math_sin",
    description="Tool: math_sin (from math server)."
)

mcp.add_tool(math_tan,
    name="math_tan",
    description="Tool: math_tan (from math server)."
)

mcp.add_tool(max_list,
    name="max_list",
    description="Tool: max_list (from math server)."
)

mcp.add_tool(mean,
    name="mean",
    description="Tool: mean (from math server)."
)

mcp.add_tool(median,
    name="median",
    description="Tool: median (from math server)."
)

mcp.add_tool(min_list,
    name="min_list",
    description="Tool: min_list (from math server)."
)

mcp.add_tool(mode,
    name="mode",
    description="Tool: mode (from math server)."
)

mcp.add_tool(modulo,
    name="modulo",
    description="Tool: modulo (from math server)."
)

mcp.add_tool(multiply,
    name="multiply",
    description="Tool: multiply (from math server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
