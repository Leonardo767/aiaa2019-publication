from server.src.main_utils import (
    vectorize_nodes, determine_center_node)
from server.src.delta_weights import find_delta


def main_path_optimizer(created_nodes, contact_points, iter_val=1):
    print("Running optimizer for " + str(iter_val) + " iterations...")
    if iter_val == 0:
        return created_nodes, contact_points
    for i in range(iter_val):
        for flight_number, leg_times in created_nodes.items():
            for leg_time, leg_points in leg_times.items():
                contact_points_relevant = contact_points[flight_number][leg_time]
                if len(contact_points_relevant):  # if leg made contact
                    node_vector = vectorize_nodes(leg_points)
                    contact_points_relevant = vectorize_nodes(
                        contact_points_relevant)
                    print()
                    print('NEXT:')
                    print(contact_points_relevant)
                    print(node_vector)
                    print('calcs:')
                    center_node_idx, sim_point_ends = determine_center_node(
                        node_vector, contact_points_relevant)
                    beta_params = [1, 1, 1]
                    delta_val_vector = find_delta(
                        node_vector, center_node_idx, sim_point_ends, beta_params)

    new_nodes = created_nodes
    new_contact_points = contact_points
    return new_nodes, new_contact_points
