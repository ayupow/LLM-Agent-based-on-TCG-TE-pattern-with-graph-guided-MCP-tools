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

def raster_band_statistics(
    source: str
) -> Dict[str, Any]:
    """
    Calculate min, max, mean, and std for each band of a raster.

    Parameters:
    - source: path to input raster (local or URL).
    """
    try:
        import numpy as np
        import rasterio

        src_path = os.path.expanduser(source.replace("`", ""))
        stats = {}

        with rasterio.open(src_path) as src:
            for i in range(1, src.count + 1):
                band = src.read(i, masked=True)  # masked array handles NoData
                stats[f"Band {i}"] = {
                    "min": float(band.min()),
                    "max": float(band.max()),
                    "mean": float(band.mean()),
                    "std": float(band.std())
                }

        return {
            "status": "success",
            "statistics": stats,
            "message": f"Band-wise statistics computed successfully."
        }

    except Exception as e:
        raise ValueError(f"Failed to compute statistics: {e}")
