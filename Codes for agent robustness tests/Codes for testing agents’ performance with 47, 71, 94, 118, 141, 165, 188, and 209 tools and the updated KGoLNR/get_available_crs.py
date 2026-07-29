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

def get_available_crs() -> Dict[str, Any]:
    """Get list of available CRS."""
    try:
        import pyproj
        from pyproj.database import get_codes
        from pyproj.enums import PJType
        
        crs_list = []
        # Get a sample of common EPSG codes (limit to avoid huge lists)
        epsg_codes = list(get_codes("EPSG", PJType.CRS))[:100]  # Limit to first 100 for performance
        
        for code in epsg_codes:
            try:
                # Directly create CRS and get info without calling the tool function
                crs_obj = pyproj.CRS.from_epsg(int(code))
                crs_list.append({
                    "auth_name": "EPSG",
                    "code": str(code),
                    "name": crs_obj.name,
                    "type": crs_obj.type_name
                })
            except Exception as ex:
                # Skip invalid CRS codes
                logger.debug(f"Skipping EPSG:{code}: {str(ex)}")
                continue
        
        if not crs_list:
            # Fallback: return some well-known CRS
            well_known_crs = [
                {"auth_name": "EPSG", "code": "4326", "name": "WGS 84", "type": "Geographic 2D CRS"},
                {"auth_name": "EPSG", "code": "3857", "name": "WGS 84 / Pseudo-Mercator", "type": "Projected CRS"},
                {"auth_name": "EPSG", "code": "4269", "name": "NAD83", "type": "Geographic 2D CRS"},
            ]
            crs_list = well_known_crs
        
        return {
            "status": "success",
            "crs_list": crs_list,
            "message": "Available CRS list retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting available CRS: {str(e)}")
        raise ValueError(f"Failed to get available CRS: {str(e)}")
