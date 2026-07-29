# added_math_L6 — MCP Server (subset for level L6)
from mcp.server.fastmcp import FastMCP

from add import add
from ceiling import ceiling
from degrees_to_radians import degrees_to_radians
from math_arcsin import math_arcsin
from multiply import multiply
from median import median
from max_list import max_list
from math_arctan import math_arctan
from math_arccos import math_arccos
from math_round import math_round
from math_tan import math_tan
from min_list import min_list
from floor import floor
from division import division
from mode import mode
from subtract import subtract
from math_sin import math_sin
from mean import mean
from modulo import modulo
from math_cos import math_cos
from sum_list import sum_list
from radians_to_degrees import radians_to_degrees

mcp = FastMCP(name="added_math_L6")

mcp.add_tool(add,
    name="add",
    description="Tool: add (from math server)."
)

mcp.add_tool(ceiling,
    name="ceiling",
    description="Tool: ceiling (from math server)."
)

mcp.add_tool(degrees_to_radians,
    name="degrees_to_radians",
    description="Tool: degrees_to_radians (from math server)."
)

mcp.add_tool(math_arcsin,
    name="math_arcsin",
    description="Tool: math_arcsin (from math server)."
)

mcp.add_tool(multiply,
    name="multiply",
    description="Tool: multiply (from math server)."
)

mcp.add_tool(median,
    name="median",
    description="Tool: median (from math server)."
)

mcp.add_tool(max_list,
    name="max_list",
    description="Tool: max_list (from math server)."
)

mcp.add_tool(math_arctan,
    name="math_arctan",
    description="Tool: math_arctan (from math server)."
)

mcp.add_tool(math_arccos,
    name="math_arccos",
    description="Tool: math_arccos (from math server)."
)

mcp.add_tool(math_round,
    name="math_round",
    description="Tool: math_round (from math server)."
)

mcp.add_tool(math_tan,
    name="math_tan",
    description="Tool: math_tan (from math server)."
)

mcp.add_tool(min_list,
    name="min_list",
    description="Tool: min_list (from math server)."
)

mcp.add_tool(floor,
    name="floor",
    description="Tool: floor (from math server)."
)

mcp.add_tool(division,
    name="division",
    description="Tool: division (from math server)."
)

mcp.add_tool(mode,
    name="mode",
    description="Tool: mode (from math server)."
)

mcp.add_tool(subtract,
    name="subtract",
    description="Tool: subtract (from math server)."
)

mcp.add_tool(math_sin,
    name="math_sin",
    description="Tool: math_sin (from math server)."
)

mcp.add_tool(mean,
    name="mean",
    description="Tool: mean (from math server)."
)

mcp.add_tool(modulo,
    name="modulo",
    description="Tool: modulo (from math server)."
)

mcp.add_tool(math_cos,
    name="math_cos",
    description="Tool: math_cos (from math server)."
)

mcp.add_tool(sum_list,
    name="sum_list",
    description="Tool: sum_list (from math server)."
)

mcp.add_tool(radians_to_degrees,
    name="radians_to_degrees",
    description="Tool: radians_to_degrees (from math server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
