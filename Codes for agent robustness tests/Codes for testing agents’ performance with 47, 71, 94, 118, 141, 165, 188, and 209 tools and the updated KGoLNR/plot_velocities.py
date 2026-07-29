# -*- coding: utf-8 -*-
"""Plot pipe velocities from EPANET simulation, highlighting stagnant pipes."""
from _helpers_epanet import _load_and_simulate, _create_plot_image

def plot_velocities(file_name: str, low_threshold: float = 0.5, only_critical: bool = False) -> list:
    """Plot pipe velocities, highlighting low-velocity pipes (potential stagnation).
    Input: file_name (str) -- .inp file. low_threshold (float=0.5) -- velocity below which pipes
           are flagged (m/s). only_critical (bool=False) -- if True, show only low-velocity pipes.
    Output: list with [base64 PNG image, text summary string]."""
    network, results = _load_and_simulate(file_name)
    all_vels = results.Velocity[0]
    all_names = [network.getLinkNameID(i + 1) for i in range(len(all_vels))]
    if only_critical:
        plot_data = [(n, v) for n, v in zip(all_names, all_vels) if v < low_threshold]
        if not plot_data: return [f"No pipes found with velocity below {low_threshold} m/s in {file_name}."]
        names, vels = zip(*plot_data)
        colors = ["#ff4d4d"] * len(vels)
        title_suffix = f"(Only Pipes < {low_threshold} m/s)"
    else:
        names, vels = all_names, all_vels
        colors = ["#ff4d4d" if v < low_threshold else "#2ecc71" for v in vels]
        title_suffix = ""
    low_count = sum(1 for v in all_vels if v < low_threshold)
    healthy_count = len(all_vels) - low_count
    plot_img = _create_plot_image(names, vels, f"Pipe Velocities: {file_name} {title_suffix}",
                                  "Pipe ID", "Velocity (m/s)", colors=colors)
    return [plot_img, f"Velocity Analysis for {file_name}:\n"
            f"  Total Network Pipes: {len(all_vels)}\n"
            f"  Stagnant/Low Flow (< {low_threshold} m/s): {low_count}\n"
            f"  Healthy Flow (>= {low_threshold} m/s): {healthy_count}"]
