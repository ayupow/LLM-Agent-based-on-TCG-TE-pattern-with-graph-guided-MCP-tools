# -*- coding: utf-8 -*-
"""Run a load flow calculation (ComLdf) on active study case."""
import json
from _helpers_pf import _pf, _load_modules, _default_cfg_path

def run_loadflow(open_digsilent: bool = True, save_csv: bool = False,
                 cfg_path: str = "") -> str:
    """Run load flow on the currently active study case.
    Input: open_digsilent (bool=True) -- show GUI. save_csv (bool=False) -- export CSV snapshot.
           cfg_path (str, optional) -- config path for output_dir/run_label.
    Output: JSON with success flag and message."""
    SimulationConfig, DIgSILENTAgent = _load_modules()
    output_dir, run_label = r"C:\RMS_Results", "run_001"
    if save_csv:
        path = cfg_path or _default_cfg_path()
        try:
            cfg = SimulationConfig.from_json(path)
            output_dir = getattr(cfg, "output_dir", output_dir) or output_dir
            run_label = getattr(cfg, "run_label", run_label) or run_label
        except Exception as e:
            return json.dumps({"success": False, "message": f"Config read failed: {e}"})
    ok, msg = _pf(DIgSILENTAgent.load_flow, open_digsilent, save_csv, output_dir, run_label)
    return json.dumps({"success": ok, "message": msg})
