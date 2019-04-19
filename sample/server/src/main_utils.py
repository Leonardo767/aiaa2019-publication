import numpy as np
from server.src.calc_utils import find_distance_components


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


def update_nodes(node_vector, delta_val_vector, sim_point_ends):
    d_vector = find_distance_components(node_vector, sim_point_ends)
    delta_val_vector = np.reshape(delta_val_vector, (-1, 1))
    change_vector = np.multiply(d_vector, delta_val_vector)
    proposed_node_vector = np.round(np.add(node_vector, change_vector), 2)
    return proposed_node_vector
