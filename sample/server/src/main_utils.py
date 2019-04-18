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
    :param node_vector: array [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param contact_points_relevant: sim points which this leg of this flight encountered
    :return center_node: node centered between points of first and last contact
    :return sim_point_ends: node from which (b_s, b_e) are found
    """
    sim_point_ends = np.asarray([
        contact_points_relevant[0, :], contact_points_relevant[-1, :]])
    midtime = sim_point_ends[0, 2] + \
        (sim_point_ends[1, 2] - sim_point_ends[0, 2])/2
    elapsed_since_midtime = np.absolute(node_vector[:, 2] - midtime)
    center_node_idx = np.argmin(elapsed_since_midtime)
    return center_node_idx, sim_point_ends
