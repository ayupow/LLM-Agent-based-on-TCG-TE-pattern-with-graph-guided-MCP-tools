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

def join_counts(shapefile_path: str, dependent_var: str = "LAND_USE", target_crs: str = "EPSG:4326",
                distance_threshold: float = 100000) -> Dict[str, Any]:
    """Global Binary Join Counts."""
    gdf, y, w, (threshold, unit), err = pysal_load_data(shapefile_path, dependent_var, target_crs, distance_threshold)
    if err:
        return {"status": "error", "message": err}

    # Join counts requires binary/categorical data - user must ensure y is binary (0/1 or True/False)
    import esda
    stat = esda.Join_Counts(y, w)
    preview = gdf[['geometry', dependent_var]].head(5).copy()
    preview['geometry'] = preview['geometry'].apply(lambda g: g.wkt)

    # Join_Counts attributes: J (total joins), bb, ww, bw, etc.
    join_count_val = None
    if hasattr(stat, "J"):
        join_count_val = float(stat.J)
    elif hasattr(stat, "jc"):
        join_count_val = float(stat.jc)
    elif hasattr(stat, "join_count"):
        join_count_val = float(stat.join_count)
    
    # Handle expected, variance, z_score - these might be DataFrames or scalars
    def safe_float(val):
        """Convert value to float, handling DataFrames and numpy types."""
        if val is None:
            return None
        if isinstance(val, pd.DataFrame):
            # If it's a DataFrame, extract the first value
            return float(val.iloc[0, 0]) if not val.empty else None
        if isinstance(val, (np.ndarray, list, tuple)):
            return float(val[0]) if len(val) > 0 else None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    
    expected_val = getattr(stat, "expected", None)
    variance_val = getattr(stat, "variance", None)
    z_score_val = getattr(stat, "z_score", None)
    p_val = None
    if hasattr(stat, "p_value"):
        p_val = safe_float(stat.p_value)
    elif hasattr(stat, "p_sim"):
        p_val = safe_float(stat.p_sim)
    
    return {
        "status": "success",
        "message": f"Join Counts completed successfully (threshold: {threshold} {unit})",
        "result": {
            "join_counts": join_count_val,
            "expected": safe_float(expected_val),
            "variance": safe_float(variance_val),
            "z_score": safe_float(z_score_val),
            "p_value": p_val,
            "data_preview": preview.to_dict(orient="records")
        }
    }
