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

def download_worldcover(
    year: int = 2021,
    collection: Optional[str] = None,
    asset_key: str = "map",
    bbox: Optional[str] = None,
    geometry_geojson: Optional[str] = None,
    out_crs: Optional[str] = "EPSG:4326",
    filename: Optional[str] = None,
    path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download ESA WorldCover (10 m) for the given AOI and year from Microsoft Planetary Computer.
    - Crops to bbox/geometry (WGS84), optional reprojection.
    - Writes a single-band categorical GeoTIFF (land cover classes).
    Notes:
      * On MPC, the collection is commonly 'esa-worldcover' with yearly items; the default here
        auto-selects by year. If your deployment uses different IDs, pass `collection` explicitly.
      * `asset_key` is typically 'map'.

    Args:
        year: WorldCover year (e.g., 2020, 2021, 2023).
        collection: STAC collection (default resolves to 'esa-worldcover').
        asset_key: Asset key to read ('map' usually).
        bbox: "minx,miny,maxx,maxy" WGS84.
        geometry_geojson: GeoJSON geometry string (WGS84).
        out_crs: Output CRS (default EPSG:4326).
        filename: Output filename (e.g., "worldcover_iran_2021.tif").
        path: Output directory.

    Returns:
        dict with status, file_path, item_id, collection, properties.
    """
    try:
        out_dir = _ensure_dir(path)
        bbox_vals = _parse_bbox(bbox) if bbox else None
        geom_obj = json.loads(geometry_geojson) if geometry_geojson else None

        coll = collection or "esa-worldcover"
        dt = f"{year}-01-01/{year}-12-31"

        item = _stac_search_one(
            collection=coll,
            intersects=geom_obj,
            bbox=bbox_vals,
            datetime=dt,
            query=None
        )

        if asset_key not in item.assets:
            raise RuntimeError(f"Asset '{asset_key}' not found in item '{item.id}'. Available: {list(item.assets.keys())}")

        data, profile = _read_clip_reproject(
            href=item.assets[asset_key].href,
            geometry_geojson=geom_obj,
            bbox_vals=bbox_vals,
            out_crs=out_crs,
            resampling=Resampling.nearest
        )

        if not filename:
            filename = f"worldcover_{year}_{item.id}.tif"
        out_path = out_dir / filename

        profile.update(count=1, dtype=data.dtype.name if hasattr(data, "dtype") else profile.get("dtype", "uint16"))
        if data.ndim == 3:
            data = data[0]

        _write_gtiff(out_path, data, profile)

        logger.info("Saved WorldCover to %s", out_path)
        return {
            "status": "success",
            "file_path": str(out_path),
            "item_id": item.id,
            "collection": coll,
            "year": year,
            "asset": asset_key,
            "properties": item.properties,
        }
    except Exception as e:
        logger.exception("Failed to download WorldCover")
        return {"status": "error", "message": str(e)}
