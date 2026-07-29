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

def getis_ord_g(
    shapefile_path: str,
    dependent_var: str = "LAND_USE",
    target_crs: str = "EPSG:4326",
    distance_threshold: float = 100000
) -> Dict[str, Any]:
    """Compute Getis-Ord G for global hot spot analysis."""
    try:
        # Clean backticks from string parameters
        shapefile_path = shapefile_path.replace("`", "")
        dependent_var = dependent_var.replace("`", "")
        target_crs = target_crs.replace("`", "")

        # Validate input file
        if not os.path.exists(shapefile_path):
            logger.error(f"Shapefile not found: {shapefile_path}")
            return {"status": "error", "message": f"Shapefile not found: {shapefile_path}"}

        # Load GeoDataFrame
        gdf = gpd.read_file(shapefile_path)
        
        # Validate dependent variable
        if dependent_var not in gdf.columns:
            logger.error(f"Dependent variable '{dependent_var}' not found in columns")
            return {"status": "error", "message": f"Dependent variable '{dependent_var}' not found in shapefile columns"}

        # Reproject to target CRS
        gdf = gdf.to_crs(target_crs)

        # Convert distance_threshold to degrees if using geographic CRS (e.g., EPSG:4326)
        effective_threshold = distance_threshold
        unit = "meters"
        if target_crs == "EPSG:4326":
            effective_threshold = distance_threshold / 111000
            unit = "degrees"

        # Extract dependent data
        dependent = gdf[dependent_var].values.astype(np.float64)

        # Create distance-based spatial weights matrix
        import libpysal
        import esda
        w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=effective_threshold, binary=False)
        w.transform = 'r'

        # Handle islands
        for island in w.islands:
            w.weights[island] = [0] * len(w.weights[island])
            w.cardinalities[island] = 0

        # Getis-Ord G
        getis = esda.G(dependent, w)

        # Prepare GeoDataFrame preview
        preview = gdf[['geometry', dependent_var]].copy()
        preview['geometry'] = preview['geometry'].apply(lambda g: g.wkt)
        preview = preview.head(5).to_dict(orient="records")

        return {
            "status": "success",
            "message": f"Getis-Ord G analysis completed successfully (distance threshold: {effective_threshold} {unit})",
            "result": {
                "shapefile_path": shapefile_path,
                "getis_ord_g": {
                    "G": float(getis.G),
                    "p_value": float(getis.p_sim),
                    "z_score": float(getis.z_sim)
                },
                "data_preview": preview
            }
        }
    
    except Exception as e:
        logger.error(f"Error performing Getis-Ord G analysis: {str(e)}")
        return {"status": "error", "message": f"Failed to perform Getis-Ord G analysis: {str(e)}"}
