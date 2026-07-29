# -*- coding: utf-8 -*-
"""Run a short-circuit calculation (ComShc) on active study case."""
import json
from _helpers_pf import _pf, _load_modules

def run_short_circuit(open_digsilent: bool = True) -> str:
    """Run short-circuit calculation on the currently active study case.
    Input: open_digsilent (bool=True) -- show GUI.
    Output: JSON with success flag and message."""
    _, DIgSILENTAgent = _load_modules()
    ok, msg = _pf(DIgSILENTAgent.short_circuit, open_digsilent)
    return json.dumps({"success": ok, "message": msg})
