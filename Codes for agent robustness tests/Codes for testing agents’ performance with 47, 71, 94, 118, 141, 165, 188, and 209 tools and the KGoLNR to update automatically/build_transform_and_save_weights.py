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

def build_transform_and_save_weights(
    data_path: str,
    method: str = "queen",
    id_field: Optional[str] = None,
    threshold: Optional[float] = None,
    k: Optional[int] = None,
    binary: bool = True,
    transform_type: Optional[str] = None,
    output_path: str = "weights.gal",
    format: str = "gal",
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Pipeline: Read shapefile, build spatial weights, optionally transform, and save to file.

    Parameters:
    - data_path: Path to point shapefile or GeoPackage
    - method: 'queen', 'rook', 'distance_band', 'knn'
    - id_field: Optional field name for IDs
    - threshold: Distance threshold (required if method='distance_band')
    - k: Number of neighbors (required if method='knn')
    - binary: True for binary weights, False for inverse distance (DistanceBand only)
    - transform_type: 'r', 'v', 'b', 'o', or 'd' (optional)
    - output_path: File path to save weights
    - format: 'gal' or 'gwt'
    - overwrite: Allow overwriting if file exists
    """
    try:
        # --- Step 1: Check input file ---
        if not os.path.exists(data_path):
            return {"status": "error", "message": f"Data file not found: {data_path}"}

        gdf = gpd.read_file(data_path)
        if gdf.empty:
            return {"status": "error", "message": "Input file contains no features"}

        coords = [(geom.x, geom.y) for geom in gdf.geometry]

        # --- Step 2: Build weights ---
        import libpysal
        method = (method or "").lower()
        if method == "queen":
            w = libpysal.weights.Queen.from_dataframe(gdf, idVariable=id_field)
        elif method == "rook":
            w = libpysal.weights.Rook.from_dataframe(gdf, idVariable=id_field)
        elif method == "distance_band":
            if threshold is None:
                return {"status": "error", "message": "Threshold is required for distance_band method"}
            if id_field and id_field in gdf.columns:
                ids = gdf[id_field].tolist()
                w = libpysal.weights.DistanceBand(coords, threshold=threshold, binary=binary, ids=ids)
            else:
                w = libpysal.weights.DistanceBand(coords, threshold=threshold, binary=binary)
        elif method == "knn":
            if k is None:
                return {"status": "error", "message": "k is required for knn method"}
            if id_field and id_field in gdf.columns:
                ids = gdf[id_field].tolist()
                w = libpysal.weights.KNN(coords, k=k, ids=ids)
            else:
                w = libpysal.weights.KNN(coords, k=k)
        else:
            return {"status": "error", "message": f"Unsupported method: {method}"}

        # --- Step 3: Apply transformation if given ---
        if transform_type:
            transform_type = (transform_type or "").lower()
            if transform_type not in {"r", "v", "b", "o", "d"}:
                return {"status": "error", "message": f"Invalid transform type: {transform_type}"}
            w.transform = transform_type

        # --- Step 4: Save weights to file ---
        format = (format or "").lower()
        if format not in {"gal", "gwt"}:
            return {"status": "error", "message": f"Invalid format: {format}"}

        if not output_path.lower().endswith(f".{format}"):
            output_path += f".{format}"

        if os.path.exists(output_path) and not overwrite:
            return {"status": "error", "message": f"File already exists: {output_path}. Set overwrite=True to replace it."}

        w.to_file(output_path, format=format)

        # --- Step 5: Build result ---
        return {
            "status": "success",
            "message": f"{method} weights built and saved successfully",
            "result": {
                "path": output_path,
                "format": format,
                "n": int(w.n),
                "transform": getattr(w, "transform", None),
                "islands": list(w.islands) if hasattr(w, "islands") else [],
            },
        }

    except Exception as e:
        logger.error(f"Error in build_transform_and_save_weights: {str(e)}")
        return {"status": "error", "message": f"Failed to build and save weights: {str(e)}"}
