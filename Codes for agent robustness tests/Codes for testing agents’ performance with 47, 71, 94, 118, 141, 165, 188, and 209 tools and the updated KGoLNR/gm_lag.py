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


def gm_lag(
    shapefile_path: str,
    y_col: str,                               # dependent variable
    x_cols: Union[str, List[str]],            # exogenous regressors (no constant)
    target_crs: str = "EPSG:4326",
    weights_method: str = "queen",            # 'queen'|'rook'|'distance'
    distance_threshold: float = 100000,       # meters; auto→degrees for EPSG:4326
    # IV/GMM config
    w_lags: int = 1,                          # instruments: WX, WWX, ...
    lag_q: bool = True,                       # also lag external instruments q
    yend_cols: Union[None, str, List[str]] = None,  # other endogenous regressors (optional)
    q_cols: Union[None, str, List[str]] = None,     # their external instruments (optional)
    # Inference options
    robust: Union[None, str] = None,          # None | 'white' | 'hac'
    hac_bandwidth: float = None,              # only used if robust='hac'
    spat_diag: bool = True,                   # AK test
    sig2n_k: bool = False,                    # variance uses n-k if True
    drop_na: bool = True                      # drop rows with NA in y/x/yend/q
) -> Dict[str, Any]:
    """
    Run spreg.GM_Lag (spatial 2SLS / GMM-IV spatial lag model) on a cross-section.

    Returns coefficients with SE/z/p, fit metrics, (optional) AK test, and a small data preview.
    """
    try:
        # --- sanitize inputs ---
        for s in ("shapefile_path","target_crs","weights_method"):
            v = locals()[s]
            if isinstance(v, str):
                locals()[s] = v.replace("`","")

        if isinstance(x_cols, str):
            x_cols_list = [c.strip() for c in x_cols.split(",") if c.strip()]
        else:
            x_cols_list = list(x_cols)

        if isinstance(yend_cols, str):
            yend_cols_list = [c.strip() for c in yend_cols.split(",") if c.strip()]
        elif yend_cols is None:
            yend_cols_list = None
        else:
            yend_cols_list = list(yend_cols)

        if isinstance(q_cols, str):
            q_cols_list = [c.strip() for c in q_cols.split(",") if c.strip()]
        elif q_cols is None:
            q_cols_list = None
        else:
            q_cols_list = list(q_cols)

        if not os.path.exists(shapefile_path):
            return {"status": "error", "message": f"Shapefile not found: {shapefile_path}"}
        if not x_cols_list:
            return {"status": "error", "message": "x_cols must include at least one regressor."}

        # --- load + project ---
        gdf = gpd.read_file(shapefile_path)
        needed = [y_col] + x_cols_list + (yend_cols_list or []) + (q_cols_list or [])
        missing = [c for c in needed if c not in gdf.columns]
        if missing:
            return {"status": "error", "message": f"Columns not found: {missing}"}

        gdf = gdf.to_crs(target_crs)

        # --- coerce numerics & subset ---
        gdf[needed] = gdf[needed].apply(pd.to_numeric, errors="coerce")
        data = gdf[needed + [gdf.geometry.name]].copy()

        if drop_na:
            before = data.shape[0]
            data = data.dropna(subset=needed)
            after = data.shape[0]
            if after == 0:
                return {"status": "error", "message": "All rows dropped due to NA in y/x/yend/q."}
            if after < before:
                gdf = gdf.loc[data.index].reset_index(drop=True)
                data = data.reset_index(drop=True)

        # --- arrays for spreg ---
        y = data[[y_col]].to_numpy(dtype=float)              # (n,1)
        X = data[x_cols_list].to_numpy(dtype=float)          # (n,k), no constant
        YEND = None if not yend_cols_list else data[yend_cols_list].to_numpy(dtype=float)
        Q = None if not q_cols_list else data[q_cols_list].to_numpy(dtype=float)

        # --- spatial weights ---
        import libpysal
        wm = weights_method.lower()
        if wm == "queen":
            w = libpysal.weights.Queen.from_dataframe(gdf.loc[data.index], use_index=True)
        elif wm == "rook":
            w = libpysal.weights.Rook.from_dataframe(gdf.loc[data.index], use_index=True)
        elif wm == "distance":
            thr = distance_threshold if target_crs.upper() != "EPSG:4326" else distance_threshold / 111000.0
            w = libpysal.weights.DistanceBand.from_dataframe(
                gdf.loc[data.index], threshold=thr, binary=False, use_index=True
            )
        else:
            return {"status":"error","message":f"Unknown weights_method: {weights_method}"}
        w.transform = "r"

        # Drop islands and re-align data if needed
        if w.islands:
            keep = [i for i in range(len(gdf.loc[data.index])) if i not in set(w.islands)]
            if not keep:
                return {"status":"error","message":"All units are islands under current weights."}
            # reindex everything
            y = y[keep, :]
            X = X[keep, :]
            if YEND is not None: YEND = YEND[keep, :]
            if Q is not None: Q = Q[keep, :]
            sub_gdf = gdf.loc[data.index].iloc[keep]
            if wm == "queen":
                w = libpysal.weights.Queen.from_dataframe(sub_gdf, use_index=True)
            elif wm == "rook":
                w = libpysal.weights.Rook.from_dataframe(sub_gdf, use_index=True)
            else:
                thr = distance_threshold if target_crs.upper() != "EPSG:4326" else distance_threshold / 111000.0
                w = libpysal.weights.DistanceBand.from_dataframe(sub_gdf, threshold=thr, binary=False, use_index=True)
            w.transform = "r"

        # --- HAC kernel weights if requested ---
        gwk = None
        if robust == "hac":
            # Build Kernel weights on centroids; ensure ones on diagonal
            coords = np.column_stack([gdf.loc[data.index].geometry.centroid.x,
                                      gdf.loc[data.index].geometry.centroid.y])
            bw = hac_bandwidth or (np.ptp(coords[:,0]) + np.ptp(coords[:,1])) / 20.0
            gwk = libpysal.weights.Kernel(coords, bandwidth=bw, fixed=True, function="triangular", diagonal=True)
            gwk.transform = "r"

        # --- fit GM_Lag ---
        try:
            from spreg import GM_Lag
        except ModuleNotFoundError:
            return {"status": "error", "message": "The 'spreg' package is not installed. Install with: pip install spreg"}

        reg = GM_Lag(
            y, X,
            yend=YEND, q=Q,
            w=w,
            w_lags=int(w_lags),
            lag_q=bool(lag_q),
            robust=robust,               # None | 'white' | 'hac'
            gwk=gwk,                     # required if robust='hac'
            sig2n_k=bool(sig2n_k),
            spat_diag=bool(spat_diag),
            name_y=y_col,
            name_x=x_cols_list,
            name_yend=(yend_cols_list or None),
            name_q=(q_cols_list or None),
            name_w=f"{weights_method}"
        )

        # --- package outputs ---
        def arr(x): return None if x is None else np.asarray(x).tolist()
        def zpack(z_list):
            # z_stat is list of (z, p)
            return [{"z": float(zp[0]), "p": float(zp[1])} for zp in (z_list or [])]

        # tiny preview (avoid geometry dtype issues)
        preview = gdf.loc[data.index, [y_col, *x_cols_list, gdf.geometry.name]].head(5).copy()
        preview["geometry_wkt"] = preview[gdf.geometry.name].apply(lambda g: g.wkt if g is not None else None)
        preview = pd.DataFrame(preview.drop(columns=[gdf.geometry.name])).to_dict(orient="records")

        result = {
            "n_obs": int(reg.n),
            "k_vars": int(reg.k),  # includes constant internally
            "dependent": y_col,
            "exog": x_cols_list,
            "endog": yend_cols_list,
            "instruments": q_cols_list,
            "weights_method": weights_method.lower(),
            "spec": {"w_lags": int(w_lags), "lag_q": bool(lag_q), "robust": robust, "sig2n_k": bool(sig2n_k)},
            "betas": [float(b) for b in np.asarray(reg.betas).flatten()],
            "beta_names": (["const"] + x_cols_list + (yend_cols_list or []) + ["W_y"])[:len(np.asarray(reg.betas).flatten())],
            "std_err": arr(reg.std_err),
            "z_stats": zpack(getattr(reg, "z_stat", None)),
            "pseudo_r2": float(getattr(reg, "pr2", np.nan)),
            "pseudo_r2_reduced": float(getattr(reg, "pr2_e", np.nan)),
            "sig2": float(getattr(reg, "sig2", np.nan)),
            "ssr": float(getattr(reg, "utu", np.nan)),
            "ak_test": arr(getattr(reg, "ak_test", None)),  # [stat, p] if spat_diag=True
            "pred_y_head": [float(v) for v in np.asarray(reg.predy).flatten()[:5]],
            "data_preview": preview
        }

        msg = "GM_Lag estimation completed successfully"
        if wm == "distance" and target_crs.upper() == "EPSG:4326":
            msg += f" (threshold interpreted as {distance_threshold/111000.0:.6f} degrees)."
        if robust == "hac":
            msg += f" (HAC bandwidth ~ {bw:.3f})."

        return {"status": "success", "message": msg, "result": result}

    except Exception as e:
        return {"status": "error", "message": f"Failed to run GM_Lag: {str(e)}"}
