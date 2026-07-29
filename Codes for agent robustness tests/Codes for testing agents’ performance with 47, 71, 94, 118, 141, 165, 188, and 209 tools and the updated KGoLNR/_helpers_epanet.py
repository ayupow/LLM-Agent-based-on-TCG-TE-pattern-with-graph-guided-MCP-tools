# -*- coding: utf-8 -*-
# Shared helpers for EPANET MCP tools
import os, io, base64, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from epyt import epanet
from pydantic import BaseModel, Field
from typing import Optional, Literal
from mcp.types import ImageContent

NETWORKS_DIR = "Networks"
MODIFIED_DIR = "Modified"
os.makedirs(NETWORKS_DIR, exist_ok=True)
os.makedirs(MODIFIED_DIR, exist_ok=True)

class Intervention(BaseModel):
    action: Literal["status", "add_pipe", "set_diameter", "delete_pipe"] = Field(
        ..., description="The type of modification.")
    id: str = Field(..., description="Unique ID of the pipe or link.")
    value: Optional[str] = Field(None, description="For 'status': 'open' or 'close'.")
    diameter: Optional[float] = Field(None, description="For 'set_diameter'/'add_pipe': diameter in inches.")
    from_node: Optional[str] = Field(None, description="For 'add_pipe': start node ID.")
    to_node: Optional[str] = Field(None, description="For 'add_pipe': end node ID.")

def _get_full_path(filename: str) -> str:
    clean_name = os.path.basename(filename)
    if not clean_name.lower().endswith(".inp"):
        clean_name += ".inp"
    mod_path = os.path.join(MODIFIED_DIR, clean_name)
    if os.path.exists(mod_path): return mod_path
    net_path = os.path.join(NETWORKS_DIR, clean_name)
    if os.path.exists(net_path): return net_path
    raise FileNotFoundError(f"'{clean_name}' not found in {MODIFIED_DIR} or {NETWORKS_DIR}.")

def _load_and_simulate(filename: str):
    full_path = _get_full_path(filename)
    network = epanet(full_path, display_msg=False, display_warnings=False)
    network.setDemandModel("DDA", 0, 0, 0)
    results = network.getComputedHydraulicTimeSeries()
    return network, results

def _create_plot_image(x_data, y_data, title, xlabel, ylabel, colors) -> ImageContent:
    plt.switch_backend("Agg")
    plt.figure(figsize=(12, 6))
    plt.bar(x_data, y_data, color=colors)
    plt.xlabel(xlabel); plt.ylabel(ylabel); plt.title(title)
    plt.xticks(rotation=90); plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png"); plt.close()
    buf.seek(0)
    return ImageContent(type="image", data=base64.b64encode(buf.read()).decode("utf-8"), mimeType="image/png")
