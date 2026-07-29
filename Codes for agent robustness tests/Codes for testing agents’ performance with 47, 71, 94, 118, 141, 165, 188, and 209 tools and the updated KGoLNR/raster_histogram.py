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

def raster_histogram(
    source: str,
    bins: int = 256
) -> Dict[str, Any]:
    """
    Compute histogram of pixel values for each band.

    Parameters:
    - source: path to input raster.
    - bins:   number of histogram bins.
    """
    try:
        import rasterio
        import numpy as np
        import os

        src_path = os.path.expanduser(source.replace("`", ""))
        histograms = {}

        with rasterio.open(src_path) as src:
            for i in range(1, src.count + 1):
                band = src.read(i, masked=True)
                hist, bin_edges = np.histogram(band.compressed(), bins=bins)
                histograms[f"Band {i}"] = {
                    "histogram": hist.tolist(),
                    "bin_edges": bin_edges.tolist()
                }

        return {
            "status": "success",
            "histograms": histograms,
            "message": f"Histogram computed for all bands."
        }

    except Exception as e:
        raise ValueError(f"Failed to compute histogram: {e}")
