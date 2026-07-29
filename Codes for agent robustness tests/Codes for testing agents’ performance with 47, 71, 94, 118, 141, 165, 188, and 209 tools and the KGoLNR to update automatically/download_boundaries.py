"""Standalone tool: data. Auto-extracted from gis-mcp."""
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

def download_boundaries(region: str, level: int = 1, path: Optional[str] = None) -> Dict[str, Any]:
    """
    Download GADM administrative boundaries and save as GeoJSON.

    Args:
        region: e.g. "USA" or "United States"
        level: 0=country, 1=state, 2=county, ...
        path: custom output folder

    Returns:
        {"status": "success", "file_path": "..."} or {"status": "error", "message": "..."}
    """
    try:
        if not _pygadm_available:
            raise ImportError("pygadm is not installed. Please install with 'pip install gis-mcp[administrative-boundaries]'.")
        region = ALIASES.get(region.upper(), region)  
        if path:
            out_dir = resolve_path(path, relative_to_storage=True)
        else:
            # Use storage path with administrative_boundaries subdirectory
            storage = get_storage_path()
            out_dir = storage / "administrative_boundaries"
        out_dir.mkdir(parents=True, exist_ok=True)

        # new pygadm API
        gdf = pygadm.AdmItems(name=region, content_level=level)

        file_name = f"{region.replace(' ', '_')}_adm{level}.geojson"
        file_path = out_dir / file_name
        gdf.to_file(file_path, driver="GeoJSON")

        logger.info("Saved %s level %s to %s", region, level, file_path)
        return {"status": "success", "file_path": str(file_path)}

    except Exception as e:
        logger.exception("Failed to download boundaries")
        return {"status": "error", "message": str(e)}
