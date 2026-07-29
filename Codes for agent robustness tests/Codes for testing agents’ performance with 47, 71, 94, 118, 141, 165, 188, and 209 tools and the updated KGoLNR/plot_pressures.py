# -*- coding: utf-8 -*-
"""Plot node pressures from EPANET simulation, optionally filtering critical nodes."""
import numpy as np
from _helpers_epanet import _load_and_simulate, _create_plot_image

def plot_pressures(file_name: str, low_threshold: float = 20.0, only_critical: bool = False) -> list:
    """Plot node pressures with optional critical-node filtering.
    Input: file_name (str) -- .inp file. low_threshold (float=20.0) -- pressure threshold (Meters).
           only_critical (bool=False) -- if True, show only nodes below threshold.
    Output: list with [base64 PNG image, text summary string]."""
    network, results = _load_and_simulate(file_name)
    idx = np.array(network.getNodeJunctionIndex()) - 1
    all_pressures = results.Pressure[0, idx]
    all_names = [network.getNodeNameID(i + 1) for i in idx]
    if only_critical:
        plot_data = [(n, p) for n, p in zip(all_names, all_pressures) if p < low_threshold]
        if not plot_data: return [f"No nodes found below {low_threshold} Meters in {file_name}."]
        names, pressures = zip(*plot_data)
        colors = ["#ff4d4d"] * len(pressures)
        title_suffix = f"(Only Nodes < {low_threshold} Meters)"
    else:
        names, pressures = all_names, all_pressures
        colors = ["#ff4d4d" if p < low_threshold else "#87ceeb" for p in pressures]
        title_suffix = ""
    low_count = sum(1 for p in all_pressures if p < low_threshold)
    plot_img = _create_plot_image(names, pressures, f"Node Pressures: {file_name} {title_suffix}",
                                  "Node ID", "Pressure (Meters)", colors=colors)
    return [plot_img, f"Summary for {file_name}:\n  Total Network Junctions: {len(all_pressures)}\n"
            f"  Critical Nodes (< {low_threshold} Meters): {low_count}\n"
            f"  Showing {len(names)} nodes in the current plot."]
