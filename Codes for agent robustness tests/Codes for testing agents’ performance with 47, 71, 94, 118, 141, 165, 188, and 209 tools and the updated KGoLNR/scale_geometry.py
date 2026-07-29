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

def scale_geometry(geometry: str, xfact: float, yfact: float, 
                origin: str = "center") -> Dict[str, Any]:
    """Scale a geometry."""
    try:
        from shapely import wkt
        from shapely.affinity import scale
        geom = wkt.loads(geometry)
        result = scale(geom, xfact=xfact, yfact=yfact, origin=origin)
        return {
            "status": "success",
            "geometry": result.wkt,
            "message": "Geometry scaled successfully"
        }
    except Exception as e:
        logger.error(f"Error scaling geometry: {str(e)}")
        raise ValueError(f"Failed to scale geometry: {str(e)}")
