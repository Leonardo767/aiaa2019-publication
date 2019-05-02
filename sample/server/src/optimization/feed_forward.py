import torch
import numpy as np
from server.src.optimization.feed_forward_utils import (
    find_distance, compute_delta_vector, update_nodes,
    compute_c_deviation, compute_c_internode, compute_c_contact)


def init_params(j_max, seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    # only positive beta allowed
    beta_params = torch.abs(torch.randn(5, requires_grad=True))
    # only positive sigma allowed
    sigma_params = torch.abs(torch.randn(5, requires_grad=True))
    # sigma_j must be scaled to j size
    sigma_params[4] *= j_max
    mu_params = torch.randn(3, requires_grad=True)
    # will scale each nodes individual delta as delta_j^((scale_bias)_j)
    scale_bias = torch.abs(torch.randn(j_max, requires_grad=True).double()) + 1
    max_val = torch.max(scale_bias)
    scale_bias /= max_val
    param_dict = {
        'beta': beta_params,
        'sigma': sigma_params,
        'mu': mu_params,
        'bias': scale_bias
    }
    return param_dict


def iterate_nodes(X_n, X_o, param_dict):
    d_s, d_e = find_distance(X_n, X_o)
    delta = compute_delta_vector(
        X_n, X_o, d_s, d_e, param_dict)
    X_n1 = update_nodes(X_n, d_s, d_e, delta)
    return X_n1, X_o


def determine_cost(X_n1, X_o, X_n0, leg_time):
    C_deviation = compute_c_deviation(X_n1, X_n0)
    C_internode = compute_c_internode(X_n1)
    C_contact = compute_c_contact(X_n1, X_o, leg_time)
    lambda_weights = torch.from_numpy(np.array([1., 1., 1.])).view(-1, 1)
    cost_components = torch.cat((C_deviation, C_internode, C_contact), 1)
    print(cost_components)
    cost = torch.mm(cost_components, lambda_weights)
    print(cost)
    return cost
