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

def get_species_info(scientific_name: str) -> Dict[str, Any]:
    """
    Retrieve taxonomic information for a given species name.
    Args:
        scientific_name: Scientific name of the species (e.g., "Puma concolor")
    Returns:
        Taxonomic info dict or error message.
    """
    try:
        result = species.name_backbone(name=scientific_name)
        logger.info("Retrieved species info for %s: %s", scientific_name, result)
        return {"status": "success", "species_info": result}
    except Exception as e:
        logger.exception("Failed to retrieve species info")
        return {"status": "error", "message": str(e)}
