"""Standalone tool: pysal. Auto-extracted from gis-mcp."""
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

def adbscan(shapefile_path: str, dependent_var: str = None, target_crs: str = "EPSG:4326",
            distance_threshold: float = 100000, eps: float = 0.1, min_samples: int = 5) -> Dict[str, Any]:
    """Adaptive DBSCAN clustering (requires coordinates, no dependent_var)."""
    if not os.path.exists(shapefile_path):
        return {"status": "error", "message": f"Shapefile not found: {shapefile_path}"}
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs(target_crs)

    coords = np.array(list(gdf.geometry.apply(lambda g: (g.x, g.y))))
    import esda
    # ADBSCAN constructor - check actual signature to avoid parameter conflicts
    # Try different calling patterns based on actual API
    try:
        # First try: eps and min_samples as keyword arguments
        stat = esda.adbscan.ADBSCAN(coords, eps=eps, min_samples=min_samples)
    except TypeError as e:
        if "multiple values for argument 'eps'" in str(e):
            # eps might be positional - try as positional argument
            try:
                stat = esda.adbscan.ADBSCAN(coords, eps, min_samples)
            except Exception:
                # Last resort: try with just coords and keyword args without eps
                stat = esda.adbscan.ADBSCAN(coords, min_samples=min_samples)
        else:
            raise

    preview = gdf[['geometry']].head(5).copy()
    preview['geometry'] = preview['geometry'].apply(lambda g: g.wkt)

    # ADBSCAN attributes - check for available attributes
    labels_val = None
    if hasattr(stat, "labels_"):
        labels_val = stat.labels_.tolist() if hasattr(stat.labels_, "tolist") else list(stat.labels_)
    elif hasattr(stat, "labels"):
        labels_val = stat.labels.tolist() if hasattr(stat.labels, "tolist") else list(stat.labels)
    
    core_indices_val = None
    if hasattr(stat, "core_sample_indices_"):
        core_indices_val = stat.core_sample_indices_.tolist() if hasattr(stat.core_sample_indices_, "tolist") else list(stat.core_sample_indices_)
    elif hasattr(stat, "core_sample_indices"):
        core_indices_val = stat.core_sample_indices.tolist() if hasattr(stat.core_sample_indices, "tolist") else list(stat.core_sample_indices)
    
    components_val = None
    if hasattr(stat, "components_"):
        components_val = stat.components_.tolist() if hasattr(stat.components_, "tolist") else list(stat.components_)
    elif hasattr(stat, "components"):
        components_val = stat.components.tolist() if hasattr(stat.components, "tolist") else list(stat.components)
    
    return {
        "status": "success",
        "message": f"A-DBSCAN clustering completed successfully (eps={eps}, min_samples={min_samples})",
        "result": {
            "labels": labels_val,
            "core_sample_indices": core_indices_val,
            "components": components_val,
            "data_preview": preview.to_dict(orient="records")
        }
    }
