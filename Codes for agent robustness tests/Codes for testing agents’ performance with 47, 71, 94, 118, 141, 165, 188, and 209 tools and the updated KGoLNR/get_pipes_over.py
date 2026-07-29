# -*- coding: utf-8 -*-
"""Filter EPANET pipes by velocity threshold."""
import numpy as np
from _helpers_epanet import _load_and_simulate

def get_pipes_over(file_name: str, threshold: float) -> str:
    """List all pipes with velocity above a given threshold.
    Input: file_name (str) -- .inp file. threshold (float) -- velocity limit in m/s.
    Output: dict of pipe_name: velocity for pipes above threshold."""
    network, results = _load_and_simulate(file_name)
    v = results.Velocity[0]
    hits = np.where(v > threshold)[0]
    report = {network.getLinkNameID(i + 1): round(v[i], 2) for i in hits}
    return f"Pipes over {threshold} in {file_name}: {report}" if report else "None found."
