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


def dynamic_lisa(
    shapefile_path: str,
    value_columns: Union[str, List[str]],   # exactly two columns: [t0, t1]
    target_crs: str = "EPSG:4326",
    weights_method: str = "queen",          # 'queen'|'rook'|'distance'
    distance_threshold: float = 100000,     # meters (converted to degrees if 4326)
    k: int = 8,                             # number of rose sectors
    permutations: int = 99,                 # 0 = skip inference
    alternative: str = "two.sided",         # 'two.sided'|'positive'|'negative'
    relative: bool = True,                  # divide each column by its mean
    drop_na: bool = True                    # drop features with NA in either column
) -> Dict[str, Any]:
    """Run dynamic LISA (directional LISA) with giddy.directional.Rose.

    Returns sector counts, angles, vector lengths, and (optionally) permutation p-values.
    """
    try:
        # --- sanitize ---
        for s in ("shapefile_path","target_crs","weights_method","alternative"):
            v = locals()[s]
            if isinstance(v, str):
                locals()[s] = v.replace("`","")

        if isinstance(value_columns, str):
            cols = [c.strip() for c in value_columns.replace("`","").split(",") if c.strip()]
        else:
            cols = list(value_columns)

        if not os.path.exists(shapefile_path):
            return {"status":"error","message":f"Shapefile not found: {shapefile_path}"}
        if len(cols) != 2:
            return {"status":"error","message":"value_columns must be exactly two columns: [start_time, end_time]."}

        # --- load + project ---
        gdf = gpd.read_file(shapefile_path)
        missing = [c for c in cols if c not in gdf.columns]
        if missing:
            return {"status":"error","message":f"Columns not found: {missing}"}
        gdf = gdf.to_crs(target_crs)

        # --- prepare Y (n x 2) ---
        Y = gdf[cols].astype(float).to_numpy(copy=True)
        if drop_na:
            mask = ~np.any(np.isnan(Y), axis=1)
            gdf = gdf.loc[mask].reset_index(drop=True)
            Y = Y[mask, :]

        if relative:
            col_means = Y.mean(axis=0)
            col_means[col_means == 0] = 1.0
            Y = Y / col_means

        # --- spatial weights ---
        import libpysal
        wm = weights_method.lower()
        if wm == "queen":
            w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
        elif wm == "rook":
            w = libpysal.weights.Rook.from_dataframe(gdf, use_index=True)
        elif wm == "distance":
            thr = distance_threshold
            if target_crs.upper() == "EPSG:4326":
                thr = distance_threshold / 111000.0  # meters → degrees
            w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=thr, binary=False)
        else:
            return {"status":"error","message":f"Unknown weights_method: {weights_method}"}
        w.transform = "r"

        # drop islands (units with no neighbors)
        if w.islands:
            keep = [i for i in range(gdf.shape[0]) if i not in set(w.islands)]
            if not keep:
                return {"status":"error","message":"All units are islands under current weights."}
            gdf = gdf.iloc[keep].reset_index(drop=True)
            Y = Y[keep, :]
            if wm == "queen":
                w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
            elif wm == "rook":
                w = libpysal.weights.Rook.from_dataframe(gdf, use_index=True)
            else:
                thr = distance_threshold if target_crs.upper() != "EPSG:4326" else distance_threshold/111000.0
                w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=thr, binary=False)
            w.transform = "r"

        # --- Dynamic LISA (Rose) ---
        from giddy.directional import Rose
        rose = Rose(Y, w, k=int(k))  # computes cuts, counts, theta, r, bins, lag internally

        # permutation inference (optional)
        pvals = None
        expected_perm = larger_perm = smaller_perm = None
        if permutations and permutations > 0:
            rose.permute(permutations=int(permutations), alternative=alternative)
            pvals = np.asarray(getattr(rose, "p", None)).tolist() if hasattr(rose, "p") else None
            expected_perm = np.asarray(getattr(rose, "expected_perm", [])).tolist()
            larger_perm = np.asarray(getattr(rose, "larger_perm", [])).tolist()
            smaller_perm = np.asarray(getattr(rose, "smaller_perm", [])).tolist()

        # preview
        def _wkt_safe(g):
            try:
                return g.wkt
            except Exception:
                return str(g)

        preview = gdf[[*cols, gdf.geometry.name]].head(5).copy()
        preview[gdf.geometry.name] = preview[gdf.geometry.name].apply(_wkt_safe)
        preview = preview.rename(columns={gdf.geometry.name: "geometry_wkt"}).to_dict(orient="records")

        result = {
            "n_regions": int(Y.shape[0]),
            "k_sectors": int(k),
            "weights_method": wm,
            "value_columns": cols,
            "cuts_radians": np.asarray(rose.cuts).tolist(),        # sector edges
            "sector_counts": np.asarray(rose.counts).tolist(),     # count per sector
            "angles_theta_rad": np.asarray(rose.theta).tolist(),   # one per region
            "vector_lengths_r": np.asarray(rose.r).tolist(),       # one per region
            "bins_used": np.asarray(rose.bins).tolist(),
            "inference": {
                "permutations": int(permutations),
                "alternative": alternative,
                "p_values_by_sector": pvals,
                "expected_counts_perm": expected_perm,
                "larger_or_equal_counts": larger_perm,
                "smaller_or_equal_counts": smaller_perm
            },
            "data_preview": preview
        }

        msg = "Dynamic LISA (Rose) completed successfully"
        if wm == "distance" and target_crs.upper() == "EPSG:4326":
            msg += f" (threshold interpreted as {distance_threshold/111000.0:.6f} degrees)."

        return {"status":"success","message":msg,"result":result}

    except Exception as e:
        return {"status":"error","message":f"Failed to run Dynamic LISA: {str(e)}"}
