import numpy as np


def find_delta_per_d(d, beta_d):
    delta_per_d = 0
    return delta_per_d


def find_delta_per_theta(theta, beta_theta):
    delta_per_theta = 0
    return delta_per_theta


def find_delta_per_n(n, beta_n):
    delta_per_n = 0
    return delta_per_n


def find_delta(d, theta, n, beta_params):
    # beta_params = [beta_d, beta_theta, beta_n]
    beta_d, beta_theta, beta_n = beta_params
    delta = sum([find_delta_per_d(
        d, beta_d), find_delta_per_theta(theta, beta_theta), find_delta_per_n(n, beta_n)])
    return delta
