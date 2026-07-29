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

def compute_s2_ndvi(
    datetime: str = "2024-07-01/2024-07-15",
    cloud_cover_lt: Optional[int] = 20,
    bbox: Optional[str] = None,
    geometry_geojson: Optional[str] = None,
    out_crs: Optional[str] = "EPSG:4326",
    filename: Optional[str] = None,
    path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compute NDVI from Sentinel-2 L2A (B08=NIR, B04=Red) for an AOI/time window via MPC.
    - Picks a low-cloud item intersecting the AOI.
    - Clips to AOI and writes single-band NDVI GeoTIFF scaled to float32 (-1..1).

    Args:
        datetime: STAC datetime/interval (e.g., "2024-07-01/2024-07-15").
        cloud_cover_lt: Only consider items with eo:cloud_cover < value. Use None to disable.
        bbox: "minx,miny,maxx,maxy" (WGS84).
        geometry_geojson: GeoJSON geometry (WGS84).
        out_crs: Output CRS for NDVI raster.
        filename: Output filename (default auto-generated).
        path: Output directory.

    Returns:
        dict with status, file_path, item_id, collection, properties.
    """
    try:
        out_dir = _ensure_dir(path)
        bbox_vals = _parse_bbox(bbox) if bbox else None
        geom_obj = json.loads(geometry_geojson) if geometry_geojson else None

        collection = "sentinel-2-l2a"
        query = {"eo:cloud_cover": {"lt": cloud_cover_lt}} if cloud_cover_lt is not None else None

        item = _stac_search_one(
            collection=collection,
            intersects=geom_obj,
            bbox=bbox_vals,
            datetime=datetime,
            query=query
        )

        need_assets = {"B08": "NIR", "B04": "RED"}
        hrefs = {}
        for k in need_assets.keys():
            if k not in item.assets:
                raise RuntimeError(f"Sentinel-2 asset '{k}' not available in item '{item.id}'.")
            hrefs[k] = item.assets[k].href

        nir, nir_profile = _read_clip_reproject(
            href=hrefs["B08"], geometry_geojson=geom_obj, bbox_vals=bbox_vals, out_crs=out_crs,
            resampling=Resampling.bilinear
        )
        red, red_profile = _read_clip_reproject(
            href=hrefs["B04"], geometry_geojson=geom_obj, bbox_vals=bbox_vals, out_crs=out_crs,
            resampling=Resampling.bilinear
        )

        nir_arr = nir[0] if nir.ndim == 3 else nir
        red_arr = red[0] if red.ndim == 3 else red

        if nir_arr.shape != red_arr.shape:
            raise RuntimeError(f"Band shape mismatch after processing: NIR{nir_arr.shape} vs RED{red_arr.shape}")

        nir_arr = nir_arr.astype("float32")
        red_arr = red_arr.astype("float32")
        denom = (nir_arr + red_arr)
        ndvi = (nir_arr - red_arr) / np.where(denom == 0, np.nan, denom)
        ndvi = np.nan_to_num(ndvi, nan=0.0).astype("float32")

        out_profile = nir_profile.copy()
        out_profile.update(count=1, dtype="float32", nodata=np.float32(0.0))

        if not filename:
            filename = f"s2_ndvi_{item.id}.tif"
        out_path = out_dir / filename

        _write_gtiff(out_path, ndvi, out_profile)

        logger.info("Saved NDVI to %s", out_path)
        return {
            "status": "success",
            "file_path": str(out_path),
            "item_id": item.id,
            "collection": collection,
            "assets": ["B08", "B04"],
            "properties": item.properties,
        }
    except Exception as e:
        logger.exception("Failed to compute NDVI")
        return {"status": "error", "message": str(e)}
