import numpy as np


def assign_n(node_vector_length, center_node_idx):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param center_node: node from which (b_s, b_e) are found
    :return: n assignment vector, same length as node vector, except a vector of [n] ints rather than [x, y, t] vectors
    """
    n = []
    for i in range(node_vector_length):
        n.append(i - center_node_idx)
    n = np.reshape(np.asarray(n), (1, -1))
    return n


def find_theta(node_vector, sim_point_ends):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param sim_point_ends: (b_s, b_e) = ([x_s, y_s, t_s], [x_e, y_e, t_e]) two points of first/last sim contact, respectively
    :return: theta vector, same length as node vector, except a vector of [theta] scalars rather than [x, y, t] vectors
    """
    # using cos(theta) = dot(u,v)/(norm(u)*norm(v))
    sim_vector = np.subtract(sim_point_ends[0, :], sim_point_ends[1, :])
    sim_mag = np.linalg.norm(sim_vector)

    d_s_components = np.subtract(node_vector, sim_point_ends[0, :])
    mag_product = np.multiply(np.linalg.norm(d_s_components, axis=1), sim_mag)
    cos_theta_s = np.divide(np.dot(d_s_components, sim_vector), mag_product)
    theta_s = np.reshape(np.arccos(cos_theta_s), (1, -1))

    d_e_components = np.subtract(node_vector, sim_point_ends[1, :])
    mag_product = np.multiply(np.linalg.norm(d_e_components, axis=1), sim_mag)
    cos_theta_e = np.divide(np.dot(d_e_components, sim_vector), mag_product)
    theta_e = np.reshape(np.arccos(cos_theta_e), (1, -1))

    theta = np.concatenate([theta_s, theta_e], axis=0)
    return theta


def find_distance(node_vector, sim_point_ends):
    """
    :param node_vector: vector [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    :param sim_point_ends: (b_s, b_e) = ([x_s, y_s, t_s], [x_e, y_e, t_e]) two points of first/last sim contact, respectively
    :return: distance vector, same length as node vector, except a vector of [d_s, d_e] rather than [x, y, t] vectors
    """
    d_s = np.linalg.norm(np.subtract(
        node_vector, sim_point_ends[0, :]), axis=1)
    d_s = np.reshape(d_s, (1, -1))
    d_e = np.linalg.norm(np.subtract(
        node_vector, sim_point_ends[1, :]), axis=1)
    d_e = np.reshape(d_e, (1, -1))
    d = np.concatenate([d_s, d_e], axis=0)
    return d


def norm_score(x, mu, sigma):
    exp_val = np.divide(-np.power(np.subtract(x, mu), 2), (2*sigma**2))
    norm_score = np.multiply(np.exp(exp_val), 1/(sigma*(2*np.pi)**0.5))
    scaled_norm_score = np.multiply(norm_score, sigma/0.4)
    return scaled_norm_score
