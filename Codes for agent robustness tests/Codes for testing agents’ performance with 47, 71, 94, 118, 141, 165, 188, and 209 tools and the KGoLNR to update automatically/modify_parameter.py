# -*- coding: utf-8 -*-
"""Modify a PowerFactory object attribute."""
import json
from typing import Any
from _helpers_pf import _pf, _load_modules

def modify_parameter(object_name: str, variable: str, new_value: Any,
                     open_digsilent: bool = True) -> str:
    """Set an attribute on all objects matching object_name query.
    Input: object_name (str) -- query for GetCalcRelevantObjects (e.g. 'G 10.ElmSym').
           variable (str) -- attribute name (e.g. 'e:outserv'). new_value (Any) -- new value.
           open_digsilent (bool=True) -- show GUI.
    Output: JSON with success flag and message."""
    _, DIgSILENTAgent = _load_modules()
    ok, msg = _pf(DIgSILENTAgent.modify_parameter, object_name, variable, new_value, open_digsilent)
    return json.dumps({"success": ok, "message": msg})
