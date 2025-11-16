import json
import ezdxf

def convert_DWGfile_to_JSONfile(config_json_path: str) -> str:
    """
    config_json_path: JSON 文件，包含以下字段：
        {
            "dwg_file": "example.dwg",
            "output_json": "infrastructure_networks.json"
        }
    """
    with open(config_json_path, 'r') as f:
        config = json.load(f)

    dwg_file_path = config.get("dwg_file")
    output_json_path = config.get("output_json", "infrastructure_networks.json")

    doc = ezdxf.readfile(dwg_file_path)
    msp = doc.modelspace()

    all_network_data = {'nodes': [], 'edges': []}

    for entity in msp:
        if entity.dxftype() == 'POINT':
            coord = [entity.dxf.location.x, entity.dxf.location.y]
            node_prop = {
                'Code': entity.dxf.handle,
                'Facility': None,
                'Service Area': None,
                'Location': None,
                'Demands': None,
                'Coordinates': coord,
                'Infrastructure Type': None
            }
            all_network_data['nodes'].append(node_prop)

        elif entity.dxftype() == 'LINE':
            start = [entity.dxf.start.x, entity.dxf.start.y]
            end = [entity.dxf.end.x, entity.dxf.end.y]
            edge_prop = {
                'Code': entity.dxf.handle,
                'Start': start,
                'End': end,
                'Infrastructure Type': None
            }
            all_network_data['edges'].append(edge_prop)

    with open(output_json_path, 'w') as outfile:
        json.dump(all_network_data, outfile, indent=4)

    return f"The DWG file has been converted and saved to {output_json_path}"
