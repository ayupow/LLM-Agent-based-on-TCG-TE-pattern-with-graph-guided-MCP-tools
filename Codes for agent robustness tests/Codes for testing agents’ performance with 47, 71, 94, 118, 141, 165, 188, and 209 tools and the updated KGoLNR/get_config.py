# -*- coding: utf-8 -*-
"""Get active simulation_config.json contents."""
import json
from _helpers_pf import _default_cfg_path

def get_config(cfg_path: str = "") -> str:
    """Return the active simulation_config.json as a JSON string.
    Input: cfg_path (str, optional) -- path to config file. Uses default if empty.
    Output: JSON string of the config."""
    path = cfg_path or _default_cfg_path()
    with open(path, "r", encoding="utf-8") as fh:
        return json.dumps(json.load(fh), indent=2, ensure_ascii=False)
