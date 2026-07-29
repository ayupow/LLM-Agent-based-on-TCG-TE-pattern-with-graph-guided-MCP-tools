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

def ols_with_spatial_diagnostics_safe(
    data_path: str,
    y_field: str,
    x_fields: List[str],
    weights_path: Optional[str] = None,
    weights_method: str = "queen",
    id_field: Optional[str] = None,
    threshold: Optional[float] = None,
    k: Optional[int] = None,
    binary: bool = True
) -> Dict[str, Any]:
    """
    Safe MCP pipeline: Read shapefile, build/load W, convert numeric, check NaNs, run OLS.

    Parameters:
    - data_path: path to shapefile or GeoPackage
    - y_field: dependent variable column name
    - x_fields: list of independent variable column names
    - weights_path: optional path to existing weights file (.gal or .gwt)
    - weights_method: 'queen', 'rook', 'distance_band', or 'knn' (used if weights_path not provided)
    - id_field: optional attribute name to use as observation IDs
    - threshold: required if method='distance_band'
    - k: required if method='knn'
    - binary: True for binary weights (DistanceBand only)
    """
    try:
        # --- Step 1: Read data ---
        if not os.path.exists(data_path):
            return {"status": "error", "message": f"Data file not found: {data_path}"}

        gdf = gpd.read_file(data_path)
        if gdf.empty:
            return {"status": "error", "message": "Input file contains no features"}

        # --- Step 2: Extract and convert y and X ---
        if y_field not in gdf.columns:
            return {"status": "error", "message": f"Dependent variable '{y_field}' not found in dataset"}
        if any(xf not in gdf.columns for xf in x_fields):
            return {"status": "error", "message": f"Independent variable(s) {x_fields} not found in dataset"}

        y = gdf[[y_field]].astype(float).values
        X = gdf[x_fields].astype(float).values

        # --- Step 3: Check for NaNs or infinite values ---
        if not np.all(np.isfinite(y)):
            return {"status": "error", "message": "Dependent variable contains NaN or infinite values"}
        if not np.all(np.isfinite(X)):
            return {"status": "error", "message": "Independent variables contain NaN or infinite values"}

        # --- Step 4: Load or build weights ---
        import libpysal
        if weights_path:
            if not os.path.exists(weights_path):
                return {"status": "error", "message": f"Weights file not found: {weights_path}"}
            w = libpysal.open(weights_path).read()
        else:
            coords = [(geom.x, geom.y) for geom in gdf.geometry]
            wm = weights_method.lower()
            if wm == "queen":
                w = libpysal.weights.Queen.from_dataframe(gdf, idVariable=id_field)
            elif wm == "rook":
                w = libpysal.weights.Rook.from_dataframe(gdf, idVariable=id_field)
            elif wm == "distance_band":
                if threshold is None:
                    return {"status": "error", "message": "Threshold is required for distance_band"}
                ids = gdf[id_field].tolist() if id_field and id_field in gdf.columns else None
                w = libpysal.weights.DistanceBand(coords, threshold=threshold, binary=binary, ids=ids)
            elif wm == "knn":
                if k is None:
                    return {"status": "error", "message": "k is required for knn"}
                ids = gdf[id_field].tolist() if id_field and id_field in gdf.columns else None
                w = libpysal.weights.KNN(coords, k=k, ids=ids)
            else:
                return {"status": "error", "message": f"Unsupported weights method: {weights_method}"}

        w.transform = "r"  # Row-standardize for regression

        # --- Step 5: Fit OLS with spatial diagnostics ---
        try:
            from spreg import OLS
        except ModuleNotFoundError:
            return {"status": "error", "message": "The 'spreg' package is not installed. Install with: pip install spreg"}
        
        # Ensure y is shape (n, 1) and X is (n, k) for spreg
        y = y.reshape(-1, 1) if len(y.shape) == 1 else y
        if X.shape[1] != len(x_fields):
            X = X.T if X.shape[0] == len(x_fields) else X
        
        # Run OLS with spatial diagnostics
        ols_model = OLS(y, X, w=w, spat_diag=True, name_y=y_field, name_x=x_fields, name_ds="dataset")

        # --- Step 6: Collect results ---
        # Extract Moran's I for residuals if available (from diagnostics)
        moran_residual = None
        moran_pvalue = None
        if hasattr(ols_model, "diagnostics") and ols_model.diagnostics is not None:
            diag = ols_model.diagnostics
            # Check for Moran's I in diagnostics
            if isinstance(diag, dict):
                if "moran_res" in diag and diag["moran_res"] is not None:
                    mor_res = diag["moran_res"]
                    if len(mor_res) >= 2:
                        moran_residual = float(mor_res[0])
                        moran_pvalue = float(mor_res[1])
        
        # Extract beta names
        beta_names = []
        if hasattr(ols_model, "name_x") and ols_model.name_x:
            beta_names = list(ols_model.name_x)
        else:
            beta_names = [f"x_{i}" for i in range(len(x_fields))]
        
        # Add constant to names if present
        has_constant = hasattr(ols_model, "constant") and ols_model.constant
        if has_constant:
            beta_names = ["constant"] + beta_names
        
        # Extract betas
        betas_dict = {}
        if hasattr(ols_model, "betas") and ols_model.betas is not None:
            betas_flat = ols_model.betas.flatten()
            # Match betas to names
            for i, beta_val in enumerate(betas_flat):
                if i < len(beta_names):
                    betas_dict[beta_names[i]] = float(beta_val)
                else:
                    betas_dict[f"beta_{i}"] = float(beta_val)
        
        # Extract standard errors
        std_err_list = []
        if hasattr(ols_model, "std_err") and ols_model.std_err is not None:
            std_err_list = ols_model.std_err.tolist() if hasattr(ols_model.std_err, "tolist") else list(ols_model.std_err)
        
        results = {
            "n_obs": int(ols_model.n) if hasattr(ols_model, "n") else int(len(y)),
            "r2": float(ols_model.r2) if hasattr(ols_model, "r2") else None,
            "std_error": std_err_list,
            "betas": betas_dict,
            "moran_residual": moran_residual,
            "moran_pvalue": moran_pvalue,
        }

        return {
            "status": "success",
            "message": "OLS regression with spatial diagnostics completed successfully",
            "result": results,
            "regression_results": results  # Also include as regression_results for test compatibility
        }

    except Exception as e:
        logger.error(f"Error in ols_with_spatial_diagnostics_safe: {str(e)}")
        return {"status": "error", "message": f"Failed to run OLS regression: {str(e)}"}
