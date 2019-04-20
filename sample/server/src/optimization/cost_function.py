import numpy as np


def determine_metrics(results_flight_nodes, contact_points, original_nodes):
    cost = {}
    for flight_number, leg_times in results_flight_nodes.items():
        cost_leg_times = {}
        for leg_time, leg_points in leg_times.items():
            contact_points_relevant = contact_points[flight_number][leg_time]
            if len(contact_points_relevant):  # if leg made contact
                # determine path deviation, if any:
                metrics_path_dev = find_path_deviation(
                    leg_points, original_nodes[flight_number][leg_time])
                # determine standard dev of node spacing:
                metrics_internode_std = find_internode_std(leg_points)
                # reward contact points:
                metrics_contacted = count_contacted(contact_points_relevant)
                # determine total cost for this path:
                total_cost = find_total_cost(
                    metrics_path_dev, metrics_internode_std, metrics_contacted)
            else:
                metrics_path_dev = 0
                metrics_internode_std = 0
                metrics_contacted = 0
                total_cost = 0
            cost_leg_times[leg_time] = total_cost
        cost[flight_number] = cost_leg_times
    # determine total cost for this iteration (info only):
    total_cost_all = 0
    for flight_number, leg_times in cost.items():
        for leg_time, _ in leg_times.items():
            total_cost_all += cost[flight_number][leg_time]
    metrics = (cost, total_cost_all)
    return metrics


def find_path_deviation(node_vector, original_nodes):
    diff = np.linalg.norm(np.subtract(original_nodes, node_vector), axis=1)
    path_start = original_nodes[0, :]
    path_end = original_nodes[-1, :]
    orig_path_length = np.linalg.norm(np.subtract(path_end, path_start))
    metrics_path_dev = np.average(np.divide(diff, orig_path_length))
    return metrics_path_dev


def find_internode_std(node_vector):
    return 0


def count_contacted(contacted_points_relevant):
    return 0


def find_total_cost(metrics_path_dev, metrics_internode_std, metrics_contacted):
    return 0
