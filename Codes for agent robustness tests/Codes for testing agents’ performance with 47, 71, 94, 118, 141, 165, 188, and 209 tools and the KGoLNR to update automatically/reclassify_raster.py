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

def reclassify_raster(raster_path: str, reclass_map: dict, output_path: str) -> Dict[str, Any]:
    """
    Reclassify raster values using a mapping dictionary.
    Args:
        raster_path: Path to the input raster.
        reclass_map: Dictionary mapping old values to new values (e.g., {1: 10, 2: 20}).
        output_path: Path to save the reclassified raster.
    Returns:
        Dictionary with status and message.
    """
    try:
        import rasterio
        import numpy as np
        with rasterio.open(raster_path) as src:
            data = src.read(1)
            profile = src.profile.copy()
            reclass_data = np.copy(data)
            for old, new in reclass_map.items():
                reclass_data[data == old] = new
        output_path_resolved = resolve_path(output_path, relative_to_storage=True)
        output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(str(output_path_resolved), "w", **profile) as dst:
            dst.write(reclass_data, 1)
        return {
            "status": "success",
            "message": f"Raster reclassified and saved to '{output_path_resolved}'.", 
            "output_path": str(output_path_resolved)
        }
    except Exception as e:
        logger.error(f"Error in reclassify_raster: {str(e)}")
        return {"status": "error", "message": str(e)}
