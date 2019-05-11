import torch
from server.src.optimization.feed_forward_utils import find_distance
from server.lib.data_wrangling.dataUtils import find_contact
from server.src.main_utils import tensorize_nodes


def construct_input(X_n, X_o):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_in: concatnated tensor of input neurons (d_s, d_e)
    """
    d_s, d_e = find_distance(X_n, X_o)
    return d_s, d_e


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


def create_plane(d_vector, X_n):
    # takes a basis in 3-D space and outputs orthonormal basis in 2-D plane
    # uses the Gram-Schmidt process
    x_vect = X_n[1] - X_n[0]
    u1 = x_vect / torch.norm(x_vect)
    y2 = d_vector - torch.dot(d_vector, u1) * u1
    u2 = y2 / torch.norm(y2)
    # print(u1)
    # print(u2)
    # print()
    return (u1, u2)


def find_plane_bias(d_s, d_e, ref='s'):
    # determines bias for point s
    strength_s = torch.norm(d_s)
    strength_e = torch.norm(d_e)
    total = strength_s + strength_e
    s_bias = strength_e / total   # the larger d_e is, the more we skew to s
    e_bias = strength_s / total
    if ref == 's':
        plane_bias = s_bias
    else:
        plane_bias = e_bias
    return plane_bias


def generate_delta_distribution(j_vector, beta, sigma, mu):
    scaling_factor = beta/(2 * 3.14159 * sigma**2)**0.5
    exp_factor = -(j_vector - mu)**2/(2*sigma**2)
    X_n_delta = scaling_factor*torch.exp(exp_factor)
    return X_n_delta


def mutate_param(param, informed_param, j, batch_size, mutation_factor):
    param = param * (1 + torch.randn(batch_size - 1, dtype=torch.float64) *
                     mutation_factor).repeat(j, 1)
    param_oddball = informed_param * (1 + torch.randn(1, dtype=torch.float64) *
                                      mutation_factor).repeat(j, 1)
    mutated_param_matrix = torch.cat((param, param_oddball), dim=1)
    return mutated_param_matrix


def blend_deviations(X_n_s, X_n_e, s_bias):
    X_n = s_bias * X_n_s + (1 - s_bias) * X_n_e
    return X_n


def find_percent_covered(X_o, flight_time, valid_timestep):
    # time_covered = X_o[-1, 2] - X_o[0, 2]
    timestamps = X_o[:, 2].tolist()
    time_covered = 0
    for i in range(len(timestamps) - 1):
        if timestamps[i + 1] - timestamps[i] < valid_timestep:
            time_covered += timestamps[i + 1] - timestamps[i]
    # print(time_covered)
    percent_covered = time_covered/flight_time
    return percent_covered
