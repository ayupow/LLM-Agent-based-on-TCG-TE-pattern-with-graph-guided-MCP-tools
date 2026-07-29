"""Standalone tool: pyproj. Auto-extracted from gis-mcp."""
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

def get_crs_info(crs: str) -> Dict[str, Any]:
    """Get information about a CRS."""
    try:
        import pyproj
        crs_obj = pyproj.CRS(crs)
        return {
            "status": "success",
            "name": crs_obj.name,
            "type": crs_obj.type_name,
            "axis_info": [axis.direction for axis in crs_obj.axis_info],
            "is_geographic": crs_obj.is_geographic,
            "is_projected": crs_obj.is_projected,
            "datum": str(crs_obj.datum),
            "ellipsoid": str(crs_obj.ellipsoid),
            "prime_meridian": str(crs_obj.prime_meridian),
            "area_of_use": str(crs_obj.area_of_use) if crs_obj.area_of_use else None,
            "message": "CRS information retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting CRS info: {str(e)}")
        raise ValueError(f"Failed to get CRS info: {str(e)}")
