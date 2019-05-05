import torch
import numpy as np
from server.src.optimization.feed_forward_utils import (
    find_distance, compute_delta_vector, update_nodes,
    compute_c_deviation, compute_c_internode, compute_c_contact)


def init_params(j_max, seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    # only positive beta allowed
    beta_params = torch.abs(torch.randn(
        5, requires_grad=True, dtype=torch.float64))
    # only positive sigma allowed
    sigma_params = torch.abs(torch.randn(
        4, requires_grad=True, dtype=torch.float64))
    # sigma_j must be scaled to j size
    sigma_j = torch.abs(torch.randn(
        1, requires_grad=True, dtype=torch.float64)) * j_max
    sigma_params = torch.cat((sigma_params, sigma_j))
    mu_params = torch.randn(3, requires_grad=True, dtype=torch.float64)
    # will scale each nodes individual delta as delta_j^((scale_bias)_j)
    scale_bias = torch.abs(torch.randn(
        j_max, requires_grad=True, dtype=torch.float64)) + 1
    max_val = torch.max(scale_bias)
    scale_bias = scale_bias / max_val
    # eta = torch.randn((j_max, 3), requires_grad=True, dtype=torch.float64) / 50
    # print(eta)
    param_dict = {
        'beta': beta_params,
        'sigma': sigma_params,
        'mu': mu_params,
        'bias': scale_bias
        # 'eta': eta
    }
    return param_dict


def iterate_nodes(X_n, X_o, param_dict):
    X_n.requires_grad_(True)
    d_s, d_e = find_distance(X_n, X_o)
    # delta = compute_delta_vector(
    #     X_n, X_o, d_s, d_e, param_dict)
    delta = 0
    # eta = param_dict['eta']
    # X_n1 = update_nodes(X_n, d_s, d_e, delta)
    X_n1 = X_n
    return X_n1, X_o, X_n


def determine_cost(X_n1, X_o, X_n0, leg_time):
    C_deviation = compute_c_deviation(X_n1, X_n0)
    C_internode = compute_c_internode(X_n1)
    C_contact = compute_c_contact(X_n1, X_o, X_n0, leg_time)
    lambda_weights = torch.from_numpy(np.array([1., 10., 100.])).view(-1, 1)
    cost_components = torch.cat((C_deviation, C_internode, C_contact), 1)
    cost = torch.mm(cost_components, lambda_weights)
    return cost, cost_components
