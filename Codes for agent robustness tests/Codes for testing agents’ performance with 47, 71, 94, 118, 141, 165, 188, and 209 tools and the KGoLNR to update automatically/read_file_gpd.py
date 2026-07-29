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

def read_file_gpd(file_path: str) -> Dict[str, Any]:
    """Reads a geospatial file and returns stats and a data preview."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        gdf = gpd.read_file(file_path)
        # Convert geometry to WKT for serialization
        preview_df = gdf.head(5).copy()
        if 'geometry' in preview_df.columns:
            preview_df['geometry'] = preview_df['geometry'].apply(lambda g: g.wkt if g is not None else None)
        preview = preview_df.to_dict(orient="records")
        
        return {
            "status": "success",
            "columns": list(gdf.columns),
            "column_types": gdf.dtypes.astype(str).to_dict(),
            "num_rows": len(gdf),
            "num_columns": gdf.shape[1],
            "crs": str(gdf.crs),
            "bounds": gdf.total_bounds.tolist(),  # [minx, miny, maxx, maxy]
            "preview": preview,
            "message": f"File loaded successfully with {len(gdf)} rows and {gdf.shape[1]} columns"
        }

    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to read file: {str(e)}"
        }
