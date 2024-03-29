import numpy as np
from server.src.calc_utils import find_distance, assign_n, norm_score, find_theta


def find_delta_per_d(d_vector):
    delta_per_d = norm_score(d_vector, 0, 1)
    return delta_per_d


def find_delta_per_theta(node_vector, sim_point_ends):
    theta_vector = find_theta(node_vector, sim_point_ends)
    delta_per_theta = norm_score(theta_vector, np.pi, 1)
    return delta_per_theta


def find_delta_per_n(node_vector, center_node_idx):
    n = assign_n(node_vector.shape[0], center_node_idx)
    delta_per_n = norm_score(n, 0, 1.5)
    return delta_per_n


def find_delta(node_vector, center_node_idx, sim_point_ends, beta_params):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param center_node: node centered between points of first and last contact
    :param sim_point_ends: [[x_s, y_s, t_s], [x_e, y_e, t_e]] two points of first/last sim contact, respectively
    :param beta_params: [[beta_d_s, beta_d_e, beta_theta_s, beta_theta_e, beta_n]]
    :return: distance vector, same length as node vector, except a vector of [d_s, d_e] rather than [x, y, t] vectors
    """
    beta_params = np.reshape(np.asarray(beta_params), (-1, 1))
    d_vector = find_distance(node_vector, sim_point_ends)
    delta_matrix = np.concatenate([find_delta_per_d(d_vector),
                                   find_delta_per_theta(
                                       node_vector, sim_point_ends),
                                   find_delta_per_n(node_vector, center_node_idx)], axis=0)
    delta_matrix = np.multiply(delta_matrix, beta_params)
    delta = np.prod(delta_matrix, axis=0)
    delta = np.power(delta, 0.5)  # amplify vals < 1 by taking yroot()
    # deadband filter out small values of delta
    smallest_delta = 10**(-3)
    delta = np.nan_to_num(delta)
    delta = np.where(delta < smallest_delta, 0, delta)
    # print(delta)
    return delta
