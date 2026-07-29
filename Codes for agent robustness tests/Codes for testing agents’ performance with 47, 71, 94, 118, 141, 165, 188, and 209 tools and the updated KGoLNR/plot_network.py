# -*- coding: utf-8 -*-
"""Generate a visual layout of an EPANET water network."""
import matplotlib, io, base64
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from epyt import epanet
from mcp.types import ImageContent
from _helpers_epanet import _get_full_path

def plot_network(file_name: str) -> ImageContent:
    """Generate a PNG visualization of the network layout (nodes + pipes).
    Input: file_name (str) -- .inp file name.
    Output: base64-encoded PNG image of the network."""
    full_path = _get_full_path(file_name)
    network = epanet(full_path, display_msg=False, display_warnings=False)
    network.plot()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return ImageContent(type="image", data=base64.b64encode(buf.read()).decode("utf-8"), mimeType="image/png")
