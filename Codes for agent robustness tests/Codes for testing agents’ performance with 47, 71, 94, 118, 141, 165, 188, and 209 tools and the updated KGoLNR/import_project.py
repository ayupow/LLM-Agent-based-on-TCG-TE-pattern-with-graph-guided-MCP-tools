# -*- coding: utf-8 -*-
"""Import a DIgSILENT PowerFactory project from .pfd file."""
import json
from _helpers_pf import _pf, _load_modules

def import_project(file_path: str = "", open_digsilent: bool = True) -> str:
    """Import a .pfd project file and activate it. PowerFactory must be running first.
    Input: file_path (str) -- absolute path to .pfd file. open_digsilent (bool=True) -- show GUI.
    Output: JSON with success flag and message."""
    if not file_path:
        return json.dumps({"success": False, "message": "file_path is required"})
    _, DIgSILENTAgent = _load_modules()
    ok, msg = _pf(DIgSILENTAgent.import_project, file_path, open_digsilent)
    return json.dumps({"success": ok, "message": msg})
