from server.src.main_utils import (
    vectorize_nodes, determine_center_node, update_nodes)
from server.src.delta_weights import find_delta
from server.lib.data_wrangling.dataUtils import insert_results_plot_data


def main_path_optimizer(created_nodes, contact_points, iter_val=1, legs_observed=2):
    print("Running optimizer for " + str(iter_val) + " iterations...")
    if iter_val == 0:
        return created_nodes, contact_points
    results_plot_data = [[False]*legs_observed]
    for i in range(iter_val):
        print('ITERATION #{}...'.format(i))
        for flight_number, leg_times in created_nodes.items():
            for leg_time, leg_points in leg_times.items():
                contact_points_relevant = contact_points[flight_number][leg_time]
                if len(contact_points_relevant):  # if leg made contact
                    node_vector = vectorize_nodes(leg_points)
                    contact_points_relevant = vectorize_nodes(
                        contact_points_relevant)
                    center_node_idx, sim_point_ends = determine_center_node(
                        node_vector, contact_points_relevant)
                    beta_params = [1, 1, 1]  # tunable params
                    delta_val_vector = find_delta(
                        node_vector, center_node_idx, sim_point_ends, beta_params)
                    proposed_node_vector = update_nodes(
                        node_vector, delta_val_vector, sim_point_ends)
                    # ===========================================
                    # insert velocity limiter here
                    # ===========================================
                    new_nodes = proposed_node_vector.tolist()
                    created_nodes[flight_number][leg_time] = new_nodes
                    # if there is still room in datacard
                    if not results_plot_data[-1]:
                        results_plot_data = insert_results_plot_data(
                            results_plot_data, new_nodes, contact_points_relevant)
        print(created_nodes)
    return created_nodes
