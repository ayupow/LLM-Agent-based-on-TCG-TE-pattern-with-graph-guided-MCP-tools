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

def clip_raster_with_shapefile(
    raster_path_or_url: str,
    shapefile_path: str,
    destination: str
) -> Dict[str, Any]:
    """
    Clip a raster dataset using polygons from a shapefile and write the result.
    Converts the shapefile's CRS to match the raster's CRS if they are different.
    
    Parameters:
    - raster_path_or_url: local path or HTTPS URL of the source raster.
    - shapefile_path:     local filesystem path to a .shp file containing polygons.
    - destination:        local path where the masked raster will be written.
    """
    try:
        import numpy as np
        import rasterio
        import rasterio.mask
        from rasterio.warp import transform_geom
        import pyproj
        import fiona

        # Clean paths
        raster_clean = raster_path_or_url.replace("`", "")
        shp_clean = shapefile_path.replace("`", "")
        dst_clean = destination.replace("`", "")

        # Verify shapefile exists
        shp_path = os.path.expanduser(shp_clean)
        if not os.path.isfile(shp_path):
            raise FileNotFoundError(f"Shapefile not found at '{shp_path}'.")

        # Open the raster
        if raster_clean.lower().startswith("https://"):
            src = rasterio.open(raster_clean)
        else:
            src_path = os.path.expanduser(raster_clean)
            if not os.path.isfile(src_path):
                raise FileNotFoundError(f"Raster not found at '{src_path}'.")
            src = rasterio.open(src_path)

        raster_crs = src.crs  # Get raster CRS

        # Read geometries from shapefile and check CRS
        with fiona.open(shp_path, "r") as shp:
            shapefile_crs = pyproj.CRS(shp.crs)  # Get shapefile CRS
            shapes: List[Dict[str, Any]] = [feat["geometry"] for feat in shp]

            # Convert geometries to raster CRS if necessary
            if shapefile_crs != raster_crs:
                shapes = [transform_geom(str(shapefile_crs), str(raster_crs), shape) for shape in shapes]

        # Apply mask: crop to shapes and set outside pixels to zero
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta.copy()
        src.close()

        # Update metadata for the masked output
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # Resolve destination path relative to storage
        dst_path = resolve_path(dst_clean, relative_to_storage=True)
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the masked raster
        with rasterio.open(str(dst_path), "w", **out_meta) as dst:
            dst.write(out_image)

        return {
            "status": "success",
            "destination": str(dst_path),
            "message": f"Raster masked and saved to '{dst_path}'."
        }

    except Exception as e:
        print(f"Error: {e}")
        raise ValueError(f"Failed to mask raster: {e}")
