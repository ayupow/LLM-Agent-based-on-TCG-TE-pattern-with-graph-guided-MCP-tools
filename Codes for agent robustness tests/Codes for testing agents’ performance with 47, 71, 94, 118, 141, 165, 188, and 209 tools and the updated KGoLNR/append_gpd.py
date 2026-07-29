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

def append_gpd(shapefile1_path: str, shapefile2_path: str, output_path: str) -> Dict[str, Any]:
    """ Reads two shapefiles directly, concatenates them vertically."""
    try:
        # Configure a basic logger for demonstration
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Step 1: Read the two shapefiles into GeoDataFrames.
        logger.info(f"Reading {shapefile1_path}...")
        gdf1 = gpd.read_file(shapefile1_path)
        
        logger.info(f"Reading {shapefile2_path}...")
        gdf2 = gpd.read_file(shapefile2_path)

        # Step 2: Ensure the Coordinate Reference Systems (CRS) match.
        if gdf1.crs != gdf2.crs:
            logger.warning(
                f"CRS mismatch: GDF1 has '{gdf1.crs}' and GDF2 has '{gdf2.crs}'. "
                "Reprojecting GDF2."
            )
            gdf2 = gdf2.to_crs(gdf1.crs)

        # Step 3: Concatenate the two GeoDataFrames.
        combined_gdf = pd.concat([gdf1, gdf2], ignore_index=True)

        # Step 4: Save the combined GeoDataFrame to a new shapefile.
        output_path_resolved = resolve_path(output_path, relative_to_storage=True)
        output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving combined shapefile to {output_path_resolved}...")
        combined_gdf.to_file(str(output_path_resolved), driver='ESRI Shapefile')

        return {
            "status": "success",
            "message": f"Shapefiles concatenated successfully into '{output_path_resolved}'.",
            "info": {
                "output_path": str(output_path_resolved),
                "num_features": len(combined_gdf),
                "crs": str(combined_gdf.crs),
                "columns": list(combined_gdf.columns)
            }
        }
    
    except Exception as e:
        logger.error(f"Error processing shapefiles: {str(e)}")
        raise ValueError(f"Failed to process shapefiles: {str(e)}")
