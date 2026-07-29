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

def distance_band_weights(
    data_path: str,
    threshold: float,
    binary: bool = True,
    id_field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a distance-based spatial weights (W) object from point data.

    - data_path: path to point shapefile or GeoPackage
    - threshold: distance threshold for neighbors (in CRS units, e.g., meters)
    - binary: True for binary weights, False for inverse distance weights
    - id_field: optional attribute name to use as observation IDs
    """
    try:
        if not os.path.exists(data_path):
            return {"status": "error", "message": f"Data file not found: {data_path}"}

        gdf = gpd.read_file(data_path)

        if gdf.empty:
            return {"status": "error", "message": "Input file contains no features"}

        # Extract coordinates
        coords = [(geom.x, geom.y) for geom in gdf.geometry]

        # Create DistanceBand weights
        import libpysal
        if id_field and id_field in gdf.columns:
            ids = gdf[id_field].tolist()
            w = libpysal.weights.DistanceBand(coords, threshold=threshold, binary=binary, ids=ids)
        else:
            w = libpysal.weights.DistanceBand(coords, threshold=threshold, binary=binary)

        ids = w.id_order
        neighbor_counts = [w.cardinalities[i] for i in ids]
        islands = list(w.islands) if hasattr(w, "islands") else []

        # Previews - convert to native Python types immediately
        preview_ids = ids[:5]
        neighbors_preview = {}
        weights_preview = {}
        for i in preview_ids:
            # Convert neighbor IDs and weights to native Python types
            neighbors = w.neighbors.get(i, [])
            weights_list = w.weights.get(i, [])
            neighbors_preview[i] = [int(n) if isinstance(n, (np.integer, np.int32, np.int64)) else n for n in neighbors]
            weights_preview[i] = [float(w_val) if isinstance(w_val, (np.floating, np.float32, np.float64)) else (int(w_val) if isinstance(w_val, (np.integer, np.int32, np.int64)) else w_val) for w_val in weights_list]

        result = {
            "n": int(w.n),
            "id_count": int(len(ids)),
            "threshold": float(threshold),
            "binary": bool(binary),
            "id_field": id_field,
            "neighbors_stats": {
                "min": int(min(neighbor_counts)) if neighbor_counts else 0,
                "max": int(max(neighbor_counts)) if neighbor_counts else 0,
                "mean": float(np.mean(neighbor_counts)) if neighbor_counts else 0.0,
            },
            "islands": [int(i) if isinstance(i, (np.integer, np.int32, np.int64)) else i for i in islands],
            "neighbors_preview": neighbors_preview,
            "weights_preview": weights_preview,
        }

        # Convert numpy types to native Python types for serialization (recursive)
        def convert_numpy_types(obj):
            """Recursively convert numpy types to native Python types."""
            if obj is None:
                return None
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_numpy_types(item) for item in obj]
            elif isinstance(obj, (np.integer, np.int32, np.int64, np.int8, np.int16)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float32, np.float64, np.float16)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
                # Handle other iterable types
                return [convert_numpy_types(item) for item in obj]
            else:
                return obj
        
        result = convert_numpy_types(result)

        return {
            "status": "success",
            "message": "DistanceBand spatial weights constructed successfully",
            "result": result,
            "weights_info": result,  # Also include as weights_info for test compatibility
        }

    except Exception as e:
        logger.error(f"Error creating DistanceBand weights: {str(e)}")
        return {"status": "error", "message": f"Failed to create DistanceBand weights: {str(e)}"}
