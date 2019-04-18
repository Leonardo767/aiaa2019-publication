from server.src.main_utils import vectorize_nodes, determine_center_node


def main_path_optimizer(created_nodes, contact_points, iter_val=1):
    print("Running optimizer for " + str(iter_val) + " iterations...")
    print(contact_points)
    if iter_val == 0:
        return created_nodes, contact_points
    for i in range(iter_val):
        for flight_number, leg_times in created_nodes.items():
            for leg_time, leg_points in leg_times.items():
                node_vector = vectorize_nodes(leg_points)
                contact_points_relevant = contact_points[flight_number][leg_time]
                center_node, sim_point_ends = determine_center_node(
                    node_vector, contact_points_relevant)
    new_nodes = created_nodes
    new_contact_points = contact_points
    return new_nodes, new_contact_points
