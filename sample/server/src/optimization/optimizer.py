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
    scaling_factor = 1/(2 * 3.14159 * sigma**2)**0.5
    exp_factor = -beta*(j_vector - mu)**2/(2*sigma**2)
    X_n_delta = scaling_factor*torch.exp(exp_factor)
    return X_n_delta


def mutate(plane_basis, X_n, object_point, negate=False):
    # calculate parameters informing the mutation
    path_scale_length = X_n.size()[0]
    diffs = torch.norm(X_n - object_point.repeat(X_n.size()[0], 1), dim=1)
    min_dist, closest_point_idx = torch.min(diffs, 0)

    # use the heuristics found here to generate informed distribution parameters
    informed_beta = min_dist/2  # conservative deviation, about half of sight range
    # 1/16 of path affected within 1 z-score
    informed_sigma = path_scale_length//16
    informed_mu = closest_point_idx  # peaks at closest point to object

    # mutate the informed starting points

    # calculate deviation distirbution from parameters
    j_vector = torch.linspace(0, X_n.size()[0], X_n.size()[
        0], dtype=torch.float64).view(-1, 1)
    X_n_delta = generate_delta_distribution(
        j_vector, informed_beta, informed_sigma, informed_mu)
    if negate:
        X_n_delta = -X_n_delta
    X_n_mutation = X_n + X_n_delta
    return X_n_mutation


def blend_deviations(X_n_s, X_n_e, s_bias):
    X_n = s_bias * X_n_s + (1 - s_bias) * X_n_e
    return X_n


def main_opt(X_n, X_o, flight_number, leg_time, created_nodes_sim, sight, iter_val):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_n_opt: optimized X_n
    :return X_o_opt: X_o using X_n_opt
    """
    X_n0 = X_n
    flight_time = X_n0[-1][2] - leg_time
    d_s, d_e = construct_input(X_n, X_o)
    # mutate s
    plane_s = create_plane(d_s[0], X_n)
    X_n_mutation_s = mutate(plane_s, X_n, X_o[0])
    # mutate e
    plane_e = create_plane(d_e[0], X_n)
    X_n_mutation_e = mutate(plane_e, X_n, X_o[-1], negate=True)
    # blend
    plane_s_bias = find_plane_bias(d_s, d_e)
    X_n = blend_deviations(X_n_mutation_s, X_n_mutation_e, plane_s_bias)
    X_n_opt, X_o_opt = X_n, find_new_contact(
        X_n, flight_number, leg_time, created_nodes_sim, sight)
    return X_n_opt, X_o_opt
