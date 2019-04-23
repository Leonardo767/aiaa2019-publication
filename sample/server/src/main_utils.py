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


def velocity_saturate(proposed_node_vector, leg_time, v_limit):
    v_min = v_limit[0]
    v_max = v_limit[1]
    diffs = np.subtract(
        proposed_node_vector[1:-1, 0:2], proposed_node_vector[0:-2, 0:2])
    travelled = np.reshape(np.linalg.norm(diffs, axis=1), (-1, 1))
    time_steps = np.reshape(np.subtract(
        proposed_node_vector[1:-1, 2], proposed_node_vector[0:-2, 2]), (-1, 1))
    # v_min produces maximum allowable time for diff
    time_upper_bound = np.divide(travelled, v_min)
    # v_max produces minimum allowable time for diff
    time_lower_bound = np.divide(travelled, v_max)
    # print(time_upper_bound)
    # print(time_lower_bound)
    num_points = time_steps.shape[0]
    for i in range(num_points):
        if time_lower_bound[i, :] > time_steps[i, :]:
            proposed_node_vector[i + 1, 2] = proposed_node_vector[i,
                                                                  2] + time_lower_bound[i, :]
        elif time_upper_bound[i, :] < time_steps[i, :]:
            proposed_node_vector[i + 1, 2] = proposed_node_vector[i,
                                                                  2] + time_upper_bound[i, :]
    new_time_steps = np.reshape(np.subtract(
        proposed_node_vector[1:-1, 2], proposed_node_vector[0:-2, 2]), (-1, 1))

    velocities = np.divide(travelled, time_steps)
    new_velocities = np.divide(travelled, new_time_steps)
    print(velocities)
    print(new_velocities)
    return proposed_node_vector
