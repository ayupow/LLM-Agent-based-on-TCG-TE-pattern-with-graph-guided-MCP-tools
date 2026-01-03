import json
import networkx as nx

def simulate_failure_scenario_using_FMEA_analysis(main_json_path):
    main_json_path = main_json_path.strip().replace('"', '')


    output_json_path = 'cascading_failure_of_FMEA_analysis_results.json'
    failure_modes_json_path = 'identified_failure_modes.json'

    # 读取包含各个文件路径的 JSON 文件
    with open(main_json_path, 'r') as f:
        file_paths = json.load(f)

    # 根据路径读取 interdependent_infrastructure_networks_with_cascading_information 和 failure_modes
    with open(file_paths['interdependent_infrastructure_networks_with_cascading_information'], 'r') as f:
        network_data = json.load(f)

    with open(file_paths['failure_modes_extended'], 'r') as f:
        failure_modes = json.load(f)

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点，并将基础设施类型、状态、容量和最后维护时间作为属性
    for node in network_data['nodes']:
        G.add_node(node['Code'],
                   layer=node['Infrastructure Type'],
                   status=node['Status'],  # 新增字段
                   capacity=node['Capacity'],  # 新增字段
                   last_maintenance=node['Last Maintenance'])  # 新增字段

    # 添加边，并包含状态和容量
    for edge in network_data['edges']:
        G.add_edge(edge['Start'], edge['End'],
                   infrastructure_type=edge['Infrastructure Type'],
                   status=edge.get('Status', 'operational'),  # 新增字段，默认为 'operational'
                   capacity=edge.get('Capacity', 1000))  # 新增字段，默认为 1000

    # 初始化故障模式识别结果
    identified_modes = []

    # 逐个评估故障模式
    for mode in failure_modes['modes']:
        affected_nodes = []
        # 检查与该故障模式相关的节点
        for node in G.nodes():
            if mode['criteria'] in G.nodes[node]['layer']:  # 根据具体标准识别受影响节点
                affected_nodes.append(node)

        # 记录识别的故障模式和受影响节点
        if affected_nodes:
            identified_modes.append({
                'mode': mode['description'],
                'affected_nodes': affected_nodes,
                'severity': mode['severity'],  # 新增字段
                'occurrence': mode['occurrence'],  # 新增字段
                'detection': mode['detection'],  # 新增字段
                'mitigation_strategy': mode['mitigation_strategy'],  # 新增字段
                'recovery_actions': mode['recovery_actions'],  # 新增字段
                'cost_implications': mode['cost_implications'],  # 新增字段
                'responsible_party': mode['responsible_party']  # 新增字段
            })

    # 保存识别的故障模式到 identified_failure_modes.json 文件
    with open(failure_modes_json_path, 'w') as f:
        json.dump({"identified_failure_modes": identified_modes}, f, indent=4)

    # 保存 FMEA 分析结果到输出文件
    with open(output_json_path, 'w') as f:
        json.dump({"fmea_results": identified_modes}, f, indent=4)

    # 更新 Global_Data.json 文件，写入新的路径
    file_paths['cascading_failure_of_FMEA_analysis_results'] = output_json_path
    file_paths['identified_failure_modes'] = failure_modes_json_path
    with open(main_json_path, 'w') as f:
        json.dump(file_paths, f, indent=4)

    return "The cascading failure identification by FMEA results and identified failure modes have been saved in Global_Data.json"


