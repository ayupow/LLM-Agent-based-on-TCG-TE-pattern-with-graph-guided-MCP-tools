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

def hillshade(raster_path: str, azimuth: float = 315, angle_altitude: float = 45, output_path: str = None) -> Dict[str, Any]:
    """
    Generate hillshade from a DEM raster.
    Args:
        raster_path: Path to the DEM raster.
        azimuth: Sun azimuth angle in degrees.
        angle_altitude: Sun altitude angle in degrees.
        output_path: Optional path to save the hillshade raster.
    Returns:
        Dictionary with status, message, and output path if saved.
    """
    try:
        import rasterio
        import numpy as np
        with rasterio.open(raster_path) as src:
            elevation = src.read(1).astype('float32')
            profile = src.profile.copy()
            x, y = np.gradient(elevation, src.res[0], src.res[1])
            slope = np.pi/2 - np.arctan(np.sqrt(x*x + y*y))
            aspect = np.arctan2(-x, y)
            az = np.deg2rad(azimuth)
            alt = np.deg2rad(angle_altitude)
            shaded = np.sin(alt) * np.sin(slope) + np.cos(alt) * np.cos(slope) * np.cos(az - aspect)
            hillshade = np.clip(255 * shaded, 0, 255).astype('uint8')
        if output_path:
            output_path_resolved = resolve_path(output_path, relative_to_storage=True)
            output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
            profile.update(dtype='uint8', count=1)
            with rasterio.open(str(output_path_resolved), "w", **profile) as dst:
                dst.write(hillshade, 1)
            output_path = str(output_path_resolved)
        return {
            "status": "success",
            "message": "Hillshade generated successfully.",
            "output_path": output_path
        }
    except Exception as e:
        logger.error(f"Error in hillshade: {str(e)}")
        return {"status": "error", "message": str(e)}
