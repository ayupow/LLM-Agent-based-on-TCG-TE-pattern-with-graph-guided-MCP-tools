"""Standalone tool: utilities. Auto-extracted from gis-mcp."""
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

def save_results(
    data: Dict[str, Any],
    filename: Optional[str] = None,
    formats: Optional[List[str]] = None,
    folder: str = "outputs"
) -> Dict[str, Any]:
    """
    MCP Tool: Save any GIS-MCP result dict to files, only when the user requests.

    Args:
        data: The dictionary returned by any GIS-MCP tool.
        filename: Base filename without extension.
        formats: List of formats to save (default = all).
        folder: Target folder (relative to configured storage directory, or absolute path).

    Returns:
        Dict with 'saved_files' mapping format -> path.
    """
    try:
        paths = save_output(data, filename=filename, folder=folder, formats=formats)
        return {
            "status": "success",
            "saved_files": paths,
            "message": "Results saved successfully."
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save results: {e}"}
