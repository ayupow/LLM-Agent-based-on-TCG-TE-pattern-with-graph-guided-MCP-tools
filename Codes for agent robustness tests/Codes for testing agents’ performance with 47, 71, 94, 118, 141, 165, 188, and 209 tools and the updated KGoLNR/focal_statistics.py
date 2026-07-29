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

def focal_statistics(raster_path: str, statistic: str, size: int = 3, output_path: str = None) -> Dict[str, Any]:
    """
    Compute focal (moving window) statistics on a raster.
    Args:
        raster_path: Path to the input raster.
        statistic: Statistic to compute ('mean', 'min', 'max', 'std').
        size: Window size (odd integer).
        output_path: Optional path to save the result.
    Returns:
        Dictionary with status, message, and output path if saved.
    """
    try:
        import rasterio
        import numpy as np
        from scipy.ndimage import generic_filter
        with rasterio.open(raster_path) as src:
            data = src.read(1)
            profile = src.profile.copy()
            func = None
            if statistic == "mean":
                func = np.mean
            elif statistic == "min":
                func = np.min
            elif statistic == "max":
                func = np.max
            elif statistic == "std":
                func = np.std
            else:
                raise ValueError(f"Unsupported statistic: {statistic}")
            filtered = generic_filter(data, func, size=size, mode='nearest')
        if output_path:
            output_path_resolved = resolve_path(output_path, relative_to_storage=True)
            output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
            with rasterio.open(str(output_path_resolved), "w", **profile) as dst:
                dst.write(filtered, 1)
            output_path = str(output_path_resolved)
        return {
            "status": "success",
            "message": f"Focal {statistic} computed successfully.",
            "output_path": output_path
        }
    except Exception as e:
        logger.error(f"Error in focal_statistics: {str(e)}")
        return {"status": "error", "message": str(e)}
