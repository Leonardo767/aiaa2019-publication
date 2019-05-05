import torch
from server.src.optimization.feed_forward_utils import find_distance
from server.lib.data_wrangling.dataUtils import find_contact
from server.lib.data_wrangling.dbUtils import extract_settings
from server.src.main_utils import tensorize_nodes


def construct_input(X_n, X_o):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_in: concatnated tensor of input neurons (d_s, d_e)
    """
    return find_distance(X_n, X_o)


def find_new_contact(X_n_new, flight_number, leg_time, created_nodes_sim, sight):
    contact_points = find_contact(
        {flight_number: {leg_time: X_n_new.tolist()}}, created_nodes_sim, sight=sight)
    contact_points_relevant = contact_points[flight_number][leg_time]
    _, X_o = tensorize_nodes(X_n_new.tolist(), contact_points_relevant)
    return X_o


def construct_output(d_s, d_e, X_o):
    X_n_s = X_o[0, :] - d_s
    X_n_e = X_o[-1, :] = d_e
    X_n = X_n_s + (X_n_e - X_n_s)/2
    return X_n


def main_opt(X_n, X_o, flight_number, leg_time, created_nodes_sim, sight, iter_val):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_n_opt: optimized X_n
    :return X_o_opt: X_o using X_n_opt
    """
    X_n0 = X_n
    leg_time = X_n0[0][2] - (X_n0[1][2] - X_n0[0][2])
    flight_time = X_n0[-1][2] - leg_time
    print(leg_time)
    # build input
    X_in = construct_input(X_n, X_o)

    X_n_opt, X_o_opt = X_n, X_o
    return X_n_opt, X_o_opt
