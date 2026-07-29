# added_gis_pysal — MCP Server
# Auto-generated from tools_gis_pysal/ individual tool files

from mcp.server.fastmcp import FastMCP

from adbscan import adbscan
from build_and_transform_weights import build_and_transform_weights
from build_transform_and_save_weights import build_transform_and_save_weights
from distance_band_weights import distance_band_weights
from dynamic_lisa import dynamic_lisa
from gamma_statistic import gamma_statistic
from gearys_c import gearys_c
from getis_ord_g import getis_ord_g
from getis_ord_g_local import getis_ord_g_local
from gm_lag import gm_lag
from join_counts import join_counts
from join_counts_local import join_counts_local
from knn_weights import knn_weights
from moran_local import moran_local
from morans_i import morans_i
from ols_with_spatial_diagnostics_safe import ols_with_spatial_diagnostics_safe
from spatial_markov import spatial_markov
from weights_from_shapefile import weights_from_shapefile

mcp = FastMCP(name="added_gis_pysal")

mcp.add_tool(adbscan,
    name="adbscan",
    description="Adaptive DBSCAN clustering for spatial point data."
)

mcp.add_tool(build_and_transform_weights,
    name="build_and_transform_weights",
    description="Build and transform spatial weights in one step."
)

mcp.add_tool(build_transform_and_save_weights,
    name="build_transform_and_save_weights",
    description="Build spatial weights, transform, and save to file."
)

mcp.add_tool(distance_band_weights,
    name="distance_band_weights",
    description="Create distance-based spatial weights from point data."
)

mcp.add_tool(dynamic_lisa,
    name="dynamic_lisa",
    description="Dynamic directional LISA for spatiotemporal autocorrelation."
)

mcp.add_tool(gamma_statistic,
    name="gamma_statistic",
    description="Compute Gamma Statistic for spatial autocorrelation."
)

mcp.add_tool(gearys_c,
    name="gearys_c",
    description="Compute Global Geary's C Autocorrelation Statistic."
)

mcp.add_tool(getis_ord_g,
    name="getis_ord_g",
    description="Compute Getis-Ord G for global hot spot analysis."
)

mcp.add_tool(getis_ord_g_local,
    name="getis_ord_g_local",
    description="Local Getis-Ord G (Gi*) hot spot analysis per location."
)

mcp.add_tool(gm_lag,
    name="gm_lag",
    description="spreg.GM_Lag spatial 2SLS/GMM-IV spatial lag model."
)

mcp.add_tool(join_counts,
    name="join_counts",
    description="Global Binary Join Counts for binary spatial autocorrelation."
)

mcp.add_tool(join_counts_local,
    name="join_counts_local",
    description="Local Join Counts per location."
)

mcp.add_tool(knn_weights,
    name="knn_weights",
    description="Create k-nearest neighbors spatial weights from point data."
)

mcp.add_tool(moran_local,
    name="moran_local",
    description="Local Moran's I (LISA) — cluster/outlier detection per location."
)

mcp.add_tool(morans_i,
    name="morans_i",
    description="Compute Moran's I Global Autocorrelation Statistic."
)

mcp.add_tool(ols_with_spatial_diagnostics_safe,
    name="ols_with_spatial_diagnostics_safe",
    description="Safe OLS regression with full spatial diagnostics."
)

mcp.add_tool(spatial_markov,
    name="spatial_markov",
    description="Giddy Spatial Markov on panel data (n regions x t periods)."
)

mcp.add_tool(weights_from_shapefile,
    name="weights_from_shapefile",
    description="Create spatial weights matrix from shapefile using contiguity (queen/rook)."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
