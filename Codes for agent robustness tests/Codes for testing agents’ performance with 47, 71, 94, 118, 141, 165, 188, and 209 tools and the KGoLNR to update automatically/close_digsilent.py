# -*- coding: utf-8 -*-
"""Close DIgSILENT PowerFactory API session."""
import json
from _helpers_pf import _pf, _load_modules

def close_digsilent() -> str:
    """Close the DIgSILENT PowerFactory API session. Executes app.Exit() and clears shared handles."""
    _, DIgSILENTAgent = _load_modules()
    def _impl():
        DIgSILENTAgent.close()
        return {"success": True, "message": "DIgSILENT API closed"}
    return json.dumps(_pf(_impl))
