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

def raster_algebra(
    raster1: str,
    raster2: str,
    band_index: int,
    operation: str,  # User selects "add" or "subtract"
    destination: str
) -> Dict[str, Any]:
    """
    Perform algebraic operations (addition or subtraction) on two raster bands, 
    handling alignment issues automatically.

    Parameters:
    - raster1:     Path to the first raster (.tif).
    - raster2:     Path to the second raster (.tif).
    - band_index:  Index of the band to process (1-based index).
    - operation:   Either "add" or "subtract" to specify the calculation.
    - destination: Path to save the result as a new raster.

    The function aligns rasters if needed, applies the selected operation, and saves the result.
    """
    try:
        import rasterio
        import numpy as np
        from rasterio.warp import reproject, calculate_default_transform, Resampling

        # Expand file paths
        r1 = os.path.expanduser(raster1.replace("`", ""))
        r2 = os.path.expanduser(raster2.replace("`", ""))
        dst = os.path.expanduser(destination.replace("`", ""))

        # Open the raster files
        with rasterio.open(r1) as src1, rasterio.open(r2) as src2:
            # Ensure alignment of rasters
            if src1.crs != src2.crs or src1.transform != src2.transform or src1.shape != src2.shape:
                transform, width, height = calculate_default_transform(
                    src2.crs, src1.crs, src2.width, src2.height, *src2.bounds
                )
                aligned_data = np.zeros((height, width), dtype="float32")
                reproject(
                    source=src2.read(band_index),
                    destination=aligned_data,
                    src_transform=src2.transform,
                    src_crs=src2.crs,
                    dst_transform=transform,
                    dst_crs=src1.crs,
                    resampling=Resampling.bilinear
                )
                band2 = aligned_data
            else:
                band2 = src2.read(band_index).astype("float32")

            band1 = src1.read(band_index).astype("float32")

            # Perform the selected operation
            if operation.lower() == "add":
                result = band1 + band2
            elif operation.lower() == "subtract":
                result = band1 - band2
            else:
                raise ValueError("Invalid operation. Use 'add' or 'subtract'.")

            # Prepare output raster metadata
            profile = src1.profile.copy()
            profile.update(dtype="float32", count=1)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)

        # Save the result to a new raster file
        with rasterio.open(dst, "w", **profile) as dstfile:
            dstfile.write(result, 1)

        return {
            "status": "success",
            "destination": dst,
            "message": f"Raster operation '{operation}' completed and saved."
        }

    except Exception as e:
        raise ValueError(f"Failed to perform raster operation: {e}")
