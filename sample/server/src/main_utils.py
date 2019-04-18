import numpy as np


def vectorize_nodes(nodes_list):
    """
    :param nodes_list: [[x_0, y_0, t_0], ... [x_n, y_n, t_n]] from interpolated nodes dictionary
    :return: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    """
    node_vector = np.asarray(nodes_list)
    return node_vector


def determine_center_node(node_vector, contact_points_relevant):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param contact_points_relevant: sim points which this leg of this flight encountered
    :return: node from which (b_s, b_e) are found
    """
    center_node = 0
    sim_points_end = 0
    return center_node, sim_points_end
