"""Standalone tool: visualize. Auto-extracted from gis-mcp."""
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

def create_map(
    layers: List[Dict[str, Any]],
    filename: str = "map",
    filetype: str = "png",
    title: str = None,
    show_grid: bool = True,
    add_legend: bool = True,
    output_dir: str = "outputs"
) -> Dict[str, Any]:
    """
    Create a styled map from multiple inputs (vectors, rasters, WKT, or coords).

    Args:
        layers: List of dicts, each containing "data" and "style".
            data can be: file path (.shp, .geojson, .tif), WKT string, coords, or GeoDataFrame
        filename: Output filename (without extension).
        filetype: png, pdf, jpg...
        title: Optional map title.
        show_grid: Draw a grid.
        add_legend: Add legend if labels are provided.
        output_dir: Directory to save output.
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 8))

        for layer in layers:
            data = layer.get("data")
            style = layer.get("style", {})
            label = style.pop("label", None) 

            gdf = None

            if isinstance(data, str):
                data = os.path.abspath(data)

                if data.lower().endswith(".shp") or data.lower().endswith(".geojson"):
                    gdf = gpd.read_file(data)
                elif data.lower().endswith(".tif"):
                    with rasterio.open(data) as src:
                        rioshow(src, ax=ax, **style)
                        continue
                else:
                    geom = wkt.loads(data)
                    gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")

            elif isinstance(data, gpd.GeoDataFrame):
                gdf = data

            elif isinstance(data, list):
                from shapely.geometry import Polygon, LineString, Point
                if len(data) > 2:
                    geom = Polygon(data)
                elif len(data) == 2:
                    geom = LineString(data)
                else:
                    geom = Point(data)
                gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")

            if gdf is not None:
                if "column" in style: 
                    column = style.pop("column")
                    gdf.plot(ax=ax, column=column, **style, label=label)
                else:
                    gdf.plot(ax=ax, **style, label=label)

        if title:
            ax.set_title(title, fontsize=14)
        if show_grid:
            ax.grid(True, linestyle="--", alpha=0.5)
        if add_legend:
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend()

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.abspath(os.path.join(output_dir, f"{filename}.{filetype}"))
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close(fig)

        return {
            "status": "success",
            "message": f"Map created and saved to {output_path}",
            "output_path": output_path
        }

    except Exception as e:
        return {"status": "error", "message": f"create_map failed: {str(e)}"}
