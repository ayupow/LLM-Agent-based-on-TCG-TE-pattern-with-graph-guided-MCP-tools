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

def get_utm_zone(coordinates: List[float]) -> Dict[str, Any]:
    """Get UTM zone for given coordinates."""
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
        
        # Create CRS from the first matching CRSInfo
        crs_obj = pyproj.CRS.from_authority(crs_info_list[0].auth_name, crs_info_list[0].code)
        # Extract zone number from CRS name (e.g., "WGS 84 / UTM zone 10N" -> 10)
        import re
        zone_match = re.search(r'zone\s+(\d+)', crs_info_list[0].name, re.IGNORECASE)
        if zone_match:
            zone = int(zone_match.group(1))
        else:
            # Fallback: try to extract from authority code
            # EPSG codes for UTM: 32601-32660 (north), 32701-32760 (south)
            code = int(crs_info_list[0].code)
            if 32601 <= code <= 32660:  # Northern hemisphere
                zone = code - 32600
            elif 32701 <= code <= 32760:  # Southern hemisphere
                zone = code - 32700
            else:
                raise ValueError("Could not extract valid UTM zone number from CRS")
        
        if zone < 1 or zone > 60:
            raise ValueError(f"Invalid UTM zone number: {zone}")
        
        return {
            "status": "success",
            "zone": zone,
            "message": "UTM zone retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting UTM zone: {str(e)}")
        raise ValueError(f"Failed to get UTM zone: {str(e)}")
