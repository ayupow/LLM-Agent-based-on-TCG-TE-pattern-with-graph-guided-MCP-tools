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

def merge_gpd(shapefile1_path: str, shapefile2_path: str, output_path: str) -> Dict[str, Any]:
    """ 
    Merges two shapefiles based on common attribute columns,
    This function performs a database-style join, not a spatial join.
    Args:
        left_shapefile_path: Path to the left shapefile. The geometry from this file is preserved.
        right_shapefile_path: Path to the right shapefile to merge.
        output_path: Path to save the merged output shapefile.
        how: Type of merge. One of 'left', 'right', 'outer', 'inner'. Defaults to 'inner'.
        on: Column name to join on. Must be found in both shapefiles.
        left_on: Column name to join on in the left shapefile.
        right_on: Column name to join on in the right shapefile.
        suffixes: Suffix to apply to overlapping column names.
    """
    try :
        # Step 1: Read the two shapefiles directly into GeoDataFrames.
        logger.info(f"Reading left shapefile: {shapefile1_path}...")
        left_gdf = gpd.read_file(shapefile1_path)
        
        logger.info(f"Reading right shapefile: {shapefile2_path}...")
        # For an attribute join, we only need the attribute data from the right file.
        # We can drop its geometry column to make the merge cleaner and more memory-efficient.
        right_df = pd.DataFrame(gpd.read_file(shapefile2_path).drop(columns='geometry'))

         # Step 2: Perform the merge operation using pandas.merge.
        # This function correctly handles the geometry of the left GeoDataFrame.
        logger.info(f"Performing merge...")
        merged_df = pd.merge(
            left_gdf,
            right_df,
            how='inner',  # Default to inner merge
            suffixes=('_left', '_right')
        )
        
        # Convert back to GeoDataFrame to preserve geometry and CRS
        merged_gdf = gpd.GeoDataFrame(merged_df, crs=left_gdf.crs)

        if merged_gdf.empty:
            logger.warning("The merge result is empty. No matching records were found.")

        # Step 3: Save the merged GeoDataFrame to a new shapefile.
        output_path_resolved = resolve_path(output_path, relative_to_storage=True)
        output_path_resolved.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving merged shapefile to {output_path_resolved}...")
        merged_gdf.to_file(str(output_path_resolved), driver='ESRI Shapefile')

        return {
            "status": "success",
            "message": f"Shapefiles merged successfully into '{output_path_resolved}'.",
            "info": {
                "output_path": str(output_path_resolved),
                "merge_type": 'inner',
                "num_features": len(merged_gdf),
                "crs": str(merged_gdf.crs),
                "columns": list(merged_gdf.columns)
            }
        }
    except Exception as e:
        logger.error(f"Error merging shapefiles: {str(e)}")
        raise ValueError(f"Failed to merge shapefiles: {str(e)}")
