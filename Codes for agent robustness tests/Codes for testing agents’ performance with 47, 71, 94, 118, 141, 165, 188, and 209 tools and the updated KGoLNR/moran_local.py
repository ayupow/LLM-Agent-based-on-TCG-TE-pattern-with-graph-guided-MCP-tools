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

def moran_local(shapefile_path: str, dependent_var: str = "LAND_USE", target_crs: str = "EPSG:4326",
                distance_threshold: float = 100000) -> Dict[str, Any]:
    """Local Moran's I."""
    gdf, y, w, (threshold, unit), err = pysal_load_data(shapefile_path, dependent_var, target_crs, distance_threshold)
    if err:
        return {"status": "error", "message": err}

    # Handle islands - if all points are islands, fall back to KNN weights for connectivity
    import libpysal
    if w.islands:
        if len(w.islands) == len(gdf):
            # All points are islands - fall back to KNN weights
            try:
                # Use k=4 for a 5x5 grid to ensure connectivity
                w = libpysal.weights.KNN.from_dataframe(gdf, k=4)
                w.transform = 'r'
            except Exception as e:
                return {"status": "error", "message": f"All units are islands and KNN fallback failed: {str(e)}"}
        else:
            # Some islands - filter them out
            keep_idx = [i for i in range(len(gdf)) if i not in set(w.islands)]
            if len(keep_idx) == 0:
                return {"status": "error", "message": "All units are islands (no neighbors). Try increasing distance_threshold."}
            # Filter data
            gdf_filtered = gdf.iloc[keep_idx].reset_index(drop=True)
            y_filtered = y[keep_idx]
            # Rebuild weights without islands using the same threshold
            w_filtered = libpysal.weights.DistanceBand.from_dataframe(
                gdf_filtered, 
                threshold=threshold,  # Use the effective threshold already calculated in pysal_load_data
                binary=False
            )
            w_filtered.transform = 'r'
            gdf, y, w = gdf_filtered, y_filtered, w_filtered

    import esda
    stat = esda.Moran_Local(y, w)
    preview = gdf[['geometry', dependent_var]].head(5).copy()
    preview['geometry'] = preview['geometry'].apply(lambda g: g.wkt)

    # Return local statistics array summary
    return {
        "status": "success",
        "message": f"Local Moran's I completed successfully (threshold: {threshold} {unit})",
        "result": {
            "Is": stat.Is.tolist() if hasattr(stat.Is, 'tolist') else list(stat.Is),
            "p_values": stat.p_sim.tolist() if hasattr(stat.p_sim, 'tolist') else list(stat.p_sim),
            "z_scores": stat.z_sim.tolist() if hasattr(stat.z_sim, 'tolist') else list(stat.z_sim),
            "data_preview": preview.to_dict(orient="records")
        }
    }
