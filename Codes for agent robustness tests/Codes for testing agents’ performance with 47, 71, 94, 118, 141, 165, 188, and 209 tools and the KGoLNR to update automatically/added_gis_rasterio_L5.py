# added_gis_rasterio_L5 — MCP Server (subset for level L5)
from mcp.server.fastmcp import FastMCP

from extract_band import extract_band
from raster_algebra import raster_algebra
from zonal_statistics import zonal_statistics
from raster_band_statistics import raster_band_statistics
from concat_bands import concat_bands
from hillshade import hillshade
from tile_raster import tile_raster
from get_raster_crs import get_raster_crs
from reclassify_raster import reclassify_raster
from metadata_raster import metadata_raster
from raster_histogram import raster_histogram

mcp = FastMCP(name="added_gis_rasterio_L5")

mcp.add_tool(extract_band,
    name="extract_band",
    description="Tool: extract_band (from gis rasterio server)."
)

mcp.add_tool(raster_algebra,
    name="raster_algebra",
    description="Tool: raster_algebra (from gis rasterio server)."
)

mcp.add_tool(zonal_statistics,
    name="zonal_statistics",
    description="Tool: zonal_statistics (from gis rasterio server)."
)

mcp.add_tool(raster_band_statistics,
    name="raster_band_statistics",
    description="Tool: raster_band_statistics (from gis rasterio server)."
)

mcp.add_tool(concat_bands,
    name="concat_bands",
    description="Tool: concat_bands (from gis rasterio server)."
)

mcp.add_tool(hillshade,
    name="hillshade",
    description="Tool: hillshade (from gis rasterio server)."
)

mcp.add_tool(tile_raster,
    name="tile_raster",
    description="Tool: tile_raster (from gis rasterio server)."
)

mcp.add_tool(get_raster_crs,
    name="get_raster_crs",
    description="Tool: get_raster_crs (from gis rasterio server)."
)

mcp.add_tool(reclassify_raster,
    name="reclassify_raster",
    description="Tool: reclassify_raster (from gis rasterio server)."
)

mcp.add_tool(metadata_raster,
    name="metadata_raster",
    description="Tool: metadata_raster (from gis rasterio server)."
)

mcp.add_tool(raster_histogram,
    name="raster_histogram",
    description="Tool: raster_histogram (from gis rasterio server)."
)

if __name__ == "__main__":
    mcp.run(transport="stdio")
