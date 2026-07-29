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

def gamma_statistic(shapefile_path: str, dependent_var: str = "LAND_USE", target_crs: str = "EPSG:4326", distance_threshold: float = 100000) -> Dict[str, Any]:
    """Compute Gamma Statistic for spatial autocorrelation."""
    gdf, y, w, (threshold, unit), err = pysal_load_data(shapefile_path, dependent_var, target_crs, distance_threshold)
    if err:
        return {"status": "error", "message": err}

    import esda
    stat = esda.Gamma(y, w)
    preview = gdf[['geometry', dependent_var]].head(5).assign(
        geometry=lambda df: df.geometry.apply(lambda g: g.wkt)
    ).to_dict(orient="records")

    # Gamma statistic - check for available attributes
    gamma_val = None
    if hasattr(stat, "G"):
        gamma_val = float(stat.G)
    elif hasattr(stat, "gamma"):
        gamma_val = float(stat.gamma)
    elif hasattr(stat, "gamma_index"):
        gamma_val = float(stat.gamma_index)
    
    p_val = None
    if hasattr(stat, "p_value"):
        p_val = float(stat.p_value)
    elif hasattr(stat, "p_sim"):
        p_val = float(stat.p_sim)
    
    return {
        "status": "success",
        "message": f"Gamma Statistic completed successfully (threshold: {threshold} {unit})",
        "result": {
            "Gamma": gamma_val,
            "p_value": p_val,
            "data_preview": preview
        }
    }
