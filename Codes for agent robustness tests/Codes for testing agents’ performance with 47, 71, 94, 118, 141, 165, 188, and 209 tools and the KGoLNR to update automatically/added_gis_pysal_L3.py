# added_gis_pysal_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from adbscan import adbscan
from build_and_transform_weights import build_and_transform_weights
from distance_band_weights import distance_band_weights
from getis_ord_g import getis_ord_g
from gm_lag import gm_lag
from join_counts import join_counts
from moran_local import moran_local
from morans_i import morans_i
from ols_with_spatial_diagnostics_safe import ols_with_spatial_diagnostics_safe
from weights_from_shapefile import weights_from_shapefile

mcp = FastMCP(name="added_gis_pysal_L3")

mcp.add_tool(adbscan,
    name="adbscan",
    description="Tool: adbscan (from gis pysal server)."
)

mcp.add_tool(build_and_transform_weights,
    name="build_and_transform_weights",
    description="Tool: build_and_transform_weights (from gis pysal server)."
)

mcp.add_tool(distance_band_weights,
    name="distance_band_weights",
    description="Tool: distance_band_weights (from gis pysal server)."
)

mcp.add_tool(getis_ord_g,
    name="getis_ord_g",
    description="Tool: getis_ord_g (from gis pysal server)."
)

mcp.add_tool(gm_lag,
    name="gm_lag",
    description="Tool: gm_lag (from gis pysal server)."
)

mcp.add_tool(join_counts,
    name="join_counts",
    description="Tool: join_counts (from gis pysal server)."
)

mcp.add_tool(moran_local,
    name="moran_local",
    description="Tool: moran_local (from gis pysal server)."
)

mcp.add_tool(morans_i,
    name="morans_i",
    description="Tool: morans_i (from gis pysal server)."
)

mcp.add_tool(ols_with_spatial_diagnostics_safe,
    name="ols_with_spatial_diagnostics_safe",
    description="Tool: ols_with_spatial_diagnostics_safe (from gis pysal server)."
)

mcp.add_tool(weights_from_shapefile,
    name="weights_from_shapefile",
    description="Tool: weights_from_shapefile (from gis pysal server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
