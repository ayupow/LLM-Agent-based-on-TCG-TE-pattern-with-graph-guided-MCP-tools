"""Standalone tool: data. Auto-extracted from gis-mcp."""
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

def download_street_network(place: str, network_type: str = "drive", file_path: str = None, custom_filter: str = None) -> Dict[str, Any]:
    """
    Download a street network for a given place using OSMnx.
    Args:
        place: Name of the place (e.g., "Los Angeles, California, USA")
        network_type: Type of network ("drive", "walk", "bike", etc.). Ignored if custom_filter is provided.
        file_path: Optional. Full path where the GraphML file will be saved. If not set, saves to default location.
        custom_filter: Optional. OSMnx custom filter string to specify which roads to download (e.g., '["highway"~"motorway|trunk|primary"]').
    Returns:
        NetworkX graph as GraphML file path or error message.
    """
    try:
        if custom_filter is not None:
            G = ox.graph_from_place(place, custom_filter=custom_filter)
        else:
            G = ox.graph_from_place(place, network_type=network_type)
        if file_path is not None:
            file_path = resolve_path(file_path, relative_to_storage=True)
            file_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # Use storage path with movement_data subdirectory
            storage = get_storage_path()
            out_dir = storage / "movement_data"
            out_dir.mkdir(parents=True, exist_ok=True)
            file_path = out_dir / f"{place.replace(',', '').replace(' ', '_')}_{network_type if custom_filter is None else 'custom'}.graphml"
        ox.save_graphml(G, file_path)
        logger.info(f"Saved street network for {place} to {file_path}")
        return {"status": "success", "file_path": str(file_path)}
    except Exception as e:
        logger.exception("Failed to download street network")
        return {"status": "error", "message": str(e)}
