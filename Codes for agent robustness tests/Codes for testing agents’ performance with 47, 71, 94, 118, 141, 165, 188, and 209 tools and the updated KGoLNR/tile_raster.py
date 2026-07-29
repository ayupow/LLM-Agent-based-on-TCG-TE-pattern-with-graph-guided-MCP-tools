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

def tile_raster(
    source: str,
    tile_size: int,
    destination_dir: str
) -> Dict[str, Any]:
    """
    Split a raster into square tiles of a given size and save them individually.

    Parameters:
    - source:         input raster path.
    - tile_size:      size of each tile (e.g., 256 or 512).
    - destination_dir: directory to store the tiles.
    """
    try:
        import os
        import rasterio
        from rasterio.windows import Window

        src_path = os.path.expanduser(source.replace("`", ""))
        dst_dir = os.path.expanduser(destination_dir.replace("`", ""))
        os.makedirs(dst_dir, exist_ok=True)

        tile_count = 0

        with rasterio.open(src_path) as src:
            profile = src.profile.copy()
            for i in range(0, src.height, tile_size):
                for j in range(0, src.width, tile_size):
                    window = Window(j, i, tile_size, tile_size)
                    transform = src.window_transform(window)
                    data = src.read(window=window)

                    out_profile = profile.copy()
                    out_profile.update({
                        "height": data.shape[1],
                        "width": data.shape[2],
                        "transform": transform
                    })

                    tile_path = os.path.join(dst_dir, f"tile_{i}_{j}.tif")
                    with rasterio.open(tile_path, "w", **out_profile) as dst:
                        dst.write(data)

                    tile_count += 1

        return {
            "status": "success",
            "tiles_created": tile_count,
            "message": f"{tile_count} tiles created and saved in '{dst_dir}'."
        }

    except Exception as e:
        raise ValueError(f"Failed to tile raster: {e}")
