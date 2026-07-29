# added_gis_geopandas — MCP Server
# Auto-generated from tools_gis_geopandas/ individual tool files

from mcp.server.fastmcp import FastMCP

from append_gpd import append_gpd
from clip_vector import clip_vector
from dissolve_gpd import dissolve_gpd
from explode_gpd import explode_gpd
from merge_gpd import merge_gpd
from overlay_gpd import overlay_gpd
from point_in_polygon import point_in_polygon
from read_file_gpd import read_file_gpd
from sjoin_gpd import sjoin_gpd
from sjoin_nearest_gpd import sjoin_nearest_gpd
from write_file_gpd import write_file_gpd

mcp = FastMCP(name="added_gis_geopandas")

mcp.add_tool(append_gpd,
    name="append_gpd",
    description="Concatenates two shapefiles vertically (row-wise append). Handles CRS mismatch."
)

mcp.add_tool(clip_vector,
    name="clip_vector",
    description="Clip vector geometries using a clip polygon boundary."
)

mcp.add_tool(dissolve_gpd,
    name="dissolve_gpd",
    description="Dissolve geometries by attribute using geopandas.dissolve."
)

mcp.add_tool(explode_gpd,
    name="explode_gpd",
    description="Split multi-part geometries into single parts using geopandas.explode."
)

mcp.add_tool(merge_gpd,
    name="merge_gpd",
    description="Merges two shapefiles based on common attribute columns (attribute join)."
)

mcp.add_tool(overlay_gpd,
    name="overlay_gpd",
    description="Overlay two GeoDataFrames using spatial set operations (intersection/union/difference)."
)

mcp.add_tool(point_in_polygon,
    name="point_in_polygon",
    description="Check if points are inside polygons using spatial join (predicate='within')."
)

mcp.add_tool(read_file_gpd,
    name="read_file_gpd",
    description="Reads a geospatial file and returns stats and a data preview."
)

mcp.add_tool(sjoin_gpd,
    name="sjoin_gpd",
    description="Spatial join between two GeoDataFrames (intersects/contains/within/touches/crosses/overlaps)."
)

mcp.add_tool(sjoin_nearest_gpd,
    name="sjoin_nearest_gpd",
    description="Nearest neighbor spatial join between two GeoDataFrames."
)

mcp.add_tool(write_file_gpd,
    name="write_file_gpd",
    description="Export a GeoDataFrame to file (Shapefile, GeoJSON, GPKG, etc.)."
)


if __name__ == "__main__":
    mcp.run(transport="stdio")
