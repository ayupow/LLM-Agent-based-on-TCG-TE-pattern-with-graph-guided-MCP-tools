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

def geojson_to_geometry(geojson: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert GeoJSON to a Shapely geometry using shapely.geometry.shape.
    Args:
        geojson: GeoJSON dictionary.
    Returns:
        Dictionary with status, message, and geometry as WKT.
    """
    try:
        from shapely.geometry import shape
        geom = shape(geojson)
        return {
            "status": "success",
            "geometry": geom.wkt,
            "message": "GeoJSON converted to geometry successfully"
        }
    except Exception as e:
        logger.error(f"Error in geojson_to_geometry: {str(e)}")
        return {"status": "error", "message": str(e)}
