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

def weights_from_shapefile(shapefile_path: str, contiguity: str = "queen", id_field: Optional[str] = None) -> Dict[str, Any]:

    """Create a spatial weights (W) from a shapefile using contiguity.

    - contiguity: 'queen' or 'rook' (default 'queen')
    - id_field: optional attribute name to use as observation IDs
    """
    try:
        if not os.path.exists(shapefile_path):
            return {"status": "error", "message": f"Shapefile not found: {shapefile_path}"}

        contiguity_lower = (contiguity or "").lower()
        import libpysal
        if contiguity_lower == "queen":
            w = libpysal.weights.Queen.from_shapefile(shapefile_path, idVariable=id_field)
        elif contiguity_lower == "rook":
            w = libpysal.weights.Rook.from_shapefile(shapefile_path, idVariable=id_field)
        else:
            # Fallback to generic W loader if an unrecognized contiguity is provided
            w = libpysal.weights.W.from_shapefile(shapefile_path, idVariable=id_field)

        ids = w.id_order
        neighbor_counts = [w.cardinalities[i] for i in ids]
        islands = list(w.islands) if hasattr(w, "islands") else []

        preview_ids = ids[:5]
        neighbors_preview = {i: w.neighbors.get(i, []) for i in preview_ids}
        weights_preview = {i: w.weights.get(i, []) for i in preview_ids}

        result = {
            "n": int(w.n),
            "id_count": int(len(ids)),
            "id_field": id_field,
            "contiguity": contiguity_lower if contiguity_lower in {"queen", "rook"} else "generic",
            "neighbors_stats": {
                "min": int(min(neighbor_counts)) if neighbor_counts else 0,
                "max": int(max(neighbor_counts)) if neighbor_counts else 0,
                "mean": float(np.mean(neighbor_counts)) if neighbor_counts else 0.0,
            },
            "islands": islands,
            "neighbors_preview": neighbors_preview,
            "weights_preview": weights_preview,
        }

        return {
            "status": "success",
            "message": "Spatial weights constructed successfully",
            "result": result,
            "weights_info": result,  # Also include as weights_info for test compatibility
        }

    except Exception as e:
        logger.error(f"Error creating spatial weights from shapefile: {str(e)}")
        return {"status": "error", "message": f"Failed to create spatial weights: {str(e)}"}
