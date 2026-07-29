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

def calculate_geodetic_point(start_point: List[float], azimuth: float, 
                        distance: float, ellps: str = "WGS84") -> Dict[str, Any]:
    """Calculate point at given distance and azimuth."""
    try:
        import pyproj
        geod = pyproj.Geod(ellps=ellps)
        lon, lat = start_point
        lon2, lat2, back_azimuth = geod.fwd(lon, lat, azimuth, distance)
        return {
            "status": "success",
            "point": [lon2, lat2],
            "back_azimuth": back_azimuth,
            "ellps": ellps,
            "message": "Geodetic point calculated successfully"
        }
    except Exception as e:
        logger.error(f"Error calculating geodetic point: {str(e)}")
        raise ValueError(f"Failed to calculate geodetic point: {str(e)}")
