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

def sjoin_nearest_gpd(left_path: str, right_path: str, how: str = "left", max_distance: float = None, output_path: str = None) -> Dict[str, Any]:
    """
    Nearest neighbor spatial join using geopandas.sjoin_nearest.
    Args:
        left_path: Path to the left geospatial file.
        right_path: Path to the right geospatial file.
        how: Type of join ('left', 'right').
        max_distance: Optional maximum search distance.
        output_path: Optional path to save the result.
    Returns:
        Dictionary with status, message, and output info.
    """
    try:
        left = gpd.read_file(left_path)
        right = gpd.read_file(right_path)
        if left.crs != right.crs:
            right = right.to_crs(left.crs)
        kwargs = {"how": how}
        if max_distance is not None:
            kwargs["max_distance"] = max_distance
        result = gpd.sjoin_nearest(left, right, **kwargs)
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
            "message": f"Nearest spatial join ({how}) completed successfully.",
            "num_features": len(result),
            "crs": str(result.crs),
            "columns": list(result.columns),
            "preview": preview,
            "output_path": output_path,
        }
    except Exception as e:
        logger.error(f"Error in sjoin_nearest_gpd: {str(e)}")
        return {"status": "error", "message": str(e)}
