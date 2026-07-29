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

def metadata_raster(path_or_url: str) -> Dict[str, Any]:
    """
    Open a raster dataset in read-only mode and return metadata.
    
    This tool supports two modes based on the provided string:
    1. A local filesystem path (e.g., "D:\\Data\\my_raster.tif").
    2. An HTTPS URL (e.g., "https://example.com/my_raster.tif").
    
    The input must be a single string that is either a valid file path
    on the local machine or a valid HTTPS URL pointing to a raster.
    """
    try:
        # Import numpy first to ensure NumPy's C-API is initialized
        import numpy as np
        import rasterio

        # Remove any backticks (`) if the client wrapped the path_or_url in them
        cleaned = path_or_url.replace("`", "")

        # Determine if the string is an HTTPS URL or a local file path
        if cleaned.lower().startswith("https://"):
            # For HTTPS URLs, let Rasterio/GDAL handle remote access directly
            dataset = rasterio.open(cleaned)
        else:
            # Treat as local filesystem path
            local_path = os.path.expanduser(cleaned)

            # Verify that the file exists on disk
            if not os.path.isfile(local_path):
                raise FileNotFoundError(f"Raster file not found at '{local_path}'.")

            # Open the local file in read-only mode
            dataset = rasterio.open(local_path)

        # Build a mapping from band index to its data type (dtype)
        band_dtypes = {i: dtype for i, dtype in zip(dataset.indexes, dataset.dtypes)}

        # Collect core metadata fields in simple Python types
        meta: Dict[str, Any] = {
            "name": dataset.name,                                       # Full URI or filesystem path
            "mode": dataset.mode,                                       # Mode should be 'r' for read                                 
            "driver": dataset.driver,                                   # GDAL driver, e.g. "GTiff"
            "width": dataset.width,                                     # Number of columns
            "height": dataset.height,                                   # Number of rows
            "count": dataset.count,                                     # Number of bands
            "bounds": dataset.bounds,                                   # Show bounding box
            "band_dtypes": band_dtypes,                                 # { band_index: dtype_string }
            "no_data": dataset.nodatavals,                              # Number of NoData values in each band
            "crs": dataset.crs.to_string() if dataset.crs else None,    # CRS as EPSG string or None
            "transform": list(dataset.transform),                       # Affine transform coefficients (6 floats)
        }

        # Return a success status along with metadata
        return {
            "status": "success",
            "metadata": meta,
            "message": f"Raster dataset opened successfully from '{cleaned}'."
        }

    except Exception as e:
        # Log the error for debugging purposes, then raise ValueError so MCP can relay it
        logger.error(f"Error opening raster '{path_or_url}': {str(e)}")
        raise ValueError(f"Failed to open raster '{path_or_url}': {str(e)}")
