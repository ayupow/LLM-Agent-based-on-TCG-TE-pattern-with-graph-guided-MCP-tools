# -*- coding: utf-8 -*-
"""Run the full DIgSILENT RMS simulation pipeline."""
from _helpers_pf import _pf, _load_modules, _to_json, _default_cfg_path

def run_simulation(cfg_path: str = "", export_pfd: bool = False,
                   open_digsilent: bool = True) -> str:
    """Run the full RMS simulation pipeline: connect → activate study case → load flow
    → RMS simulation → CSV export → plots → optional PFD export.
    All parameters read from simulation_config.json.
    Input: cfg_path (str, optional) -- path to config. export_pfd (bool=False) -- export .pfd.
           open_digsilent (bool=True) -- show GUI.
    Output: JSON with success flag, csv_path, optional pfd_path, per-step status."""
    SimulationConfig, DIgSILENTAgent = _load_modules()
    path = cfg_path or _default_cfg_path()
    cfg = SimulationConfig.from_json(path)
    cfg.export_pfd = 1 if export_pfd else 0
    cfg.open_digsilent = 1 if open_digsilent else 0
    def _impl():
        agent = DIgSILENTAgent(cfg)
        return agent.run_pipeline()
    return _to_json(_pf(_impl))
