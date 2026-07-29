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

def get_utm_crs(coordinates: List[float]) -> Dict[str, Any]:
    """Get UTM CRS for given coordinates."""
    try:
        import pyproj
        from pyproj.database import query_utm_crs_info
        lon, lat = coordinates
        crs_info_list = query_utm_crs_info(
            datum_name="WGS 84",  # Use "WGS 84" with space as per standard
            area_of_interest=pyproj.aoi.AreaOfInterest(
                west_lon_degree=lon,
                south_lat_degree=lat,
                east_lon_degree=lon,
                north_lat_degree=lat
            )
        )
        if not crs_info_list:
            raise ValueError("No UTM CRS found for the given coordinates")
        
        # Create CRS from CRSInfo and get its string representation
        crs_obj = pyproj.CRS.from_authority(crs_info_list[0].auth_name, crs_info_list[0].code)
        crs_str = crs_obj.to_string()
        
        return {
            "status": "success",
            "crs": crs_str,
            "message": "UTM CRS retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting UTM CRS: {str(e)}")
        raise ValueError(f"Failed to get UTM CRS: {str(e)}")
