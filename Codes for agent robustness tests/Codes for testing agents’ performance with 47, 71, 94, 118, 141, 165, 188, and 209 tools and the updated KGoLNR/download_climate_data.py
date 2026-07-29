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

def download_climate_data(
    variable: str,
    year: str,
    month: str,
    day: str,
    time: str = "12:00",
    dataset: str = "reanalysis-era5-single-levels",
    format: str = "netcdf",
    path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Download climate data (ERA5 or other CDS datasets).

    Args:
        variable: e.g. "2m_temperature", "total_precipitation"
        year: e.g. "2024"
        month: "01".."12"
        day: "01".."31"
        time: Time of day (default: "12:00")
        dataset: CDS dataset name (default: "reanalysis-era5-single-levels")
        format: File format ("netcdf" or "grib")
        path: custom output folder (default: ./data/climate_data)

    Returns:
        {"status": "success", "file_path": "..."} or {"status": "error", "message": "..."}
    """
    try:
        if path:
            out_dir = resolve_path(path, relative_to_storage=True)
        else:
            # Use storage path with climate_data subdirectory
            storage = get_storage_path()
            out_dir = storage / "climate_data"
        out_dir.mkdir(parents=True, exist_ok=True)

        client = cdsapi.Client()

        file_path = out_dir / f"{dataset}_{variable}_{year}{month}{day}.{ 'nc' if format == 'netcdf' else 'grib'}"

        client.retrieve(
            dataset,
            {
                "variable": variable,
                "year": year,
                "month": month,
                "day": day,
                "time": time,
                "format": format,
            },
            str(file_path),
        )

        logger.info("Saved climate data %s for %s-%s-%s to %s",
                    variable, year, month, day, file_path)

        return {"status": "success", "file_path": str(file_path)}

    except Exception as e:
        logger.exception("Failed to download climate data")
        return {"status": "error", "message": str(e)}
