import json
import networkx as nx
import random
import math
import copy
import pandas as pd


def schedule_restoration_sequence_considering_population_by_SA(global_json_path):
    # Clean path
    global_json_path = global_json_path.strip().replace('\n', '')

    # Load global data
    with open(global_json_path, 'r') as f:
        global_data = json.load(f)

    # Load paths from global data
    network_path = global_data["interdependent_infrastructure_networks_with_different_resource_demand"]
    cascading_failure_path = global_data["cascading_failure_identification_by_big_nodes_attacks"]
    population_data_path = global_data["population_data"]

    # Load data from files
    with open(network_path, 'r') as f:
        network_data = json.load(f)
    with open(cascading_failure_path, 'r') as f:
        failed_nodes = json.load(f)["failed_nodes"]
    with open(population_data_path, 'r') as f:
        population_data = json.load(f)

    # Create directed graph from network data
    G = nx.DiGraph()
    for edge in network_data["edges"]:
        G.add_edge(edge["Start"], edge["End"])

    # Helper function to calculate the total population affected by a list of recovered nodes
    def calculate_population_affected(recovered_nodes):
        affected_population = 0
        affected_areas = set()
        for node in recovered_nodes:
            for n in network_data["nodes"]:
                if n["Code"] == node and n["Service Area"]:
                    areas = n["Service Area"].split(',')
                    for area in areas:
                        affected_areas.add(area)
        for area in affected_areas:
            for data in population_data:
                if data["Id"] == area:
                    affected_population += data["Population"]
        return affected_population, affected_areas

    # Simulated Annealing parameters
    initial_temp = 1000
    cooling_rate = 0.95
    min_temp = 1
    max_iterations = 1000

    # Initialize solution: random permutation of failed nodes
    current_solution = list(failed_nodes)
    random.shuffle(current_solution)
    current_population, _ = calculate_population_affected(current_solution)
    best_solution = copy.deepcopy(current_solution)
    best_population = current_population

    # Store all accepted solutions
    all_solutions = []

    # Simulated Annealing process
    temp = initial_temp
    iteration = 0

    while temp > min_temp and iteration < max_iterations:
        # Generate neighbor solution by swapping two nodes
        neighbor = copy.deepcopy(current_solution)
        if len(neighbor) >= 2:
            i, j = random.sample(range(len(neighbor)), 2)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        # Calculate neighbor's objective value
        neighbor_population, neighbor_areas = calculate_population_affected(neighbor)

        # Calculate cost difference (maximizing population, so use negative difference)
        cost_diff = current_population - neighbor_population

        # Accept or reject neighbor
        if cost_diff <= 0 or random.random() < math.exp(-cost_diff / temp):
            current_solution = neighbor
            current_population = neighbor_population

            # Record accepted solution
            daily_recovery_order = []
            cumulative_population_restored = 0
            restored_areas_set = set()
            day = 1
            for node in current_solution:
                population_gain, affected_areas = calculate_population_affected([node])
                cumulative_population_restored += population_gain
                restored_areas_set.update(affected_areas)
                daily_recovery_order.append({
                    "day": day,
                    "recovered_node": node,
                    "restored_areas": list(restored_areas_set),
                    "cumulative_population_restored": cumulative_population_restored
                })
                day += 1
            all_solutions.append({
                "iteration": iteration + 1,
                "solution": daily_recovery_order,
                "total_population_restored": current_population
            })

        # Update best solution if neighbor is better
        if neighbor_population > best_population:
            best_solution = copy.deepcopy(neighbor)
            best_population = neighbor_population

        # Cool down
        temp *= cooling_rate
        iteration += 1

    # Generate daily recovery order for the best solution
    daily_recovery_order = []
    cumulative_population_restored = 0
    restored_areas_set = set()
    day = 1

    for node in best_solution:
        population_gain, affected_areas = calculate_population_affected([node])
        cumulative_population_restored += population_gain
        restored_areas_set.update(affected_areas)
        daily_recovery_order.append({
            "day": day,
            "recovered_node": node,
            "restored_areas": list(restored_areas_set),
            "cumulative_population_restored": cumulative_population_restored
        })
        print(f"Day {day} - Recovered node: {node}")
        print(f"Cumulative population restored: {cumulative_population_restored}")
        day += 1

    # Save best solution to JSON
    output_json_path = 'recovery_sequence_considering_population_by_SA.json'
    with open(output_json_path, 'w') as f:
        json.dump(daily_recovery_order, f, indent=4)

    # Save all solutions to JSON
    all_solutions_json_path = 'all_solutions_by_SA.json'
    with open(all_solutions_json_path, 'w') as f:
        json.dump(all_solutions, f, indent=4)

    # Convert all solutions to Excel
    all_solutions_excel_path = 'all_solutions_by_SA.xlsx'
    data_rows = []
    for solution in all_solutions:
        iteration = solution["iteration"]
        for entry in solution["solution"]:
            data_rows.append({
                "Iteration": iteration,
                "Day": entry["day"],
                "Recovered Node": entry["recovered_node"],
                "Restored Areas": ", ".join(entry["restored_areas"]),
                "Cumulative Population Restored": entry["cumulative_population_restored"]
            })
    df = pd.DataFrame(data_rows)
    df.to_excel(all_solutions_excel_path, index=False, sheet_name="Solutions")

    # Update global data output path
    global_data["recovery_sequence_considering_population_by_SA"] = output_json_path
    global_data["all_solutions_by_SA"] = all_solutions_json_path
    global_data["all_solutions_excel_by_SA"] = all_solutions_excel_path
    with open(global_json_path, 'w') as f:
        json.dump(global_data, f, indent=4)

    return "The path to recovery order result, all solutions JSON, and all solutions Excel have been saved in global_data.json"

schedule_restoration_sequence_considering_population_by_SA("Global_Data.json")