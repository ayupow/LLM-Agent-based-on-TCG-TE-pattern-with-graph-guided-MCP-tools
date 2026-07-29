"""Standalone tool: data. Auto-extracted from gis-mcp."""
import os
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Storage helper (replaces gis_mcp.storage_config)
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

# Configure logging
logger = logging.getLogger(__name__)

def calculate_shortest_path(graphml_path: str, origin: tuple, destination: tuple) -> Dict[str, Any]:
    """
    Calculate the shortest path between two points using a saved street network.
    Args:
        graphml_path: Path to the saved GraphML file
        origin: (lat, lon) tuple for the origin
        destination: (lat, lon) tuple for the destination
    Returns:
        List of node IDs representing the shortest path or error message.
    """
    try:
        G = ox.load_graphml(graphml_path)
        orig_node = ox.nearest_nodes(G, origin[1], origin[0])
        dest_node = ox.nearest_nodes(G, destination[1], destination[0])
        path = nx.shortest_path(G, orig_node, dest_node, weight="length")
        logger.info(f"Calculated shortest path from {origin} to {destination}")
        return {"status": "success", "path": path}
    except Exception as e:
        logger.exception("Failed to calculate shortest path")
        return {"status": "error", "message": str(e)}
