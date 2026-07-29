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

def overlay_gpd(gdf1_path: str, gdf2_path: str, how: str = "intersection", output_path: str = None) -> Dict[str, Any]:
    """
    Overlay two GeoDataFrames using geopandas.overlay.
    Args:
        gdf1_path: Path to the first geospatial file.
        gdf2_path: Path to the second geospatial file.
        how: Overlay method ('intersection', 'union', 'identity', 'symmetric_difference', 'difference').
        output_path: Optional path to save the result.
    Returns:
        Dictionary with status, message, and output info.
    """
    try:
        gdf1 = gpd.read_file(gdf1_path)
        gdf2 = gpd.read_file(gdf2_path)
        if gdf1.crs != gdf2.crs:
            gdf2 = gdf2.to_crs(gdf1.crs)
        result = gpd.overlay(gdf1, gdf2, how=how)
        if output_path:
            output_path_resolved = resolve_path(output_path, relative_to_storage=True)
            output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
            result.to_file(str(output_path_resolved))
            output_path = str(output_path_resolved)
        # Convert geometry to WKT for serialization
        preview_df = result.head(5).copy()
        if 'geometry' in preview_df.columns:
            preview_df['geometry'] = preview_df['geometry'].apply(lambda g: g.wkt if g is not None else None)
        preview = preview_df.to_dict(orient="records")
        return {
            "status": "success",
            "message": f"Overlay ({how}) completed successfully.",
            "num_features": len(result),
            "crs": str(result.crs),
            "columns": list(result.columns),
            "preview": preview,
            "output_path": output_path,
        }
    except Exception as e:
        logger.error(f"Error in overlay_gpd: {str(e)}")
        return {"status": "error", "message": str(e)}
