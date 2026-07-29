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

def write_raster(array: list, reference_raster: str, output_path: str, dtype: str = None) -> Dict[str, Any]:
    """
    Write a numpy array to a raster file using metadata from a reference raster.
    Args:
        array: 2D or 3D list (or numpy array) of raster values.
        reference_raster: Path to a raster whose metadata will be copied.
        output_path: Path to save the new raster.
        dtype: Optional data type (e.g., 'float32', 'uint8').
    Returns:
        Dictionary with status and message.
    """
    try:
        import rasterio
        import numpy as np
        arr = np.array(array)
        with rasterio.open(reference_raster) as src:
            profile = src.profile.copy()
            if dtype:
                profile.update(dtype=dtype)
            if arr.ndim == 2:
                profile.update(count=1)
            elif arr.ndim == 3:
                profile.update(count=arr.shape[0])
            else:
                raise ValueError("Array must be 2D or 3D.")
        output_path_resolved = resolve_path(output_path, relative_to_storage=True)
        output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(str(output_path_resolved), "w", **profile) as dst:
            # Reshape 2D array to (1, height, width) for rasterio.write()
            if arr.ndim == 2:
                dst.write(arr, 1)  # Write to band 1
            else:
                dst.write(arr)
        return {
            "status": "success",
            "message": f"Raster written to '{output_path_resolved}' successfully.",
            "output_path": str(output_path_resolved)
        }
    except Exception as e:
        logger.error(f"Error in write_raster: {str(e)}")
        return {"status": "error", "message": str(e)}
