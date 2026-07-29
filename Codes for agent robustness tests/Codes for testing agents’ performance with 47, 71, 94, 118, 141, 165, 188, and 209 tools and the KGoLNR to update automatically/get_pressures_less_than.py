# -*- coding: utf-8 -*-
"""Filter EPANET nodes by pressure threshold."""
import numpy as np
from _helpers_epanet import _load_and_simulate

def get_pressures_less_than(file_name: str, threshold: float) -> str:
    """List all nodes with pressure below a given threshold.
    Input: file_name (str) -- .inp file. threshold (float) -- pressure limit in Meters.
    Output: dict of node_name: pressure for nodes below threshold."""
    network, results = _load_and_simulate(file_name)
    idx = np.array(network.getNodeJunctionIndex()) - 1
    p = results.Pressure[0, idx]
    hits = np.where(p < threshold)[0]
    report = {network.getNodeNameID(idx[i] + 1): round(p[i], 2) for i in hits}
    return f"Nodes under {threshold} in {file_name}: {report}" if report else "None found."
