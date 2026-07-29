# added_gis_rasterio_L7 — MCP Server (subset for level L7)
from mcp.server.fastmcp import FastMCP

from clip_raster_with_shapefile import clip_raster_with_shapefile
from compute_ndvi import compute_ndvi
from concat_bands import concat_bands
from focal_statistics import focal_statistics
from get_raster_crs import get_raster_crs
from raster_algebra import raster_algebra
from raster_band_statistics import raster_band_statistics
from raster_histogram import raster_histogram
from reclassify_raster import reclassify_raster
from tile_raster import tile_raster
from weighted_band_sum import weighted_band_sum
from write_raster import write_raster
from zonal_statistics import zonal_statistics
from reproject_raster import reproject_raster
from metadata_raster import metadata_raster
from extract_band import extract_band
from hillshade import hillshade
from resample_raster import resample_raster

mcp = FastMCP(name="added_gis_rasterio_L7")

mcp.add_tool(clip_raster_with_shapefile,
    name="clip_raster_with_shapefile",
    description="Tool: clip_raster_with_shapefile (from gis rasterio server)."
)

mcp.add_tool(compute_ndvi,
    name="compute_ndvi",
    description="Tool: compute_ndvi (from gis rasterio server)."
)

mcp.add_tool(concat_bands,
    name="concat_bands",
    description="Tool: concat_bands (from gis rasterio server)."
)

mcp.add_tool(focal_statistics,
    name="focal_statistics",
    description="Tool: focal_statistics (from gis rasterio server)."
)

mcp.add_tool(get_raster_crs,
    name="get_raster_crs",
    description="Tool: get_raster_crs (from gis rasterio server)."
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

mcp.add_tool(reproject_raster,
    name="reproject_raster",
    description="Tool: reproject_raster (from gis rasterio server)."
)

mcp.add_tool(metadata_raster,
    name="metadata_raster",
    description="Tool: metadata_raster (from gis rasterio server)."
)

mcp.add_tool(extract_band,
    name="extract_band",
    description="Tool: extract_band (from gis rasterio server)."
)

mcp.add_tool(hillshade,
    name="hillshade",
    description="Tool: hillshade (from gis rasterio server)."
)

mcp.add_tool(resample_raster,
    name="resample_raster",
    description="Tool: resample_raster (from gis rasterio server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
