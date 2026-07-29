# added_gis_pysal_L4 — MCP Server (subset for level L4)
from mcp.server.fastmcp import FastMCP

from build_and_transform_weights import build_and_transform_weights
from distance_band_weights import distance_band_weights
from dynamic_lisa import dynamic_lisa
from getis_ord_g import getis_ord_g
from getis_ord_g_local import getis_ord_g_local
from gm_lag import gm_lag
from knn_weights import knn_weights
from moran_local import moran_local
from ols_with_spatial_diagnostics_safe import ols_with_spatial_diagnostics_safe
from spatial_markov import spatial_markov

mcp = FastMCP(name="added_gis_pysal_L4")

mcp.add_tool(build_and_transform_weights,
    name="build_and_transform_weights",
    description="Tool: build_and_transform_weights (from gis pysal server)."
)

mcp.add_tool(distance_band_weights,
    name="distance_band_weights",
    description="Tool: distance_band_weights (from gis pysal server)."
)

mcp.add_tool(dynamic_lisa,
    name="dynamic_lisa",
    description="Tool: dynamic_lisa (from gis pysal server)."
)

mcp.add_tool(getis_ord_g,
    name="getis_ord_g",
    description="Tool: getis_ord_g (from gis pysal server)."
)

mcp.add_tool(getis_ord_g_local,
    name="getis_ord_g_local",
    description="Tool: getis_ord_g_local (from gis pysal server)."
)

mcp.add_tool(gm_lag,
    name="gm_lag",
    description="Tool: gm_lag (from gis pysal server)."
)

mcp.add_tool(knn_weights,
    name="knn_weights",
    description="Tool: knn_weights (from gis pysal server)."
)

mcp.add_tool(moran_local,
    name="moran_local",
    description="Tool: moran_local (from gis pysal server)."
)

mcp.add_tool(ols_with_spatial_diagnostics_safe,
    name="ols_with_spatial_diagnostics_safe",
    description="Tool: ols_with_spatial_diagnostics_safe (from gis pysal server)."
)

mcp.add_tool(spatial_markov,
    name="spatial_markov",
    description="Tool: spatial_markov (from gis pysal server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
