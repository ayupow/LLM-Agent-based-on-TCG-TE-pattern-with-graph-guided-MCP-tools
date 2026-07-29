# -*- coding: utf-8 -*-
"""Run a full EPANET hydraulic simulation on any network."""
import time, numpy as np
from _helpers_epanet import _get_full_path, _load_and_simulate

def run_epanet_simulation(file_name: str) -> str:
    """Runs a full hydraulic simulation on any network (Original or Modified).
    Input: file_name (str) -- .inp file name (searches Networks/ and Modified/ dirs).
    Output: simulation summary with node count, pipe count, min pressure, max velocity."""
    start = time.time()
    network, results = _load_and_simulate(file_name)
    junc_idx = np.array(network.getNodeJunctionIndex()) - 1
    pressures = results.Pressure[0, junc_idx]
    return (f"Results for: {file_name}\n"
            f"Source Path: {_get_full_path(file_name)}\n"
            f"Nodes: {network.getNodeJunctionCount()} | Pipes: {len(network.getLinkIndex())}\n"
            f"Min Pressure: {np.min(pressures):.2f} Meters | Max Velocity: {np.max(results.Velocity[0]):.2f} m/s")
