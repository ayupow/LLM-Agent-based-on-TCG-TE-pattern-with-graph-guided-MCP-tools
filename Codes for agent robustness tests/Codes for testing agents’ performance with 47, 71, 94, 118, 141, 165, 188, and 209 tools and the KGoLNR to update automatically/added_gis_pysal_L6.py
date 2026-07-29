# added_gis_pysal_L6 — MCP Server (subset for level L6)
from mcp.server.fastmcp import FastMCP

from gearys_c import gearys_c
from join_counts import join_counts
from moran_local import moran_local
from spatial_markov import spatial_markov
from getis_ord_g import getis_ord_g
from gamma_statistic import gamma_statistic
from build_transform_and_save_weights import build_transform_and_save_weights
from weights_from_shapefile import weights_from_shapefile
from gm_lag import gm_lag
from adbscan import adbscan
from ols_with_spatial_diagnostics_safe import ols_with_spatial_diagnostics_safe
from join_counts_local import join_counts_local
from dynamic_lisa import dynamic_lisa
from distance_band_weights import distance_band_weights
from knn_weights import knn_weights
from build_and_transform_weights import build_and_transform_weights
from getis_ord_g_local import getis_ord_g_local
from morans_i import morans_i

mcp = FastMCP(name="added_gis_pysal_L6")

mcp.add_tool(gearys_c,
    name="gearys_c",
    description="Tool: gearys_c (from gis pysal server)."
)

mcp.add_tool(join_counts,
    name="join_counts",
    description="Tool: join_counts (from gis pysal server)."
)

mcp.add_tool(moran_local,
    name="moran_local",
    description="Tool: moran_local (from gis pysal server)."
)

mcp.add_tool(spatial_markov,
    name="spatial_markov",
    description="Tool: spatial_markov (from gis pysal server)."
)

mcp.add_tool(getis_ord_g,
    name="getis_ord_g",
    description="Tool: getis_ord_g (from gis pysal server)."
)

mcp.add_tool(gamma_statistic,
    name="gamma_statistic",
    description="Tool: gamma_statistic (from gis pysal server)."
)

mcp.add_tool(build_transform_and_save_weights,
    name="build_transform_and_save_weights",
    description="Tool: build_transform_and_save_weights (from gis pysal server)."
)

mcp.add_tool(weights_from_shapefile,
    name="weights_from_shapefile",
    description="Tool: weights_from_shapefile (from gis pysal server)."
)

mcp.add_tool(gm_lag,
    name="gm_lag",
    description="Tool: gm_lag (from gis pysal server)."
)

mcp.add_tool(adbscan,
    name="adbscan",
    description="Tool: adbscan (from gis pysal server)."
)

mcp.add_tool(ols_with_spatial_diagnostics_safe,
    name="ols_with_spatial_diagnostics_safe",
    description="Tool: ols_with_spatial_diagnostics_safe (from gis pysal server)."
)

mcp.add_tool(join_counts_local,
    name="join_counts_local",
    description="Tool: join_counts_local (from gis pysal server)."
)

mcp.add_tool(dynamic_lisa,
    name="dynamic_lisa",
    description="Tool: dynamic_lisa (from gis pysal server)."
)

mcp.add_tool(distance_band_weights,
    name="distance_band_weights",
    description="Tool: distance_band_weights (from gis pysal server)."
)

mcp.add_tool(knn_weights,
    name="knn_weights",
    description="Tool: knn_weights (from gis pysal server)."
)

mcp.add_tool(build_and_transform_weights,
    name="build_and_transform_weights",
    description="Tool: build_and_transform_weights (from gis pysal server)."
)

mcp.add_tool(getis_ord_g_local,
    name="getis_ord_g_local",
    description="Tool: getis_ord_g_local (from gis pysal server)."
)

mcp.add_tool(morans_i,
    name="morans_i",
    description="Tool: morans_i (from gis pysal server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
