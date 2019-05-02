import numpy as np
import torch
from server.src.calc_utils import find_distance_components


def tensorize_nodes(leg_points, contact_points_relevant):
    """
    :param nodes_list: [[x_0, y_0, t_0], ... [x_n, y_n, t_n]] from interpolated nodes dictionary
    :return: tesnor [[x_0, y_0, t_0], ... [x_n, y_n, t_n]], containing all manipulatable nodes for a given leg
    """
    nodes = np.asarray(leg_points)
    points = np.asarray(contact_points_relevant)
    X_n = torch.from_numpy(nodes)
    X_o = torch.from_numpy(points)
    return X_n, X_o


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


def update_nodes(node_vector, delta_val_vector, sim_point_ends, v_limit):
    d_vector = find_distance_components(node_vector, sim_point_ends)
    delta_val_vector = np.reshape(delta_val_vector, (-1, 1))
    change_vector = np.multiply(d_vector, delta_val_vector)
    # NOTE: insert velocity limiter here
    change_vector = velocity_saturate(node_vector, change_vector, v_limit)
    new_node_vector = np.round(np.add(node_vector, change_vector), 2)
    return new_node_vector


def velocity_saturate(node_vector, change_vector, v_limit):
    v_min = v_limit[0]
    v_max = v_limit[1]
    if v_max <= v_min:
        print('WARNING: velocity limits are not appropriate, switching v_min and v_max...')
        v_min, v_max = v_max, v_min
    diffs = np.subtract(
        node_vector[1:, 0:2], node_vector[0:-1, 0:2])

    travelled = np.reshape(np.linalg.norm(diffs, axis=1), (-1, 1))
    time_steps = np.reshape(np.subtract(
        node_vector[1:, 2], node_vector[0:-1, 2]), (-1, 1))

    velocities = np.divide(travelled, time_steps)
    # print('\n\nOLD VEL:')
    # print(velocities)
    num_points = time_steps.shape[0]
    # print(num_points)

    return change_vector
