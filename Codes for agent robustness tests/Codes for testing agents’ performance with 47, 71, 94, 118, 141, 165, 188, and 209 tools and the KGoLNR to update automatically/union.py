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

def union(geometry1: str, geometry2: str) -> Dict[str, Any]:
    """Combine two geometries."""
    try:
        from shapely import wkt
        geom1 = wkt.loads(geometry1)
        geom2 = wkt.loads(geometry2)
        result = geom1.union(geom2)
        return {
            "status": "success",
            "geometry": result.wkt,
            "message": "Union created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating union: {str(e)}")
        raise ValueError(f"Failed to create union: {str(e)}")
