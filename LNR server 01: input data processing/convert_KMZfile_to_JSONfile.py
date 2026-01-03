import json
import zipfile
from fastkml import kml
from shapely.geometry import Point, LineString

def convert_KMZfile_to_JSONfile(json_input_path: str) -> str:
    json_input_path = json_input_path.strip().replace('"', '')

    with open(json_input_path, 'r') as file:
        data = json.load(file)

    infrastructure_information = data['infrastructure_information']
    with open(infrastructure_information, 'r') as file:
        data = json.load(file)

    network_files = data['network_kmz_files']
    all_network_data = {'nodes': [], 'edges': []}

    for network in network_files:
        points_file = network['points']
        lines_file = network['lines']

        # Extract and parse points KMZ
        with zipfile.ZipFile(points_file, 'r') as kmz:
            kmz.extractall('temp_points_kmz')
        kml_file_path = 'temp_points_kmz/doc.kml'
        with open(kml_file_path, 'rt', encoding='utf-8') as f:
            doc = f.read()

        k = kml.KML()
        k.from_string(doc)
        features = list(k.features())
        placemarks = []
        for feature in features:
            placemarks.extend(list(feature.features()))

        for placemark in placemarks:
            geom = placemark.geometry
            if isinstance(geom, Point):
                coords = [geom.x, geom.y]
                props = placemark.extended_data.elements if placemark.extended_data else {}
                node_prop = {
                    'Code': props.get('Code'),
                    'Facility': props.get('Facility'),
                    'Service Area': props.get('SA'),
                    'Location': props.get('location'),
                    'Demands': props.get('Demands'),
                    'Coordinates': coords,
                    'Infrastructure Type': props.get('IT')
                }
                all_network_data['nodes'].append(node_prop)

        # Extract and parse lines KMZ (similar process, handle LineString geometries)
        with zipfile.ZipFile(lines_file, 'r') as kmz:
            kmz.extractall('temp_lines_kmz')
        kml_file_path = 'temp_lines_kmz/doc.kml'
        with open(kml_file_path, 'rt', encoding='utf-8') as f:
            doc = f.read()

        k = kml.KML()
        k.from_string(doc)
        features = list(k.features())
        placemarks = []
        for feature in features:
            placemarks.extend(list(feature.features()))

        for placemark in placemarks:
            geom = placemark.geometry
            if isinstance(geom, LineString):
                props = placemark.extended_data.elements if placemark.extended_data else {}
                edge_prop = {
                    'Code': props.get('Code'),
                    'Start': props.get('Start_node'),
                    'End': props.get('End_node'),
                    'Infrastructure Type': props.get('IT')
                }
                all_network_data['edges'].append(edge_prop)

    output_json_path = 'infrastructure_networks.json'
    with open(output_json_path, 'w') as outfile:
        json.dump(all_network_data, outfile, indent=4)

    with open(json_input_path, 'r') as file:
        global_data = json.load(file)
    global_data['infrastructure_networks'] = output_json_path
    with open(json_input_path, 'w') as file:
        json.dump(global_data, file, indent=4)

    return "The path to infrastructure_networks has been saved in Global_data.json"
