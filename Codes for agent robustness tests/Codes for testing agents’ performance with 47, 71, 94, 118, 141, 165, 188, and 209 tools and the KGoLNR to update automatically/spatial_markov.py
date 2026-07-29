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


def spatial_markov(
    shapefile_path: str,
    value_columns: Union[str, List[str]],   # time-ordered, oldest -> newest
    target_crs: str = "EPSG:4326",
    weights_method: str = "queen",          # 'queen'|'rook'|'distance'
    distance_threshold: float = 100000,     # meters (converted to degrees if 4326)
    k: int = 5,                             # classes for y (quantile bins if continuous)
    m: int = 5,                             # classes for spatial lags
    fixed: bool = True,                     # pooled quantiles across all periods
    permutations: int = 0,                  # >0 to get randomization p-values for x2
    relative: bool = True,                  # divide each period by its mean
    drop_na: bool = True,                   # drop features with any NA across time columns
    fill_empty_classes: bool = True         # handle empty bins by making them self-absorbing
) -> Dict[str, Any]:
    """Run giddy Spatial Markov on a panel (n regions x t periods) from a shapefile."""
    try:
        # --- sanitize ---
        for s in ("shapefile_path","target_crs","weights_method"):
            v = locals()[s]
            if isinstance(v, str):
                locals()[s] = v.replace("`","")

        if isinstance(value_columns, str):
            value_cols = [c.strip() for c in value_columns.replace("`","").split(",") if c.strip()]
        else:
            value_cols = list(value_columns)

        if not os.path.exists(shapefile_path):
            return {"status": "error", "message": f"Shapefile not found: {shapefile_path}"}
        if len(value_cols) < 2:
            return {"status": "error", "message": "value_columns must include at least 2 time steps (wide format)."}

        # --- load + project ---
        gdf = gpd.read_file(shapefile_path)
        missing = [c for c in value_cols if c not in gdf.columns]
        if missing:
            return {"status": "error", "message": f"Columns not found: {missing}"}

        gdf = gdf.to_crs(target_crs)

        # Ensure numeric
        gdf[value_cols] = gdf[value_cols].apply(pd.to_numeric, errors="coerce")

        # --- prepare Y (n x t) ---
        Y = gdf[value_cols].to_numpy(copy=True).astype(float)  # shape (n, t)
        if drop_na:
            mask = ~np.any(np.isnan(Y), axis=1)
            if mask.sum() < Y.shape[0]:
                gdf = gdf.loc[mask].reset_index(drop=True)
                Y = Y[mask, :]

        # optional relative values (period-wise)
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
                thr = distance_threshold / 111000.0  # meters -> degrees
            w = libpysal.weights.DistanceBand.from_dataframe(
                gdf, threshold=thr, binary=False, use_index=True
            )
        else:
            return {"status":"error","message":f"Unknown weights_method: {weights_method}"}

        w.transform = "r"

        # handle islands by dropping rows and rebuilding weights
        if w.islands:
            keep_idx = [i for i in range(gdf.shape[0]) if i not in set(w.islands)]
            if not keep_idx:
                return {"status":"error","message":"All units are islands under current weights; adjust weights_method/threshold."}
            gdf = gdf.iloc[keep_idx].reset_index(drop=True)
            Y = Y[keep_idx, :]
            if wm == "queen":
                w = libpysal.weights.Queen.from_dataframe(gdf, use_index=True)
            elif wm == "rook":
                w = libpysal.weights.Rook.from_dataframe(gdf, use_index=True)
            else:
                thr = distance_threshold if target_crs.upper() != "EPSG:4326" else distance_threshold/111000.0
                w = libpysal.weights.DistanceBand.from_dataframe(gdf, threshold=thr, binary=False, use_index=True)
            w.transform = "r"

        # --- Spatial Markov ---
        try:
            from giddy.markov import Spatial_Markov
        except ModuleNotFoundError:
            return {"status": "error", "message": "The 'giddy' package is not installed. Install with: pip install giddy"}

        sm = Spatial_Markov(
            Y, w,
            k=int(k), m=int(m),
            permutations=int(permutations),
            fixed=bool(fixed),
            discrete=False,
            fill_empty_classes=bool(fill_empty_classes),
            variable_name=";".join(value_cols)
        )

        # --- package results (JSON-safe) ---
        def tolist(x):
            """Recursively convert numpy arrays and nested structures to lists."""
            if x is None:
                return None
            try:
                if isinstance(x, np.ndarray):
                    return x.tolist()
                elif isinstance(x, (list, tuple)):
                    return [tolist(xx) for xx in x]
                elif isinstance(x, dict):
                    return {k: tolist(v) for k, v in x.items()}
                elif isinstance(x, (np.integer, np.floating)):
                    return float(x) if isinstance(x, np.floating) else int(x)
                else:
                    return x
            except Exception:
                # Fallback: try to convert to native Python type
                try:
                    return float(x) if isinstance(x, (np.floating, float)) else int(x) if isinstance(x, (np.integer, int)) else str(x)
                except Exception:
                    return x

        # Safer preview: keep geometry, write WKT to a new column, then drop geometry
        preview = gdf[[*value_cols, "geometry"]].head(5).copy()
        preview["geometry_wkt"] = preview["geometry"].apply(
            lambda g: g.wkt if g is not None and not g.is_empty else None
        )
        preview = pd.DataFrame(preview.drop(columns="geometry")).to_dict(orient="records")

        result = {
            "n_regions": int(Y.shape[0]),
            "n_periods": int(Y.shape[1]),
            "k_classes_y": int(k),
            "m_classes_lag": int(m),
            "weights_method": weights_method.lower(),
            "value_columns": value_cols,
            "discretization": {
                "cutoffs_y": tolist(getattr(sm, "cutoffs", None)),
                "cutoffs_lag": tolist(getattr(sm, "lag_cutoffs", None)),
                "fixed": bool(fixed)
            },
            "global_transition_prob_p": tolist(sm.p),      # (k x k)
            "conditional_transition_prob_P": tolist(sm.P), # (m x k x k)
            "global_steady_state_s": tolist(sm.s),         # (k,)
            "conditional_steady_states_S": tolist(sm.S),   # (m x k)
            "tests": {
                "chi2_total_x2": float(getattr(sm, "x2", np.nan)),
                "chi2_df": int(getattr(sm, "x2_dof", -1)),
                "chi2_pvalue": float(getattr(sm, "x2_pvalue", np.nan)),
                "Q": float(getattr(sm, "Q", np.nan)),
                "Q_p_value": float(getattr(sm, "Q_p_value", np.nan)),
                "LR": float(getattr(sm, "LR", np.nan)),
                "LR_p_value": float(getattr(sm, "LR_p_value", np.nan)),
            },
            "data_preview": preview,
        }

        msg = "Spatial Markov completed successfully"
        if wm == "distance" and target_crs.upper() == "EPSG:4326":
            msg += f" (threshold interpreted as {distance_threshold/111000.0:.6f} degrees)."

        # Apply tolist conversion recursively to the entire result
        result = tolist(result)

        return {"status": "success", "message": msg, "result": result}

    except Exception as e:
        return {"status": "error", "message": f"Failed to run Spatial Markov: {str(e)}"}
