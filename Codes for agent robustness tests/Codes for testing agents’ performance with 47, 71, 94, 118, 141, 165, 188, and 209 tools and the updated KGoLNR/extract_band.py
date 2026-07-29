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

def extract_band(
    source: str,
    band_index: int,
    destination: str
) -> Dict[str, Any]:
    """
    Extract a specific band from a multi-band raster and save it as a single-band GeoTIFF.

    Parameters:
    - source:      path or URL of the input raster.
    - band_index:  index of the band to extract (1-based).
    - destination: path to save the extracted band raster.
    """
    try:
        import rasterio

        src_path = os.path.expanduser(source.replace("`", ""))
        dst_path = os.path.expanduser(destination.replace("`", ""))

        with rasterio.open(src_path) as src:
            if band_index < 1 or band_index > src.count:
                raise ValueError(f"Band index {band_index} is out of range. This raster has {src.count} bands.")

            band = src.read(band_index)
            profile = src.profile.copy()
            profile.update({
                "count": 1
            })

        os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)

        with rasterio.open(dst_path, "w", **profile) as dst:
            dst.write(band, 1)

        return {
            "status": "success",
            "destination": str(dst_path),
            "message": f"Band {band_index} extracted and saved to '{dst_path}'."
        }

    except Exception as e:
        raise ValueError(f"Failed to extract band: {e}")
