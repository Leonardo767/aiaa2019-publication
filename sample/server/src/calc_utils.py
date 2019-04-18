import numpy as np


def assign_n(node_vector, center_node):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param center_node: node from which (b_s, b_e) are found
    :return: n assignment vector, same length as node vector, except a vector of [n] scalars rather than [x, y, t] vectors
    """
    n = 0
    return n


def find_theta(node_vector, sim_point_ends):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param sim_point_ends: (b_s, b_e) = ([x_s, y_s, t_s], [x_e, y_e, t_e]) two points of first/last sim contact, respectively
    :return: theta vector, same length as node vector, except a vector of [theta] scalars rather than [x, y, t] vectors
    """
    theta = 0
    return theta


def find_distance(node_vector, sim_point_ends):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param sim_point_ends: (b_s, b_e) = ([x_s, y_s, t_s], [x_e, y_e, t_e]) two points of first/last sim contact, respectively
    :return: distance vector, same length as node vector, except a vector of [d] scalars rather than [x, y, t] vectors
    """
    d = 0
    return d
