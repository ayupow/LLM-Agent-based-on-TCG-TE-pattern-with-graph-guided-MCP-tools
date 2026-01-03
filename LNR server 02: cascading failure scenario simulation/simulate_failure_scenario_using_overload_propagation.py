import json
import networkx as nx


def simulate_failure_scenario_using_overload_propagation(main_json_path):
    main_json_path = main_json_path.strip().replace('"', '')
    output_json_path = 'cascading_failure_identification_using_overload_propagation.json'

    # 读取 global_data.json 文件
    with open(main_json_path, 'r') as f:
        file_paths = json.load(f)

    # 读取网络拓扑文件
    with open(file_paths['interdependent_infrastructure_networks'], 'r') as f:
        network_topology = json.load(f)

    # 读取负载分布文件
    with open(file_paths['load_distribution'], 'r') as f:
        load_distribution = json.load(f)

    # 读取失效事件记录文件
    with open(file_paths['failure_information'], 'r') as f:
        failure_events = json.load(f)

    # 构建有向图
    G = nx.DiGraph()

    # 添加节点到网络
    for node in network_topology['nodes']:
        G.add_node(node['Code'], **node)

    # 添加边到网络
    for edge in network_topology['edges']:
        G.add_edge(edge['Start'], edge['End'], **edge)

    # 构建节点负载和容量的字典
    node_data = {entry['Code']: {'load': entry['Initial Load'], 'capacity': entry['Capacity']} for entry in
                 load_distribution['nodes']}

    # 获取初始失效节点，只考虑 reason 为 "overload" 的节点
    failed_nodes = [event['failed_facilities'] for event in failure_events['failures'] if event['reason'] == "overload"]

    cascading_failures = []  # 记录级联失效的历史
    processed_failed_nodes = set(failed_nodes)

    # 处理级联失效
    while failed_nodes:
        new_failed_nodes = []
        for node in failed_nodes:
            if not G.has_node(node):
                continue

            # 记录失效节点信息
            cascading_failures.append({
                'failed_node': node,
                'load': node_data[node]['load'],
                'capacity': node_data[node]['capacity']
            })

            # 获取邻居节点（从失效节点出发的边的终点）
            neighbors = [edge[1] for edge in G.out_edges(node)]
            if neighbors:
                load_to_redistribute = node_data[node]['load']
                load_per_neighbor = load_to_redistribute / len(neighbors)

                for neighbor in neighbors:
                    node_data[neighbor]['load'] += load_per_neighbor
                    # 检查是否超出容量
                    if node_data[neighbor]['load'] > node_data[neighbor]['capacity']:
                        node_data[neighbor]['load'] = node_data[neighbor]['capacity']  # 限制负载
                        new_failed_nodes.append(neighbor)

        processed_failed_nodes.update(failed_nodes)
        failed_nodes = new_failed_nodes

    # 保存更新后的级联失效记录到新文件
    with open(output_json_path, 'w') as f:
        json.dump(cascading_failures, f, indent=4)

    # 更新 global_data.json 文件，写入新的路径
    file_paths['cascading_failure_identification_using_overload_propagation'] = output_json_path
    with open(main_json_path, 'w') as f:
        json.dump(file_paths, f, indent=4)

    return "The cascading failure behavior has been simulated and saved to the specified JSON files."
