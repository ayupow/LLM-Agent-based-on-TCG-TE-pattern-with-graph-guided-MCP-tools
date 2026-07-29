# added_gis_rasterio — MCP Server
# Auto-generated from tools_gis_rasterio/ individual tool files

from mcp.server.fastmcp import FastMCP

from clip_raster_with_shapefile import clip_raster_with_shapefile
from compute_ndvi import compute_ndvi
from concat_bands import concat_bands
from extract_band import extract_band
from focal_statistics import focal_statistics
from get_raster_crs import get_raster_crs
from hillshade import hillshade
from metadata_raster import metadata_raster
from raster_algebra import raster_algebra
from raster_band_statistics import raster_band_statistics
from raster_histogram import raster_histogram
from reclassify_raster import reclassify_raster
from reproject_raster import reproject_raster
from resample_raster import resample_raster
from tile_raster import tile_raster
from weighted_band_sum import weighted_band_sum
from write_raster import write_raster
from zonal_statistics import zonal_statistics

mcp = FastMCP(name="added_gis_rasterio")

mcp.add_tool(clip_raster_with_shapefile,
    name="clip_raster_with_shapefile",
    description="Clip a raster using polygons from a shapefile."
)

mcp.add_tool(compute_ndvi,
    name="compute_ndvi",
    description="Compute NDVI (Normalized Difference Vegetation Index) from red+NIR bands."
)

mcp.add_tool(concat_bands,
    name="concat_bands",
    description="Concatenate single-band rasters into multi-band with auto-alignment."
)

mcp.add_tool(extract_band,
    name="extract_band",
    description="Extract a specific band from a multi-band raster."
)

mcp.add_tool(focal_statistics,
    name="focal_statistics",
    description="Compute moving-window statistics on a raster."
)

mcp.add_tool(get_raster_crs,
    name="get_raster_crs",
    description="Retrieve the CRS of a raster dataset."
)

mcp.add_tool(hillshade,
    name="hillshade",
    description="Generate hillshade from a DEM raster."
)

mcp.add_tool(metadata_raster,
    name="metadata_raster",
    description="Open a raster dataset and return metadata (driver, dims, CRS, bounds, bands)."
)

mcp.add_tool(raster_algebra,
    name="raster_algebra",
    description="Perform addition or subtraction on two raster bands with auto-alignment."
)

mcp.add_tool(raster_band_statistics,
    name="raster_band_statistics",
    description="Calculate min, max, mean, std for each band of a raster."
)

mcp.add_tool(raster_histogram,
    name="raster_histogram",
    description="Compute histogram of pixel values per band."
)

mcp.add_tool(reclassify_raster,
    name="reclassify_raster",
    description="Reclassify raster values using a mapping dictionary."
)

mcp.add_tool(reproject_raster,
    name="reproject_raster",
    description="Reproject a raster to a new CRS."
)

mcp.add_tool(resample_raster,
    name="resample_raster",
    description="Resample a raster by a scale factor."
)

mcp.add_tool(tile_raster,
    name="tile_raster",
    description="Split a raster into square tiles."
)

mcp.add_tool(weighted_band_sum,
    name="weighted_band_sum",
    description="Compute weighted sum of all bands in a raster."
)

mcp.add_tool(write_raster,
    name="write_raster",
    description="Write a numpy array to a raster file using reference raster metadata."
)

mcp.add_tool(zonal_statistics,
    name="zonal_statistics",
    description="Calculate statistics of raster values within polygon zones."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
