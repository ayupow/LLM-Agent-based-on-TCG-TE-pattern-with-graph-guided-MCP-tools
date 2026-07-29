# added_gis_rasterio_L3 — MCP Server (subset for level L3)
from mcp.server.fastmcp import FastMCP

from concat_bands import concat_bands
from extract_band import extract_band
from focal_statistics import focal_statistics
from metadata_raster import metadata_raster
from raster_algebra import raster_algebra
from raster_band_statistics import raster_band_statistics
from raster_histogram import raster_histogram
from reclassify_raster import reclassify_raster
from resample_raster import resample_raster
from tile_raster import tile_raster
from weighted_band_sum import weighted_band_sum
from write_raster import write_raster
from zonal_statistics import zonal_statistics

mcp = FastMCP(name="added_gis_rasterio_L3")

mcp.add_tool(concat_bands,
    name="concat_bands",
    description="Tool: concat_bands (from gis rasterio server)."
)

mcp.add_tool(extract_band,
    name="extract_band",
    description="Tool: extract_band (from gis rasterio server)."
)

mcp.add_tool(focal_statistics,
    name="focal_statistics",
    description="Tool: focal_statistics (from gis rasterio server)."
)

mcp.add_tool(metadata_raster,
    name="metadata_raster",
    description="Tool: metadata_raster (from gis rasterio server)."
)

mcp.add_tool(raster_algebra,
    name="raster_algebra",
    description="Tool: raster_algebra (from gis rasterio server)."
)

mcp.add_tool(raster_band_statistics,
    name="raster_band_statistics",
    description="Tool: raster_band_statistics (from gis rasterio server)."
)

mcp.add_tool(raster_histogram,
    name="raster_histogram",
    description="Tool: raster_histogram (from gis rasterio server)."
)

mcp.add_tool(reclassify_raster,
    name="reclassify_raster",
    description="Tool: reclassify_raster (from gis rasterio server)."
)

mcp.add_tool(resample_raster,
    name="resample_raster",
    description="Tool: resample_raster (from gis rasterio server)."
)

mcp.add_tool(tile_raster,
    name="tile_raster",
    description="Tool: tile_raster (from gis rasterio server)."
)

mcp.add_tool(weighted_band_sum,
    name="weighted_band_sum",
    description="Tool: weighted_band_sum (from gis rasterio server)."
)

mcp.add_tool(write_raster,
    name="write_raster",
    description="Tool: write_raster (from gis rasterio server)."
)

mcp.add_tool(zonal_statistics,
    name="zonal_statistics",
    description="Tool: zonal_statistics (from gis rasterio server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
