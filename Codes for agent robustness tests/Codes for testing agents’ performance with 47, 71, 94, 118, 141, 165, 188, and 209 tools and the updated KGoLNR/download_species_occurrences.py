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

def download_species_occurrences(
    scientific_name: str,
    limit: int = 100,
    path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Download occurrence records for a given species and save as JSON.
    Args:
        scientific_name: Scientific name of the species (e.g., "Puma concolor")
        limit: Number of occurrence records to fetch (default: 100)
        path: Custom output folder (default: ./data/ecology_data)
    Returns:
        {"status": "success", "file_path": "..."} or {"status": "error", "message": "..."}
    """
    try:
        if path:
            out_dir = resolve_path(path, relative_to_storage=True)
        else:
            # Use storage path with ecology_data subdirectory
            storage = get_storage_path()
            out_dir = storage / "ecology_data"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Get taxon key
        species_info = species.name_backbone(name=scientific_name)
        taxon_key = species_info.get("usageKey")
        if not taxon_key:
            msg = f"Taxon key not found for {scientific_name}"
            logger.error(msg)
            return {"status": "error", "message": msg}

        # Get occurrence data
        occ_data = occurrences.search(taxonKey=taxon_key, limit=limit)
        results = occ_data.get("results", [])

        file_name = f"{scientific_name.replace(' ', '_')}_occurrences.json"
        file_path = out_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "species_info": species_info,
                "occurrence_data": results
            }, f, indent=4)

        logger.info("Saved occurrence data for %s to %s", scientific_name, file_path)
        return {"status": "success", "file_path": str(file_path)}
    except Exception as e:
        logger.exception("Failed to download species occurrences")
        return {"status": "error", "message": str(e)}
