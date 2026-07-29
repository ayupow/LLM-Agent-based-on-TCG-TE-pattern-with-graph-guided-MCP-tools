# Shared helpers for PowerFactory MCP tools
import sys, os, json, concurrent.futures
from datetime import datetime
from typing import Any

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

_HERE = os.path.dirname(os.path.abspath(__file__))
_PF_DIR = os.path.join(os.path.dirname(_HERE), 'PowerMCP-main', 'PowerFactory')
if _PF_DIR not in sys.path:
    sys.path.insert(0, _PF_DIR)

_pf_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="pf_thread")

def _pf(fn, *args, **kwargs):
    return _pf_executor.submit(fn, *args, **kwargs).result()

def _load_modules():
    from Agent_DIgSILENT import SimulationConfig, DIgSILENTAgent
    return SimulationConfig, DIgSILENTAgent

def _to_json(obj: Any) -> str:
    import math
    try:
        import numpy as np
        _np = np
    except ImportError:
        _np = None
    def _clean(o):
        if _np is not None:
            if isinstance(o, _np.ndarray):
                return [_clean(v) for v in o.tolist()]
            if isinstance(o, _np.integer): return int(o)
            if isinstance(o, _np.floating):
                v = float(o)
                return None if (math.isnan(v) or math.isinf(v)) else v
            if isinstance(o, _np.bool_): return bool(o)
        if isinstance(o, dict):
            return {(str(k) if not isinstance(k, str) else k): _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
        if isinstance(o, float): return None if (math.isnan(o) or math.isinf(o)) else o
        return o
    return json.dumps(_clean(obj), indent=2, ensure_ascii=False)

def _default_cfg_path():
    import os, shutil
    try:
        from powermcp.config import get_path
        p = get_path("powerfactory", "config_path", must_exist=False)
        if p: return p
    except Exception: pass
    base = os.path.join(os.path.expanduser("~"), ".powermcp", "powerfactory")
    os.makedirs(base, exist_ok=True)
    dest = os.path.join(base, "simulation_config.json")
    example = os.path.join(_PF_DIR, "simulation_config.example.json")
    if not os.path.exists(dest) and os.path.exists(example):
        shutil.copyfile(example, dest)
    return dest
