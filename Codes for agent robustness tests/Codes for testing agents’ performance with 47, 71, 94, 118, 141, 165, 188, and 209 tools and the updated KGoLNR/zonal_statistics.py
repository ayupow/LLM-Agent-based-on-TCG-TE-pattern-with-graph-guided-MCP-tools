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

def zonal_statistics(raster_path: str, vector_path: str, stats: list = None) -> Dict[str, Any]:
    """
    Calculate statistics of raster values within polygons (zonal statistics).
    Args:
        raster_path: Path to the raster file.
        vector_path: Path to the vector file (polygons).
        stats: List of statistics to compute (e.g., ["mean", "min", "max", "std"]).
    Returns:
        Dictionary with status, message, and statistics per polygon.
    """
    try:
        import rasterio
        import rasterio.mask
        import geopandas as gpd
        import numpy as np
        if stats is None:
            stats = ["mean", "min", "max", "std"]
        gdf = gpd.read_file(vector_path)
        with rasterio.open(raster_path) as src:
            results = []
            for idx, row in gdf.iterrows():
                geom = [row["geometry"]]
                out_image, out_transform = rasterio.mask.mask(src, geom, crop=True, filled=True)
                data = out_image[0]
                data = data[data != src.nodata] if src.nodata is not None else data
                stat_result = {"index": idx}
                if data.size == 0:
                    for s in stats:
                        stat_result[s] = None
                else:
                    if "mean" in stats:
                        stat_result["mean"] = float(np.mean(data))
                    if "min" in stats:
                        stat_result["min"] = float(np.min(data))
                    if "max" in stats:
                        stat_result["max"] = float(np.max(data))
                    if "std" in stats:
                        stat_result["std"] = float(np.std(data))
                results.append(stat_result)
        return {
            "status": "success",
            "message": "Zonal statistics computed successfully.",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in zonal_statistics: {str(e)}")
        return {"status": "error", "message": str(e)}
