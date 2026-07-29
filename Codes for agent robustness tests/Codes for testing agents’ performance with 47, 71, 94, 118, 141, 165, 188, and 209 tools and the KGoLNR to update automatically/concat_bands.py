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

def concat_bands(
    folder_path: str,
    destination: str
) -> Dict[str, Any]:
    """
    Concatenate multiple single-band raster files into one multi-band raster, 
    handling alignment issues automatically.

    Parameters:
    - folder_path:   Path to folder containing input raster files (e.g. GeoTIFFs).
    - destination:   Path to output multi-band raster file.

    Notes:
    - Files are read in sorted order by filename.
    - If rasters have mismatched CRS, resolution, or dimensions, they are aligned automatically.
    """
    try:
        import rasterio
        import numpy as np
        from rasterio.warp import reproject, calculate_default_transform, Resampling
        from glob import glob

        folder_path = os.path.expanduser(folder_path.replace("`", ""))
        dst_path = os.path.expanduser(destination.replace("`", ""))

        # Collect single-band TIFF files in folder
        files = sorted(glob(os.path.join(folder_path, "*.tif")))

        if len(files) == 0:
            raise ValueError("No .tif files found in folder.")

        # Read properties of the first file for reference
        with rasterio.open(files[0]) as ref:
            meta = ref.meta.copy()
            height, width = ref.height, ref.width
            crs = ref.crs
            transform = ref.transform
            dtype = ref.dtypes[0]

        meta.update(count=len(files), dtype=dtype)

        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

        with rasterio.open(dst_path, "w", **meta) as dst:
            for idx, fp in enumerate(files, start=1):
                with rasterio.open(fp) as src:
                    band = src.read(1)

                    # Auto-align raster if size or CRS mismatch occurs
                    if src.height != height or src.width != width or src.crs != crs or src.transform != transform:
                        new_transform, new_width, new_height = calculate_default_transform(
                            src.crs, crs, src.width, src.height, *src.bounds
                        )
                        aligned_band = np.zeros((new_height, new_width), dtype=dtype)
                        reproject(
                            source=band,
                            destination=aligned_band,
                            src_transform=src.transform,
                            src_crs=src.crs,
                            dst_transform=new_transform,
                            dst_crs=crs,
                            resampling=Resampling.bilinear
                        )
                        band = aligned_band

                    dst.write(band, idx)

        return {
            "status": "success",
            "destination": str(dst_path),
            "message": f"{len(files)} single-band rasters concatenated into '{dst_path}'."
        }

    except Exception as e:
        raise ValueError(f"Failed to concatenate rasters: {e}")
