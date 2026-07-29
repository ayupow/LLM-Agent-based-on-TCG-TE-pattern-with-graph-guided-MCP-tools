# -*- coding: utf-8 -*-
"""Create and activate a study case in PowerFactory."""
import json
from _helpers_pf import _pf, _load_modules, _default_cfg_path

def create_study_case(case_name: str, base_study_case: str = "0. Base",
                      open_digsilent: bool = True, request_id: str = "",
                      cfg_path: str = "") -> str:
    """Create/activate a study case without running simulation.
    Input: case_name (str) -- target study case name. base_study_case (str='0. Base') -- source.
           open_digsilent (bool=True) -- show GUI. request_id (str, optional) -- idempotency key.
           cfg_path (str, optional) -- path to simulation_config.json.
    Output: JSON with success flag and message."""
    SimulationConfig, DIgSILENTAgent = _load_modules()
    path = cfg_path or _default_cfg_path()
    cfg = SimulationConfig.from_json(path)
    ok, msg = _pf(DIgSILENTAgent.create_study_case, cfg.project_path, case_name,
                  base_study_case, open_digsilent, request_id)
    return json.dumps({"success": ok, "message": msg})
