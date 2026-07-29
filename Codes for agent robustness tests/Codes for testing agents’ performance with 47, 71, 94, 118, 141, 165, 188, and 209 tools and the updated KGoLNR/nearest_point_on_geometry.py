"""Standalone tool: shapely. Auto-extracted from gis-mcp."""
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

def nearest_point_on_geometry(geometry1: str, geometry2: str) -> Dict[str, Any]:
    """
    Find the nearest point on geometry2 to geometry1 using shapely.ops.nearest_points.
    Args:
        geometry1: WKT string of the first geometry (e.g., a point).
        geometry2: WKT string of the second geometry.
    Returns:
        Dictionary with status, message, and the nearest point as WKT.
    """
    try:
        from shapely import wkt
        from shapely.ops import nearest_points
        geom1 = wkt.loads(geometry1)
        geom2 = wkt.loads(geometry2)
        p1, p2 = nearest_points(geom1, geom2)
        return {
            "status": "success",
            "nearest_point": p2.wkt,
            "message": "Nearest point found successfully"
        }
    except Exception as e:
        logger.error(f"Error in nearest_point_on_geometry: {str(e)}")
        return {"status": "error", "message": str(e)}
