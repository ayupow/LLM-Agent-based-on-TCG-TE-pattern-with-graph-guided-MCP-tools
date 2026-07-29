# Generate all 10 added_*.py server files that import from individual tool files
import os, sys, importlib, inspect

BASE = os.path.dirname(os.path.abspath(__file__))

# Server definitions: (filename, server_name, tool_dir, description_override)
SERVERS = [
    ("added_gis_geopandas.py",  "added_gis_geopandas",  "tools_gis_geopandas",
     {"read_file_gpd": "Reads a geospatial file and returns stats and a data preview.",
      "append_gpd": "Concatenates two shapefiles vertically (row-wise append). Handles CRS mismatch.",
      "merge_gpd": "Merges two shapefiles based on common attribute columns (attribute join).",
      "overlay_gpd": "Overlay two GeoDataFrames using spatial set operations (intersection/union/difference).",
      "dissolve_gpd": "Dissolve geometries by attribute using geopandas.dissolve.",
      "explode_gpd": "Split multi-part geometries into single parts using geopandas.explode.",
      "clip_vector": "Clip vector geometries using a clip polygon boundary.",
      "sjoin_gpd": "Spatial join between two GeoDataFrames (intersects/contains/within/touches/crosses/overlaps).",
      "sjoin_nearest_gpd": "Nearest neighbor spatial join between two GeoDataFrames.",
      "point_in_polygon": "Check if points are inside polygons using spatial join (predicate='within').",
      "write_file_gpd": "Export a GeoDataFrame to file (Shapefile, GeoJSON, GPKG, etc.)."}),

    ("added_gis_shapely.py",    "added_gis_shapely",    "tools_gis_shapely",
     {"buffer": "Create a buffer around a geometry at a given distance.",
      "intersection": "Find the intersection of two geometries.",
      "union": "Combine two geometries into one.",
      "difference": "Find the difference between two geometries (geometry1 minus geometry2).",
      "symmetric_difference": "Find the symmetric difference (XOR area) between two geometries.",
      "convex_hull": "Calculate the convex hull of a geometry.",
      "envelope": "Get the bounding box (envelope) of a geometry.",
      "minimum_rotated_rectangle": "Get the minimum rotated rectangle of a geometry.",
      "get_centroid": "Get the centroid (center of mass) of a geometry.",
      "get_bounds": "Get the bounds (minx, miny, maxx, maxy) of a geometry.",
      "get_coordinates": "Get all coordinates of a geometry.",
      "get_geometry_type": "Get the type of a geometry (Point, LineString, Polygon, etc.).",
      "rotate_geometry": "Rotate a geometry around an origin point.",
      "scale_geometry": "Scale a geometry by x and y factors.",
      "translate_geometry": "Translate (shift) a geometry by offsets.",
      "triangulate_geometry": "Create a Delaunay triangulation from a geometry.",
      "voronoi": "Create a Voronoi diagram from input points.",
      "unary_union_geometries": "Create a union of multiple geometries at once.",
      "get_length": "Get the length of a geometry (perimeter for polygons).",
      "get_area": "Get the area of a geometry.",
      "is_valid": "Check if a geometry is valid according to OGC rules.",
      "make_valid": "Fix an invalid geometry to make it valid.",
      "simplify": "Simplify a geometry by reducing vertices with tolerance.",
      "snap_geometry": "Snap one geometry to another within a tolerance.",
      "nearest_point_on_geometry": "Find the nearest point on geometry2 to geometry1.",
      "normalize_geometry": "Normalize the orientation/order of a geometry (canonical form).",
      "geometry_to_geojson": "Convert a WKT geometry to GeoJSON format.",
      "geojson_to_geometry": "Convert a GeoJSON geometry to WKT format."}),

    ("added_gis_pyproj.py",     "added_gis_pyproj",     "tools_gis_pyproj",
     {"transform_coordinates": "Transform coordinates between two coordinate reference systems (CRS).",
      "project_geometry": "Project a geometry from one CRS to another.",
      "get_crs_info": "Get detailed information about a coordinate reference system.",
      "get_available_crs": "Get the list of available coordinate reference systems.",
      "get_geod_info": "Get information about a geodetic ellipsoid.",
      "calculate_geodetic_distance": "Calculate geodetic (great-circle) distance between two points.",
      "calculate_geodetic_point": "Calculate destination point given start, azimuth, and distance.",
      "calculate_geodetic_area": "Calculate geodesic area of a polygon on the Earth's surface.",
      "get_utm_zone": "Get UTM zone number and letter for given coordinates.",
      "get_utm_crs": "Get UTM CRS string for given coordinates.",
      "get_geocentric_crs": "Get geocentric CRS (ECEF) for given coordinates."}),

    ("added_gis_rasterio.py",   "added_gis_rasterio",   "tools_gis_rasterio",
     {"zonal_statistics": "Calculate statistics of raster values within polygon zones.",
      "reclassify_raster": "Reclassify raster values using a mapping dictionary.",
      "focal_statistics": "Compute moving-window statistics on a raster.",
      "hillshade": "Generate hillshade from a DEM raster.",
      "write_raster": "Write a numpy array to a raster file using reference raster metadata.",
      "metadata_raster": "Open a raster dataset and return metadata (driver, dims, CRS, bounds, bands).",
      "get_raster_crs": "Retrieve the CRS of a raster dataset.",
      "clip_raster_with_shapefile": "Clip a raster using polygons from a shapefile.",
      "resample_raster": "Resample a raster by a scale factor.",
      "reproject_raster": "Reproject a raster to a new CRS.",
      "extract_band": "Extract a specific band from a multi-band raster.",
      "raster_band_statistics": "Calculate min, max, mean, std for each band of a raster.",
      "tile_raster": "Split a raster into square tiles.",
      "raster_histogram": "Compute histogram of pixel values per band.",
      "compute_ndvi": "Compute NDVI (Normalized Difference Vegetation Index) from red+NIR bands.",
      "raster_algebra": "Perform addition or subtraction on two raster bands with auto-alignment.",
      "concat_bands": "Concatenate single-band rasters into multi-band with auto-alignment.",
      "weighted_band_sum": "Compute weighted sum of all bands in a raster."}),

    ("added_gis_pysal.py",      "added_gis_pysal",      "tools_gis_pysal",
     {"getis_ord_g": "Compute Getis-Ord G for global hot spot analysis.",
      "morans_i": "Compute Moran's I Global Autocorrelation Statistic.",
      "gearys_c": "Compute Global Geary's C Autocorrelation Statistic.",
      "gamma_statistic": "Compute Gamma Statistic for spatial autocorrelation.",
      "moran_local": "Local Moran's I (LISA) — cluster/outlier detection per location.",
      "getis_ord_g_local": "Local Getis-Ord G (Gi*) hot spot analysis per location.",
      "join_counts": "Global Binary Join Counts for binary spatial autocorrelation.",
      "join_counts_local": "Local Join Counts per location.",
      "adbscan": "Adaptive DBSCAN clustering for spatial point data.",
      "weights_from_shapefile": "Create spatial weights matrix from shapefile using contiguity (queen/rook).",
      "distance_band_weights": "Create distance-based spatial weights from point data.",
      "knn_weights": "Create k-nearest neighbors spatial weights from point data.",
      "build_transform_and_save_weights": "Build spatial weights, transform, and save to file.",
      "ols_with_spatial_diagnostics_safe": "Safe OLS regression with full spatial diagnostics.",
      "build_and_transform_weights": "Build and transform spatial weights in one step.",
      "spatial_markov": "Giddy Spatial Markov on panel data (n regions x t periods).",
      "dynamic_lisa": "Dynamic directional LISA for spatiotemporal autocorrelation.",
      "gm_lag": "spreg.GM_Lag spatial 2SLS/GMM-IV spatial lag model."}),

    ("added_gis_data.py",       "added_gis_data",       "tools_gis_data",
     {"download_boundaries": "Download administrative boundary data for a region from OSM/geoboundaries.",
      "download_climate_data": "Download climate data (temperature, precipitation) from WorldClim/ERA5.",
      "get_species_info": "Get taxonomic and ecological info about a species from GBIF.",
      "download_species_occurrences": "Download species occurrence records from GBIF.",
      "download_worldcover": "Download ESA WorldCover land cover classification data.",
      "compute_s2_ndvi": "Compute Sentinel-2 NDVI on-demand from Microsoft Planetary Computer.",
      "download_street_network": "Download street network for a place using osmnx.",
      "calculate_shortest_path": "Calculate shortest path between two points on a street network.",
      "download_satellite_imagery": "Download analysis-ready satellite imagery from Planetary Computer (STAC+SAS)."}),

    ("added_gis_visualize.py",  "added_gis_visualize",  "tools_gis_visualize",
     {"create_map": "Create a static map visualization from geospatial data (PNG/HTML).",
      "create_web_map": "Create an interactive web map using folium/leaflet (HTML)."}),

    ("added_gis_utilities.py",  "added_gis_utilities",  "tools_gis_utilities",
     {"save_results": "Universal save/export for GIS tool results to JSON/CSV/YAML/XLSX/SHP/GEOJSON/GeoTIFF."}),

    ("added_powerfactory_mcp.py", "added_powerfactory_mcp", "tools_powerfactory",
     {"ping": "Health check — returns 'pong' to verify MCP server is reachable.",
      "close_digsilent": "Close the DIgSILENT PowerFactory API session.",
      "get_config": "Return the active simulation_config.json as a JSON string.",
      "import_project": "Import a DIgSILENT PowerFactory project from a .pfd file and activate it.",
      "create_study_case": "Create and activate a study case without running simulation.",
      "modify_parameter": "Set an attribute on all PowerFactory objects matching a query.",
      "run_loadflow": "Run a load flow calculation (ComLdf) on the active study case.",
      "run_short_circuit": "Run a short-circuit calculation (ComShc) on the active study case.",
      "run_simulation": "Run full RMS simulation pipeline: connect → load flow → RMS → CSV → plots.",
      "run_custom_case": "Run a single custom fault case with parameters at call-time.",
      "read_results_csv": "Read RMS simulation results CSV. Auto-discovers latest file."}),

    ("added_networkx_mcp.py",   "added_networkx_mcp",   "tools_networkx",
     {"create_graph": "Create a new graph (undirected or directed).",
      "add_nodes": "Add nodes to an existing graph.",
      "add_edges": "Add edges to an existing graph.",
      "get_info": "Get basic graph information (nodes, edges, directed).",
      "list_graphs": "List all stored graphs with summary info.",
      "delete_graph": "Delete a graph from storage.",
      "remove_nodes": "Remove nodes from a graph.",
      "remove_edges": "Remove edges from a graph.",
      "shortest_path": "Find shortest path between two nodes using BFS/Dijkstra.",
      "get_neighbors": "Get all neighbors of a node.",
      "set_node_attributes": "Set attributes on one or more nodes.",
      "get_node_attributes": "Get all attributes of a specific node.",
      "degree_centrality": "Calculate degree centrality for all nodes.",
      "betweenness_centrality": "Calculate betweenness centrality for all nodes.",
      "connected_components": "Find connected components in the graph.",
      "pagerank": "Calculate PageRank for all nodes.",
      "community_detection": "Detect communities using Louvain (greedy modularity) method.",
      "clustering_coefficients": "Calculate clustering coefficients for all nodes.",
      "graph_statistics": "Calculate comprehensive graph statistics (density, diameter, degree distribution).",
      "minimum_spanning_tree": "Find minimum spanning tree of an undirected graph.",
      "cycles_detection": "Detect cycles: cycle basis for undirected, DAG check for directed.",
      "graph_coloring": "Color graph vertices using greedy algorithm.",
      "centrality_measures": "Calculate multiple centrality measures (degree/betweenness/closeness/eigenvector).",
      "matching": "Find maximum weight matching in a graph.",
      "maximum_flow": "Calculate maximum flow in a directed graph.",
      "topological_sort": "Return a topological ordering of a directed acyclic graph.",
      "subgraph": "Extract an induced subgraph and store as a new graph.",
      "merge_graphs": "Compose two graphs into a new graph (union of nodes and edges).",
      "visualize_graph": "Create a base64-encoded PNG visualization of the graph.",
      "import_csv": "Import graph from CSV edge list (source,target per line).",
      "export_json": "Export graph as JSON in node-link format."}),
]

def generate_server_file(filename, server_name, tool_dir, descriptions):
    tool_dir_path = os.path.join(BASE, tool_dir)
    tool_files = sorted(f for f in os.listdir(tool_dir_path) if f.endswith('.py') and not f.startswith('_'))

    lines = []
    lines.append(f'# {server_name} — MCP Server')
    lines.append(f'# Auto-generated from {tool_dir}/ individual tool files')
    lines.append('import sys, os')
    lines.append(f"sys.path.insert(0, os.path.join(os.path.dirname(__file__), '{tool_dir}'))")
    lines.append('')
    lines.append('from mcp.server.fastmcp import FastMCP')
    lines.append('')

    # Import each tool function
    for tf in tool_files:
        mod_name = tf[:-3]  # strip .py
        lines.append(f'from {mod_name} import {mod_name}')

    lines.append('')
    lines.append(f'mcp = FastMCP(name="{server_name}")')
    lines.append('')

    # Register each tool
    for tf in tool_files:
        func_name = tf[:-3]
        desc = descriptions.get(func_name, f"Tool: {func_name}")
        lines.append(f'mcp.add_tool({func_name},')
        lines.append(f'    name="{func_name}",')
        lines.append(f'    description="{desc}"')
        lines.append(')')
        lines.append('')

    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    mcp.run(transport="stdio")')
    lines.append('')

    path = os.path.join(BASE, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'  Generated: {filename} ({len(tool_files)} tools)')

if __name__ == '__main__':
    for filename, server_name, tool_dir, descs in SERVERS:
        generate_server_file(filename, server_name, tool_dir, descs)
    print(f'\nDone — {len(SERVERS)} server files generated')
