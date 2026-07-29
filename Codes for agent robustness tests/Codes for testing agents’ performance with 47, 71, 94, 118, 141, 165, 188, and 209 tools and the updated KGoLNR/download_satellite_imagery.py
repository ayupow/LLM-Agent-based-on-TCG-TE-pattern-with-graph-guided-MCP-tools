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

def download_satellite_imagery(
    collection: str = "sentinel-2-l2a",
    assets: Union[List[str], str] = ("B04", "B03", "B02"),
    datetime: str = "2024-01-01/2024-12-31",
    cloud_cover_lt: Optional[int] = 20,
    bbox: Optional[str] = None, 
    geometry_geojson: Optional[str] = None,
    out_crs: Optional[str] = None,
    filename: Optional[str] = None,
    path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Download analysis-ready satellite imagery from Microsoft Planetary Computer (STAC + SAS).
    - Picks the least-cloudy item matching your query (by default Sentinel-2 L2A).
    - Downloads specified asset bands and writes a multi-band GeoTIFF.
    - Optional bbox/geometry crop and CRS reprojection.

    Args:
        collection: STAC collection id (e.g., "sentinel-2-l2a", "landsat-8-c2-l2")
        assets: list of asset keys to download (e.g., ["B04","B03","B02"])
        datetime: STAC datetime/interval (e.g., "2025-08-01/2025-08-31" or "2025-08-05")
        cloud_cover_lt: only items with eo:cloud_cover < this value. Use None to disable.
        bbox: "minx,miny,maxx,maxy" (in degrees if using search with WGS84). Used for cropping window.
        geometry_geojson: a GeoJSON geometry (string). If provided, precise clipping is applied.
        out_crs: target CRS for output (e.g., "EPSG:4326"). If None, keep source asset CRS.
        filename: output file name (without path). If None, an automatic name is generated.
        path: output folder. Defaults to ./data/satellite_imagery

    Returns:
        {"status": "success", "file_path": "...", "item_id": "...", "collection": "...", "assets": [...], "properties": {...}}
        or {"status": "error", "message": "..."}
    """
    try:
        if isinstance(assets, str):
            assets = [a.strip() for a in assets.split(",") if a.strip()]

        out_dir = _ensure_dir(path)
        bbox_vals = _parse_bbox(bbox) if bbox else None
        geom_obj = json.loads(geometry_geojson) if geometry_geojson else None

        item = _pick_item(
            collection=collection,
            bbox=bbox_vals,
            datetime=datetime,
            cloud_cover=cloud_cover_lt,
            intersects=geom_obj 
        )
        if geom_obj and not bbox_vals:
            minx, miny, maxx, maxy = shapely_shape(geom_obj).bounds
            bbox_vals = [minx, miny, maxx, maxy]

        bands = []
        profiles = []
        missing_assets = []
        for asset_key in assets:
            if asset_key not in item.assets:
                missing_assets.append(asset_key)
                continue

            href = item.assets[asset_key].href
            data, profile = _read_and_optionally_clip(
                href=href,
                bbox=bbox_vals,
                geometry_geojson=geom_obj,
                out_crs=out_crs
            )
            bands.append(data)
            profiles.append(profile)

        if missing_assets:
            logger.warning("Missing assets in item %s: %s", item.id, ", ".join(missing_assets))
            if not bands:
                raise RuntimeError(f"Requested assets not available in the chosen item: {missing_assets}")

        if not filename:
            safe_assets = "-".join([a.lower() for a in assets if a not in missing_assets]) or "bands"
            filename = f"{collection}_{item.id}_{safe_assets}.tif"
        out_path = out_dir / filename

        dtype = profiles[0].get("dtype")

        _write_multiband_geotiff(out_path=out_path, bands=bands, profiles=profiles, dtype=dtype)

        logger.info("Saved satellite imagery (%s) to %s", assets, out_path)

        return {
            "status": "success",
            "file_path": str(out_path),
            "item_id": item.id,
            "collection": collection,
            "assets": [a for a in assets if a not in missing_assets],
            "missing_assets": missing_assets,
            "properties": item.properties,
        }

    except Exception as e:
        logger.exception("Failed to download satellite imagery")
        return {"status": "error", "message": str(e)}
