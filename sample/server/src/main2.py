from server.src.main_utils import tensorize_nodes
from server.lib.data_wrangling.dataUtils import find_contact
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
    results_package = [[created_nodes, contact_points, 0], [0, 0, 0]]
    if iter_val == 0:
        return created_nodes, results_package
    results_nodes = {}
    results_contact = {}
    for flight_number, leg_times in created_nodes.items():
        results_legs_nodes = {}
        results_legs_contact = {}
        for leg_time, leg_points in leg_times.items():
            contact_points_relevant = contact_points[flight_number][leg_time]
            if len(contact_points_relevant):  # if leg made contact
                X_n, X_o = tensorize_nodes(leg_points, contact_points_relevant)
                print(created_nodes_sim)
                X_n_opt, X_o_opt = main_opt(
                    X_n, X_o, flight_number, leg_time, created_nodes_sim, sight,
                    iter_val)
            else:
                X_n_opt, X_o_opt = X_n, contact_points_relevant
            results_legs_nodes[leg_time] = X_n_opt.tolist()
            results_legs_contact[leg_time] = X_o_opt.tolist()
        results_nodes[flight_number] = results_legs_nodes
        results_contact[flight_number] = results_legs_contact
    results_package[1][0] = results_nodes
    results_package[1][1] = results_contact
    return results_package
