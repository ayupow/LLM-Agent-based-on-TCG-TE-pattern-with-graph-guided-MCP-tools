import json
import ifcopenshell

def convert_IFC_to_JSON(config_json_path: str) -> str:
    """
    config_json_path: JSON 文件，包含以下字段：
    {
        "ifc_file": "example.ifc",
        "output_json": "infrastructure_networks.json"
    }
    """
    with open(config_json_path, 'r') as f:
        config = json.load(f)

    ifc_file_path = config.get("ifc_file")
    output_json_path = config.get("output_json", "infrastructure_networks.json")

    model = ifcopenshell.open(ifc_file_path)
    all_elements = []
    elements = model.by_type('IfcBuildingElement')
    for elem in elements:
        all_elements.append({
            'GlobalId': elem.GlobalId,
            'Name': elem.Name,
            'Type': elem.is_a()
        })

    with open(output_json_path, 'w') as outfile:
        json.dump({'elements': all_elements}, outfile, indent=4)

    return f"The IFC file has been converted and saved to {output_json_path}"

def convert_RVTfile_to_JSONfile(config_json_path: str) -> str:
    """
    config_json_path: JSON 文件，包含以下字段：
    {
        "rvt_file": "example.rvt",
        "ifc_file": "example.ifc",
        "output_json": "infrastructure_networks.json"
    }
    """
    with open(config_json_path, 'r') as f:
        config = json.load(f)

    # 这里可以根据需求把 RVT 转 IFC 的逻辑加上
    # 当前示例直接使用 IFC 文件
    ifc_file_path = config.get("ifc_file")
    output_json_path = config.get("output_json", "infrastructure_networks.json")

    return convert_IFC_to_JSON(json.dumps({"ifc_file": ifc_file_path, "output_json": output_json_path}))
