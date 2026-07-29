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

def resample_raster(
    source: str,
    scale_factor: float,
    resampling: str,
    destination: str
) -> Dict[str, Any]:
    """
    Resample a raster dataset by a scale factor and save the result.
    
    Parameters:
    - source:       local path or HTTPS URL of the source raster.
    - scale_factor: multiplicative factor for width/height 
                    (e.g., 0.5 to halve resolution, 2.0 to double).
    - resampling:   resampling method name: "nearest", "bilinear", "cubic", etc.
    - destination:  local filesystem path for the resampled raster.
    """
    try:
        import numpy as np
        import rasterio
        from rasterio.enums import Resampling
        from rasterio.transform import Affine

        # Strip backticks if present
        src_clean = source.replace("`", "")
        dst_clean = destination.replace("`", "")

        # Open source (remote or local)
        if src_clean.lower().startswith("https://"):
            src = rasterio.open(src_clean)
        else:
            src_path = os.path.expanduser(src_clean)
            if not os.path.isfile(src_path):
                raise FileNotFoundError(f"Source raster not found at '{src_path}'.")
            src = rasterio.open(src_path)

        # Validate scale factor
        if scale_factor <= 0:
            raise ValueError("Scale factor must be positive.")

        # Compute new dimensions
        new_width  = int(src.width  * scale_factor)
        new_height = int(src.height * scale_factor)

        if new_width == 0 or new_height == 0:
            raise ValueError("Resulting raster dimensions are zero. Check scale_factor.")

        # Map resampling method string to Resampling enum
        resampling_enum = getattr(Resampling, resampling.lower(), Resampling.nearest)

        # Read and resample all bands
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=resampling_enum
        )

        # Validate resampled data
        if data is None or data.size == 0:
            raise ValueError("No data was resampled.")

        # Calculate the new transform to reflect the resampling
        new_transform = src.transform * Affine.scale(
            (src.width  / new_width),
            (src.height / new_height)
        )

        # Update profile
        profile = src.profile.copy()
        profile.update({
            "height":    new_height,
            "width":     new_width,
            "transform": new_transform
        })
        src.close()

        # Ensure destination directory exists
        dst_path = os.path.expanduser(dst_clean)
        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

        # Write the resampled raster
        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(data)

        return {
            "status":      "success",
            "destination": str(dst_path),
            "message":     f"Raster resampled by factor {scale_factor} using '{resampling}' and saved to '{dst_path}'."
        }

    except Exception as e:
        # Log error and raise for MCP to report
        logger.error(f"Error resampling raster '{source}': {e}")
        raise ValueError(f"Failed to resample raster: {e}")
