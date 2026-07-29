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

def make_valid(geometry: str) -> Dict[str, Any]:
    """Make a geometry valid."""
    try:
        from shapely import wkt, make_valid
        geom = wkt.loads(geometry)
        result = make_valid(geom)
        return {
            "status": "success",
            "geometry": result.wkt,
            "message": "Geometry made valid successfully"
        }
    except Exception as e:
        logger.error(f"Error making geometry valid: {str(e)}")
        raise ValueError(f"Failed to make geometry valid: {str(e)}")
