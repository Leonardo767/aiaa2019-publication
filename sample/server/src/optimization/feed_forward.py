import torch
import numpy as np


def init_params(j_max, seed=None):
    if seed is not None:
        torch.manual_seed(0)
    beta_params = torch.abs(torch.randn(5))     # only positive beta allowed
    sigma_params = torch.abs(torch.randn(5))    # only positive sigma allowed
    # sigma_j must be scaled to j size
    sigma_params[4] *= j_max
    mu_params = torch.randn(3)
    # will scale each nodes individual delta as delta_j^((scale_bias)_j)
    scale_bias = torch.abs(torch.randn(j_max).double()) + 1
    max_val = torch.max(scale_bias)
    scale_bias /= max_val
    param_dict = {
        'beta': beta_params,
        'sigma': sigma_params,
        'mu': mu_params,
        'bias': scale_bias
    }
    return param_dict


def iterate_nodes(nodes, points, param_dict):
    X_n = torch.from_numpy(nodes)
    X_o = torch.from_numpy(points)
    X_n1 = torch.from_numpy(nodes)
    return X_n1, X_o


def determine_cost(X_n1, X_o):
    cost = 0
    return cost
