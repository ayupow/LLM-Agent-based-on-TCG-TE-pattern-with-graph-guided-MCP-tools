# added_math_mcp — Mathematical & Statistical Operations MCP Server
from mcp.server.fastmcp import FastMCP

from add import add
from subtract import subtract
from multiply import multiply
from division import division
from sum_list import sum_list
from modulo import modulo
from floor import floor
from ceiling import ceiling
from math_round import math_round
from mean import mean
from median import median
from mode import mode
from min_list import min_list
from max_list import max_list
from math_sin import math_sin
from math_cos import math_cos
from math_tan import math_tan
from math_arcsin import math_arcsin
from math_arccos import math_arccos
from math_arctan import math_arctan
from radians_to_degrees import radians_to_degrees
from degrees_to_radians import degrees_to_radians

mcp = FastMCP(name="added_math_mcp")

mcp.add_tool(add, name="add", description="Add two numbers together: a + b.")
mcp.add_tool(subtract, name="subtract", description="Subtract b from a: a - b.")
mcp.add_tool(multiply, name="multiply", description="Multiply two numbers: a * b.")
mcp.add_tool(division, name="division", description="Divide a by b: a / b. Returns inf if b==0.")
mcp.add_tool(sum_list, name="sum_list", description="Sum all numbers in a list.")
mcp.add_tool(modulo, name="modulo", description="Return remainder of a divided by b: a % b.")
mcp.add_tool(floor, name="floor", description="Round a number down to nearest integer (floor).")
mcp.add_tool(ceiling, name="ceiling", description="Round a number up to nearest integer (ceiling).")
mcp.add_tool(math_round, name="math_round", description="Round a number to nearest integer.")
mcp.add_tool(mean, name="mean", description="Calculate arithmetic mean of a list of numbers.")
mcp.add_tool(median, name="median", description="Calculate median of a list of numbers.")
mcp.add_tool(mode, name="mode", description="Find the most common value (mode) in a list of numbers.")
mcp.add_tool(min_list, name="min_list", description="Find the minimum value in a list of numbers.")
mcp.add_tool(max_list, name="max_list", description="Find the maximum value in a list of numbers.")
mcp.add_tool(math_sin, name="math_sin", description="Calculate sine of x (input in radians).")
mcp.add_tool(math_cos, name="math_cos", description="Calculate cosine of x (input in radians).")
mcp.add_tool(math_tan, name="math_tan", description="Calculate tangent of x (input in radians).")
mcp.add_tool(math_arcsin, name="math_arcsin", description="Calculate arcsine of x (returns radians).")
mcp.add_tool(math_arccos, name="math_arccos", description="Calculate arccosine of x (returns radians).")
mcp.add_tool(math_arctan, name="math_arctan", description="Calculate arctangent of x (returns radians).")
mcp.add_tool(radians_to_degrees, name="radians_to_degrees", description="Convert radians to degrees.")
mcp.add_tool(degrees_to_radians, name="degrees_to_radians", description="Convert degrees to radians.")

if __name__ == "__main__":
    mcp.run(transport="stdio")
