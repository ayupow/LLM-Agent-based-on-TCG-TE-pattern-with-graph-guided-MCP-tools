"""Standalone tool: geopandas. Auto-extracted from gis-mcp."""
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

def write_file_gpd(gdf_path: str, output_path: str, driver: str = None) -> Dict[str, Any]:
    """
    Export a GeoDataFrame to a file (Shapefile, GeoJSON, GPKG, etc.).
    Args:
        gdf_path: Path to the input geospatial file.
        output_path: Path to save the exported file.
        driver: Optional OGR driver name (e.g., 'ESRI Shapefile', 'GeoJSON', 'GPKG').
    Returns:
        Dictionary with status and message.
    """
    try:
        gdf = gpd.read_file(gdf_path)
        output_path_resolved = resolve_path(output_path, relative_to_storage=True)
        output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
        kwargs = {"driver": driver} if driver else {}
        gdf.to_file(str(output_path_resolved), **kwargs)
        return {
            "status": "success",
            "message": f"GeoDataFrame exported to '{output_path_resolved}' successfully.",
            "output_path": str(output_path_resolved),
            "crs": str(gdf.crs),
            "num_features": len(gdf),
            "columns": list(gdf.columns),
        }
    except Exception as e:
        logger.error(f"Error in write_file_gpd: {str(e)}")
        return {"status": "error", "message": str(e)}
