# -*- coding: utf-8 -*-
"""Apply engineering interventions to an EPANET water network."""
import os
from epyt import epanet
from _helpers_epanet import _get_full_path, MODIFIED_DIR, Intervention

def modify_network(file_name: str, interventions: list) -> str:
    """Apply engineering changes (open/close pipes, add/delete pipes, set diameters).
    Input: file_name (str) -- .inp file. interventions (list[Intervention]) -- list of
           {action, id, value, diameter, from_node, to_node} dicts.
    Output: success message with modification log."""
    full_path = _get_full_path(file_name)
    network = epanet(full_path, display_msg=False, display_warnings=False)
    log = []
    for task in interventions:
        action = task.get("action", "").lower() if isinstance(task, dict) else task.action.lower()
        item_id = task.get("id", "") if isinstance(task, dict) else task.id
        value = task.get("value", "") if isinstance(task, dict) else (task.value or "")
        diameter = task.get("diameter") if isinstance(task, dict) else task.diameter
        from_node = task.get("from_node") if isinstance(task, dict) else task.from_node
        to_node = task.get("to_node") if isinstance(task, dict) else task.to_node

        if action == "status":
            idx = network.getLinkIndex(item_id)
            status_val = 1 if str(value).lower() == "open" else 0
            network.setLinkStatus(idx, status_val)
            log.append(f"Set status of {item_id} to {value}")
        elif action == "add_pipe":
            network.addLinkPipe(item_id, from_node, to_node)
            if diameter:
                idx = network.getLinkIndex(item_id)
                network.setLinkDiameter(idx, diameter)
            log.append(f"Added pipe {item_id} ({from_node} -> {to_node})")
        elif action == "set_diameter":
            idx = network.getLinkIndex(item_id)
            network.setLinkDiameter(idx, diameter)
            log.append(f"Updated {item_id} diameter to {diameter}")
        elif action == "delete_pipe":
            idx = network.getLinkIndex(item_id)
            network.deleteLink(idx)
            log.append(f"Removed pipe {item_id}")

    base = os.path.basename(file_name)
    save_name = base if base.startswith("Modified_") else f"Modified_{base}"
    save_path = os.path.join(MODIFIED_DIR, save_name)
    network.saveInputFile(save_path)
    return f"Successfully modified {save_name}:\n" + "\n".join([f"  {l}" for l in log])
