import torch
import numpy as np


def find_grads(cost, param_dict):
    beta, sigma, mu, scale_bias = param_dict.values()
    beta.retain_grad()
    sigma.retain_grad()
    mu.retain_grad()
    scale_bias.retain_grad()
    cost.mean().backward()
    # print('\nGRAD:', sigma.grad)
    grad_dict = {
        'dC_dbeta': beta.grad,
        'dC_dsigma': sigma.grad,
        'dC_dmu': mu.grad,
        'dC_dbias': scale_bias.grad
    }
    return grad_dict


def update_params(param_dict, grad_dict, alpha):
    new_beta = param_dict['beta'] - alpha * grad_dict['dC_dbeta']
    new_sigma = param_dict['sigma'] - alpha * grad_dict['dC_dsigma']
    new_mu = param_dict['mu'] - alpha * grad_dict['dC_dmu']
    new_scale_bias = param_dict['bias'] - alpha * grad_dict['dC_dbias']
    updated_param_dict = {
        'beta': new_beta,
        'sigma': new_sigma,
        'mu': new_mu,
        'bias': new_scale_bias
    }
    return updated_param_dict
