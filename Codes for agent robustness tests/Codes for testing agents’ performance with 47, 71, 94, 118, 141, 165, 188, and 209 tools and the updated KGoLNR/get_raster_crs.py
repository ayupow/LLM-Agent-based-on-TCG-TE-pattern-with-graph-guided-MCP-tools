"""Standalone tool: rasterio. Auto-extracted from gis-mcp."""
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

def get_raster_crs(path_or_url: str) -> Dict[str, Any]:
    """
    Retrieve the Coordinate Reference System (CRS) of a raster dataset.
    
    Opens the raster (local path or HTTPS URL), reads its DatasetReader.crs
    attribute as a PROJ.4-style dict, and also returns the WKT representation.
    """
    try:
        import numpy as np
        import rasterio

        # Strip backticks if the client wrapped the input in them
        cleaned = path_or_url.replace("`", "")

        # Open remote or local dataset
        if cleaned.lower().startswith("https://"):
            src = rasterio.open(cleaned)
        else:
            local_path = os.path.expanduser(cleaned)
            if not os.path.isfile(local_path):
                raise FileNotFoundError(f"Raster file not found at '{local_path}'.")
            src = rasterio.open(local_path)

        # Access the CRS object on the opened dataset
        crs_obj = src.crs
        src.close()

        if crs_obj is None:
            raise ValueError("No CRS defined for this dataset.")

        # Convert CRS to PROJ.4‐style dict and WKT string
        proj4_dict = crs_obj.to_dict()    # e.g., {'init': 'epsg:32618'}
        wkt_str    = crs_obj.to_wkt()     # full WKT representation

        return {
            "status":      "success",
            "proj4":       proj4_dict,
            "wkt":         wkt_str,
            "message":     "CRS retrieved successfully"
        }

    except Exception as e:
        # Log and re-raise as ValueError for MCP error propagation
        logger.error(f"Error retrieving CRS for '{path_or_url}': {e}")
        raise ValueError(f"Failed to retrieve CRS: {e}")
