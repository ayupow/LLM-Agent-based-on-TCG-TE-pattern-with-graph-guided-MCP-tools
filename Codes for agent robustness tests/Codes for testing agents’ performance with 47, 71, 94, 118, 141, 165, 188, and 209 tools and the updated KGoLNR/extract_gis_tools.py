# Extract every @gis_mcp.tool() function from gis-mcp into standalone .py files
# following the pattern: one file per tool, no package-internal imports.
import os, re, ast, textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, 'gis-mcp-main', 'src', 'gis_mcp')

# Storage helper to embed in each tool file (replaces .storage_config imports)
STORAGE_HELPER = textwrap.dedent("""
import os
from pathlib import Path
_storage_path = None
def _get_storage_path():
    global _storage_path
    if _storage_path is None:
        _storage_path = Path.home() / '.gis_mcp' / 'data'
        _storage_path.mkdir(parents=True, exist_ok=True)
    return _storage_path
def _resolve_path(file_path, relative_to_storage=True):
    path = Path(file_path)
    if path.is_absolute(): return path.expanduser().resolve()
    if relative_to_storage: return (_get_storage_path() / path).resolve()
    return path.expanduser().resolve()
""").strip()

# Map: module_name -> { source_file, target_dir, tool_names }
MODULES = {
    'geopandas': {
        'source': os.path.join(SRC, 'geopandas_functions.py'),
        'target': os.path.join(BASE, 'tools_gis_geopandas'),
    },
    'shapely': {
        'source': os.path.join(SRC, 'shapely_functions.py'),
        'target': os.path.join(BASE, 'tools_gis_shapely'),
    },
    'pyproj': {
        'source': os.path.join(SRC, 'pyproj_functions.py'),
        'target': os.path.join(BASE, 'tools_gis_pyproj'),
    },
    'rasterio': {
        'source': os.path.join(SRC, 'rasterio_functions.py'),
        'target': os.path.join(BASE, 'tools_gis_rasterio'),
    },
    'pysal': {
        'source': os.path.join(SRC, 'pysal_functions.py'),
        'target': os.path.join(BASE, 'tools_gis_pysal'),
    },
    'data': {
        'source': [
            os.path.join(SRC, 'data', 'administrative_boundaries.py'),
            os.path.join(SRC, 'data', 'climate.py'),
            os.path.join(SRC, 'data', 'ecology.py'),
            os.path.join(SRC, 'data', 'land_cover.py'),
            os.path.join(SRC, 'data', 'movement.py'),
            os.path.join(SRC, 'data', 'satellite_imagery.py'),
        ],
        'target': os.path.join(BASE, 'tools_gis_data'),
        'multi_source': True,
    },
    'visualize': {
        'source': [
            os.path.join(SRC, 'visualize', 'map_tool.py'),
            os.path.join(SRC, 'visualize', 'web_map_tool.py'),
        ],
        'target': os.path.join(BASE, 'tools_gis_visualize'),
        'multi_source': True,
    },
    'utilities': {
        'source': os.path.join(SRC, 'save_tool.py'),
        'target': os.path.join(BASE, 'tools_gis_utilities'),
    },
}


def extract_tool_functions(source_path):
    """Parse a Python file and yield (func_name, func_source_lines, start_line) for
       each top-level function decorated with @gis_mcp.tool()."""
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tree = ast.parse(''.join(lines))

    # Find lines with @gis_mcp.tool() decorator
    decorator_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                # Check if decorator is gis_mcp.tool() or @gis_mcp.tool()
                if isinstance(dec, ast.Call):
                    if isinstance(dec.func, ast.Attribute) and isinstance(dec.func.value, ast.Name):
                        if dec.func.value.id == 'gis_mcp' and dec.func.attr == 'tool':
                            decorator_lines.add(node.lineno)
                elif isinstance(dec, ast.Attribute):
                    if isinstance(dec.value, ast.Name) and dec.value.id == 'gis_mcp' and dec.attr == 'tool':
                        decorator_lines.add(node.lineno)

    # Find all top-level function defs
    func_nodes = [n for n in ast.iter_child_nodes(tree) if isinstance(n, ast.FunctionDef)]

    results = []
    for func in func_nodes:
        if func.lineno in decorator_lines:
            # Get the function source: from the line BEFORE the decorator to end of function
            # (function may have @gis_mcp.tool() on line before def)
            start = func.lineno - 1  # 1-indexed -> 0-indexed, and include decorator line
            # But we want to skip the decorator line(s), start from the actual def
            def_start = func.lineno - 1  # 0-indexed for def line
            # Find actual start (may have multiple decorators)
            actual_start = def_start
            for i in range(def_start - 1, -1, -1):
                stripped = lines[i].strip()
                if stripped.startswith('@gis_mcp.tool') or stripped.startswith('@gis_mcp.resource'):
                    actual_start = i
                elif stripped == '' or stripped.startswith('#'):
                    continue
                else:
                    break

            end = func.end_lineno  # 1-indexed inclusive
            func_source = ''.join(lines[actual_start:end])

            # Remove @gis_mcp.tool() and @gis_mcp.resource() decorators
            func_lines = func_source.split('\n')
            cleaned_lines = []
            for line in func_lines:
                stripped = line.strip()
                if stripped.startswith('@gis_mcp.tool') or stripped.startswith('@gis_mcp.resource'):
                    continue
                cleaned_lines.append(line)
            func_source = '\n'.join(cleaned_lines)

            results.append((func.name, func_source))

    return results


def fix_imports(source_code, module_name):
    """Remove package-internal imports (.mcp, .storage_config) and
       add standalone equivalents."""
    lines = source_code.split('\n')
    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Skip internal imports
        if 'from .mcp import' in stripped or 'from .storage_config import' in stripped:
            continue
        if stripped == 'from .mcp import gis_mcp':
            continue
        new_lines.append(line)

    result = '\n'.join(new_lines)

    # Add necessary imports at the top
    header_lines = []
    header_lines.append('"""Standalone tool: {}. Auto-extracted from gis-mcp."""'.format(
        os.path.basename(module_name)))
    header_lines.append('import os')
    header_lines.append('import logging')
    header_lines.append('from typing import Any, Dict, List, Optional, Union')
    header_lines.append('from pathlib import Path')
    header_lines.append('')
    header_lines.append('# Storage helper (replaces gis_mcp.storage_config)')
    header_lines.append(STORAGE_HELPER)
    header_lines.append('')
    header_lines.append('# Configure logging')
    header_lines.append('logger = logging.getLogger(__name__)')
    header_lines.append('')

    # Insert header before the first non-comment, non-import line
    # Find the def line
    final_lines = header_lines + [result]
    return '\n'.join(final_lines)


def main():
    total = 0
    for mod_name, cfg in MODULES.items():
        target_dir = cfg['target']
        os.makedirs(target_dir, exist_ok=True)

        sources = cfg.get('source')
        if not isinstance(sources, list):
            sources = [sources]

        for source in sources:
            funcs = extract_tool_functions(source)
            for func_name, func_source in funcs:
                out_path = os.path.join(target_dir, f'{func_name}.py')
                fixed = fix_imports(func_source, mod_name)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f'  [{mod_name}] {func_name}.py')
                total += 1

    print(f'\nTotal: {total} tool files extracted from gis-mcp')


if __name__ == '__main__':
    main()
