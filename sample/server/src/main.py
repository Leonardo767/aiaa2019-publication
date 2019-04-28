from server.src.main_utils import (
    vectorize_nodes, determine_center_node, update_nodes, velocity_saturate)
from server.src.delta_weights import find_delta
from server.lib.data_wrangling.dataUtils import find_contact
from server.src.optimization.feed_forward import init_params, iterate_nodes, determine_cost
from server.src.optimization.back_prop import find_grads, update_params
from server.src.optimization.cost_function import determine_metrics
from server.src.optimization.optimizer import main_opt


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
    param_hist = []
    global_param_dict = {}
    if iter_val == 0:
        return created_nodes, results_package
    for i in range(iter_val):
        print('ITERATION #{}...'.format(i))
        if i != 0:  # update contact points
            contact_points = find_contact(
                created_nodes, created_nodes_sim, sight=sight)
        results_flight_nodes = {}
        param_flight = {}
        for flight_number, leg_times in created_nodes.items():
            results_legs_nodes = {}
            param_leg = {}
            for leg_time, leg_points in leg_times.items():
                contact_points_relevant = contact_points[flight_number][leg_time]
                if len(contact_points_relevant):  # if leg made contact
                    # pre-processing analysis...
                    # ----------------------------------------
                    nodes, points = vectorize_nodes(
                        leg_points, contact_points_relevant)
                    if i == 0:
                        param_dict = init_params(len(leg_points), seed=0)
                    else:
                        param_dict = param_hist[i - 1][flight_number][leg_time]
                    # execute...
                    # ----------------------------------------
                    X_n1, X_o = iterate_nodes(nodes, points, param_dict)
                    cost = determine_cost(X_n1, X_o)
                    grad_dict = find_grads(cost)
                    new_param_dict = update_params(
                        param_dict, grad_dict, alpha=0.05)
                    # post-processing execution results...
                    # ----------------------------------------
                    new_nodes = X_n1.tolist()
                    created_nodes[flight_number][leg_time] = new_nodes
                else:
                    new_nodes = created_nodes[flight_number][leg_time]
                    new_param_dict = {}
                # package results into dict for next iter...
                # ----------------------------------------
                results_legs_nodes[leg_time] = new_nodes
                param_leg[leg_time] = new_param_dict
            results_flight_nodes[flight_number] = results_legs_nodes
            param_flight[flight_number] = param_leg
        metrics = []
        # metrics = determine_metrics(
        # results_flight_nodes, contact_points, original_nodes)
        results_package.append((results_flight_nodes, contact_points, metrics))
        param_hist.append(param_flight)
    return results_package
