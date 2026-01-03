import json
from dbfread import DBF

def convert_DBFfile_to_JSONfile(json_input_path: str) -> str:
    json_input_path = json_input_path.strip().replace('"', '')

    with open(json_input_path, 'r') as file:
        data = json.load(file)

    infrastructure_information = data['infrastructure_information']
    with open(infrastructure_information, 'r') as file:
        data = json.load(file)

    network_files = data['network_dbf_files']
    all_network_data = {'nodes': [], 'edges': []}

    for network in network_files:
        points_file = network['points']
        lines_file = network['lines']

        # Read DBF points
        points_dbf = DBF(points_file, load=True)
        points_list = list(points_dbf)
        for row in points_list:
            coords = [row.get('X'), row.get('Y')]  # Assume 'X' and 'Y' fields exist
            node_prop = {
                'Code': row.get('Code'), 'Facility': row.get('Facility'),
                'Service Area': row.get('SA'), 'Location': row.get('location'),
                'Demands': row.get('Demands'),
                'Coordinates': coords,
                'Infrastructure Type': row.get('IT')
            }
            all_network_data['nodes'].append(node_prop)

        # Read DBF lines
        lines_dbf = DBF(lines_file, load=True)
        lines_list = list(lines_dbf)
        for row in lines_list:
            edge_prop = {
                'Code': row.get('Code'),
                'Start': row.get('Start_node'),
                'End': row.get('End_node'),
                'Infrastructure Type': row.get('IT')
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
