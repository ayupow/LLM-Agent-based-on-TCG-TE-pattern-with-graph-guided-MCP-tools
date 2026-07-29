# -*- coding: utf-8 -*-
"""Regenerate math tools with clean UTF-8."""
import os
BASE = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(BASE, 'tools_math')

tools = [
    ("add", "a: float, b: float", "float", "Add two numbers.", "return a + b"),
    ("subtract", "a: float, b: float", "float", "Subtract b from a.", "return a - b"),
    ("multiply", "a: float, b: float", "float", "Multiply two numbers.", "return a * b"),
    ("division", "a: float, b: float", "float", "Divide a by b.", "return a / b if b != 0 else float('inf')"),
    ("sum_list", "numbers: list", "float", "Sum a list of numbers.", "return sum(numbers)"),
    ("modulo", "a: float, b: float", "float", "Return a % b.", "return a % b"),
    ("floor", "x: float", "int", "Floor: round down.", "import math; return math.floor(x)"),
    ("ceiling", "x: float", "int", "Ceiling: round up.", "import math; return math.ceil(x)"),
    ("math_round", "x: float", "int", "Round to nearest integer.", "return round(x)"),
    ("mean", "numbers: list", "float", "Arithmetic mean.", "return sum(numbers) / len(numbers) if numbers else 0"),
    ("median", "numbers: list", "float", "Median value.", "import statistics; return statistics.median(numbers) if numbers else 0"),
    ("mode", "numbers: list", "float", "Most common value.", "import statistics; return statistics.mode(numbers) if numbers else 0"),
    ("min_list", "numbers: list", "float", "Minimum value.", "return min(numbers) if numbers else 0"),
    ("max_list", "numbers: list", "float", "Maximum value.", "return max(numbers) if numbers else 0"),
    ("math_sin", "x: float", "float", "Sine (radians).", "import math; return math.sin(x)"),
    ("math_cos", "x: float", "float", "Cosine (radians).", "import math; return math.cos(x)"),
    ("math_tan", "x: float", "float", "Tangent (radians).", "import math; return math.tan(x)"),
    ("math_arcsin", "x: float", "float", "Arcsine -> radians.", "import math; return math.asin(x)"),
    ("math_arccos", "x: float", "float", "Arccosine -> radians.", "import math; return math.acos(x)"),
    ("math_arctan", "x: float", "float", "Arctangent -> radians.", "import math; return math.atan(x)"),
    ("radians_to_degrees", "x: float", "float", "Radians to degrees.", "import math; return math.degrees(x)"),
    ("degrees_to_radians", "x: float", "float", "Degrees to radians.", "import math; return math.radians(x)"),
]

for fname, params, ret, desc, body in tools:
    code = f'# -*- coding: utf-8 -*-\n"""Tool: {fname} - {desc}"""\n\ndef {fname}({params}) -> {ret}:\n    """{desc}"""\n    {body}\n'
    path = os.path.join(TDIR, f'{fname}.py')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    # Also copy to main dir
    with open(os.path.join(BASE, f'{fname}.py'), 'w', encoding='utf-8') as f:
        f.write(code)
    print(f'  {fname}.py')

print(f'Done: {len(tools)} math tools regenerated')
