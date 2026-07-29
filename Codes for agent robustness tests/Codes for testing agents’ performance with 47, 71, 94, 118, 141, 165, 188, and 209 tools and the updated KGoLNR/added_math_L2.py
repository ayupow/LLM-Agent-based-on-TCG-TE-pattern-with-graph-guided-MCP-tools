# added_math_L2 — MCP Server (subset for level L2)
from mcp.server.fastmcp import FastMCP

from add import add
from ceiling import ceiling
from degrees_to_radians import degrees_to_radians
from division import division
from floor import floor
from math_arcsin import math_arcsin
from math_round import math_round
from math_tan import math_tan
from mean import mean
from min_list import min_list
from mode import mode
from multiply import multiply
from radians_to_degrees import radians_to_degrees
from subtract import subtract
from sum_list import sum_list

mcp = FastMCP(name="added_math_L2")

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

mcp.add_tool(division,
    name="division",
    description="Tool: division (from math server)."
)

mcp.add_tool(floor,
    name="floor",
    description="Tool: floor (from math server)."
)

mcp.add_tool(math_arcsin,
    name="math_arcsin",
    description="Tool: math_arcsin (from math server)."
)

mcp.add_tool(math_round,
    name="math_round",
    description="Tool: math_round (from math server)."
)

mcp.add_tool(math_tan,
    name="math_tan",
    description="Tool: math_tan (from math server)."
)

mcp.add_tool(mean,
    name="mean",
    description="Tool: mean (from math server)."
)

mcp.add_tool(min_list,
    name="min_list",
    description="Tool: min_list (from math server)."
)

mcp.add_tool(mode,
    name="mode",
    description="Tool: mode (from math server)."
)

mcp.add_tool(multiply,
    name="multiply",
    description="Tool: multiply (from math server)."
)

mcp.add_tool(radians_to_degrees,
    name="radians_to_degrees",
    description="Tool: radians_to_degrees (from math server)."
)

mcp.add_tool(subtract,
    name="subtract",
    description="Tool: subtract (from math server)."
)

mcp.add_tool(sum_list,
    name="sum_list",
    description="Tool: sum_list (from math server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
