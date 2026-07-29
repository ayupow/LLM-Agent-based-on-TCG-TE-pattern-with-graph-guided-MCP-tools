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

def weighted_band_sum(
    source: str,
    weights: List[float],
    destination: str
) -> Dict[str, Any]:
    """
    Compute a weighted sum of all bands in a raster using specified weights.

    Parameters:
    - source:      Path to the input multi-band raster file.
    - weights:     List of weights (must match number of bands and sum to 1).
    - destination: Path to save the output single-band raster.
    """
    try:
        import os
        import numpy as np
        import rasterio

        src_path = os.path.expanduser(source.replace("`", ""))
        dst_path = os.path.expanduser(destination.replace("`", ""))

        with rasterio.open(src_path) as src:
            count = src.count
            if len(weights) != count:
                raise ValueError(f"Number of weights ({len(weights)}) does not match number of bands ({count}).")

            if not np.isclose(sum(weights), 1.0, atol=1e-6):
                raise ValueError("Sum of weights must be 1.0.")

            weighted = np.zeros((src.height, src.width), dtype="float32")

            for i in range(1, count + 1):
                band = src.read(i).astype("float32")
                weighted += weights[i - 1] * band

            profile = src.profile.copy()
            profile.update(dtype="float32", count=1)

        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(weighted, 1)

        return {
            "status": "success",
            "destination": str(dst_path),
            "message": f"Weighted band sum computed and saved to '{dst_path}'."
        }

    except Exception as e:
        raise ValueError(f"Failed to compute weighted sum: {e}")
