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

def compute_ndvi(
    source: str,
    red_band_index: int,
    nir_band_index: int,
    destination: str
) -> Dict[str, Any]:
    """
    Compute NDVI (Normalized Difference Vegetation Index) and save to GeoTIFF.

    Parameters:
    - source:            input raster path.
    - red_band_index:    index of red band (1-based).
    - nir_band_index:    index of near-infrared band (1-based).
    - destination:       output NDVI raster path.
    """
    try:
        import rasterio
        import numpy as np

        src_path = os.path.expanduser(source.replace("`", ""))
        dst_path = os.path.expanduser(destination.replace("`", ""))

        with rasterio.open(src_path) as src:
            red = src.read(red_band_index).astype("float32")
            nir = src.read(nir_band_index).astype("float32")
            ndvi = (nir - red) / (nir + red + 1e-6)  # avoid division by zero

            profile = src.profile.copy()
            profile.update(dtype="float32", count=1)

        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(ndvi, 1)

        return {
            "status": "success",
            "destination": str(dst_path),
            "message": f"NDVI calculated and saved to '{dst_path}'."
        }

    except Exception as e:
        raise ValueError(f"Failed to compute NDVI: {e}")
