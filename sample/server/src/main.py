from server.src.main_utils import (
    vectorize_nodes, determine_center_node, update_nodes, velocity_saturate)
from server.src.delta_weights import find_delta
from server.lib.data_wrangling.dataUtils import find_contact
from server.src.optimization.cost_function import determine_metrics


def main_path_optimizer(created_nodes, contact_points, created_nodes_sim, sight, original_nodes, v_limit, iter_val=1):
    """
    :param created_nodes: dict {flight_number:{leg_time:[[x_0, y_0, t_0], ..., [x_n, y_n, t_n]]}}, 
                            containing all manipulatable nodes for a given leg
    :param contact_points: same struct as created_nodes, containing initial contact with sim
    :param created_nodes_sim: same struct as created_nodes, containing sim points
    :param sight: drone property, spatial distance within which the drone can make contact with sim
    :param iter_val: user input, determines how many iterations are ran
    :return: results package of iteration history for plotting [(new_nodes, contact_points, metrics)_0,
             ..., (new_nodes, contact_points, metrics)_(iter_val)]]
    """
    print("Running optimizer for {} iterations...".format(iter_val))
    results_package = []
    if iter_val == 0:
        return created_nodes, results_package
    for i in range(iter_val):
        print('ITERATION #{}...'.format(i))
        if not i == 0:  # update contact points
            contact_points = find_contact(
                created_nodes, created_nodes_sim, sight=sight)
        results_flight_nodes = {}
        for flight_number, leg_times in created_nodes.items():
            results_legs_nodes = {}
            for leg_time, leg_points in leg_times.items():
                contact_points_relevant = contact_points[flight_number][leg_time]
                if len(contact_points_relevant):  # if leg made contact
                    # pre-processing analysis...
                    # ----------------------------------------
                    node_vector = vectorize_nodes(leg_points)
                    contact_points_relevant = vectorize_nodes(
                        contact_points_relevant)
                    center_node_idx, sim_point_ends = determine_center_node(
                        node_vector, contact_points_relevant)
                    # execute...
                    # ----------------------------------------
                    beta_params = [1, 1, 1, 1, 1]  # tunable params
                    delta_val_vector = find_delta(
                        node_vector, center_node_idx, sim_point_ends, beta_params)
                    new_node_vector = update_nodes(
                        node_vector, delta_val_vector, sim_point_ends, v_limit)
                    # post-processing execution results...
                    # ----------------------------------------
                    new_nodes = new_node_vector
                    contact_points_relevant = [
                        [round(x, 2) for x in point] for point in contact_points_relevant]
                    created_nodes[flight_number][leg_time] = new_nodes
                else:
                    new_nodes = created_nodes[flight_number][leg_time]
                results_legs_nodes[leg_time] = new_nodes
            results_flight_nodes[flight_number] = results_legs_nodes
        metrics = determine_metrics(
            results_flight_nodes, contact_points, original_nodes)
        # package all results for plotting with a deep copy
        results_package.append((results_flight_nodes, contact_points, metrics))
        # parameter tuning
        # ----------------------------------------

    return results_package
