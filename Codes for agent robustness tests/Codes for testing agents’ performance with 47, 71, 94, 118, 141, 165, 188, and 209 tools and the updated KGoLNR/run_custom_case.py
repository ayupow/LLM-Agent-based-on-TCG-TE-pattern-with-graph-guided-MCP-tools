# -*- coding: utf-8 -*-
"""Run a single custom fault case with parameters at call-time."""
from datetime import datetime
from _helpers_pf import _pf, _load_modules, _to_json, _default_cfg_path

def run_custom_case(fault_type: str, fault_element: str, t_fault: float, t_clear: float,
                    t_end: float = 10.0, dt_rms: float = 0.01, case_name: str = "Custom_Case",
                    switch_element: str = "", t_switch: float = 0.0, switch_state: int = 0,
                    create_new_study_case: bool = False, export_pfd: bool = False,
                    open_digsilent: bool = True, cfg_path: str = "") -> str:
    """Run a custom fault scenario with parameters supplied at call-time.
    Network settings read from simulation_config.json; only fault params overridden.
    Input: fault_type (str) -- 'bus', 'line', or 'gen_switch'.
           fault_element (str) -- name of faulted element in PowerFactory.
           t_fault (float) -- fault inception time (s). t_clear (float) -- clearing time (s).
           t_end (float=10.0) -- simulation end time (s). dt_rms (float=0.01) -- step size (s).
           case_name (str) -- output label. switch_element (str) -- for gen_switch faults.
           t_switch (float) -- switch operation time. switch_state (int) -- 0=trip, 1=close.
           create_new_study_case (bool=False) -- timestamped case per call.
           export_pfd (bool=False) -- export .pfd. open_digsilent (bool=True) -- show GUI.
    Output: JSON pipeline result (same schema as run_simulation)."""
    SimulationConfig, DIgSILENTAgent = _load_modules()
    path = cfg_path or _default_cfg_path()
    cfg = SimulationConfig.from_json(path)
    if create_new_study_case:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        cfg.study_case = f"{case_name}_{ts}"
    else:
        cfg.study_case = case_name
    cfg.fault_type = fault_type; cfg.fault_element = fault_element
    cfg.t_fault = t_fault; cfg.t_clear = t_clear; cfg.t_end = t_end; cfg.dt_rms = dt_rms
    cfg.run_label = case_name
    cfg.switch_element = switch_element; cfg.t_switch = t_switch or t_fault
    cfg.switch_state = switch_state
    cfg.export_pfd = 1 if export_pfd else 0
    cfg.open_digsilent = 1 if open_digsilent else 0
    def _impl():
        agent = DIgSILENTAgent(cfg)
        return agent.run_pipeline()
    return _to_json(_pf(_impl))
