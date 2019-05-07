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


def mutate(plane_basis, X_n0, object_point, init=True, old_best=None):
    j = X_n0.size()[0]
    if init or old_best is None:
        # calculate parameters informing the mutation
        path_scale_length = j
        diffs = torch.norm(X_n0 - object_point.repeat(j, 1), dim=1)
        min_dist, closest_point_idx = torch.min(diffs, 0)

        # use the heuristics found here to generate informed distribution parameters
        informed_beta = min_dist/2  # conservative deviation, about half of sight range
        # 1/16 of path affected within 1 z-score
        informed_sigma = path_scale_length//16
        informed_mu = closest_point_idx  # peaks at closest point to object
        beta, sigma, mu = informed_beta, informed_sigma, informed_mu
    else:
        if old_best is None:
            print('Missing old best parameters.')
            return 0
        beta, sigma, mu = old_best

    # mutate the informed starting points
    torch.manual_seed(0)
    batch = 5
    mutation_factor = 0.05
    beta = beta * (1 + torch.randn(batch, dtype=torch.float64) *
                   mutation_factor).repeat(j, 1)
    sigma = sigma * (1 + torch.randn(batch, dtype=torch.float64) *
                     mutation_factor).repeat(j, 1)
    mu = mu * (1 + torch.randn(batch, dtype=torch.float64) *
               mutation_factor).repeat(j, 1)

    # calculate deviation distribution from parameters
    j_vector = torch.linspace(0, j - 1, j, dtype=torch.float64).view(-1, 1)
    # j_vector = j_vector.repeat(1, batch)
    X_n_delta = generate_delta_distribution(
        j_vector, beta, sigma, mu).transpose(0, 1).view(batch, j, 1)
    orthogonal_vect = plane_basis[1].view(1, 1, 3).repeat(batch, j, 1)
    # print(orthogonal_vect)
    # print(X_n_delta)
    X_n_delta = orthogonal_vect * X_n_delta
    X_n_mutations = list(torch.split(X_n0.view(-1, 3) + X_n_delta, 1, dim=0))
    for i in range(len(X_n_mutations)):
        X_n_mutations[i] = torch.squeeze(X_n_mutations[i])
    params = []
    for i in range(batch):
        beta_val = round(beta[0][i].item(), 5)
        sigma_val = round(sigma[0][i].item(), 5)
        mu_val = round(mu[0][i].item(), 5)
        params.append((beta_val, sigma_val, mu_val))
    if not init and old_best is not None:
        params.append(old_best)
    return X_n_mutations, params


def blend_deviations(X_n_s, X_n_e, s_bias):
    X_n = s_bias * X_n_s + (1 - s_bias) * X_n_e
    return X_n


def feed_forward(X_n0, X_o, init_feed=True, params_s=None, params_e=None):
    d_s, d_e = construct_input(X_n0, X_o)
    # mutate s
    plane_s = create_plane(d_s[0], X_n0)
    if init_feed:
        X_n_mutations_s, params_s = mutate(plane_s, X_n0, X_o[0])
    else:
        X_n_mutations_s, params_s = mutate(
            plane_s, X_n0, X_o[0], init=False, old_best=params_s)
    # mutate e
    plane_e = create_plane(d_e[0], X_n0)
    if init_feed:
        X_n_mutations_e, params_e = mutate(plane_e, X_n0, X_o[-1])
    else:
        X_n_mutations_e, params_e = mutate(
            plane_e, X_n0, X_o[-1], init=False, old_best=params_e)
    # blend
    X_n = []
    plane_s_bias = find_plane_bias(d_s, d_e)
    for s_mutation, e_mutation in zip(X_n_mutations_s, X_n_mutations_e):
        X_n.append(blend_deviations(s_mutation, e_mutation, plane_s_bias))
    return X_n, params_s, params_e


def determine_best(X_n_list, params_s, params_e, flight_number, leg_time, created_nodes_sim, sight):
    X_o_results = []
    X_o_sizes = []
    for trial in X_n_list:
        X_o = find_new_contact(trial, flight_number,
                               leg_time, created_nodes_sim, sight)
        X_o_results.append(X_o)
        X_o_sizes.append(X_o.size()[0])
        print(X_o.size()[0])
    # select the best-performing
    best_idx = X_o_sizes.index(max(X_o_sizes))
    X_n_opt = X_n_list[best_idx]
    X_o_opt = X_o_results[best_idx]
    param_best_s = params_s[best_idx]
    param_best_e = params_e[best_idx]
    print(params_s)
    print(params_e)
    return X_n_opt, X_o_opt, param_best_s, param_best_e


def main_opt(X_n, X_o, flight_number, leg_time, created_nodes_sim, sight, iter_val):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_n_opt: optimized X_n
    :return X_o_opt: X_o using X_n_opt
    """
    X_n0 = X_n
    flight_time = X_n0[-1][2] - leg_time
    # test mutated flight paths in batch
    X_n_list, params_s, params_e = feed_forward(X_n0, X_o)
    # test mutated flight paths in batch
    for i in range(iter_val):
        X_n_opt, X_o_opt, param_best_s, param_best_e = determine_best(
            X_n_list, params_s, params_e, flight_number, leg_time,
            created_nodes_sim, sight)
        X_n, X_o = X_n_opt, X_o_opt
        X_n_list, params_s, params_e = feed_forward(
            X_n0, X_o, init_feed=False, params_s=param_best_s, params_e=param_best_e)
    return X_n_opt, X_o_opt
