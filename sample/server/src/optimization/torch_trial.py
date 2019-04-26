import torch
import numpy as np


def find_distance(X_n, X_o):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return d_s: distance vector to first object, same dim=0 length as node vector
    :return d_e: distance vector to last object, same dim=0 length as node vector
    """
    d_s = X_o[0, :] - X_n
    d_e = X_o[-1, :] - X_n
    return d_s, d_e


def find_theta(X_n, X_o, X_o_point, d_components):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulatable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :param X_o_point: tensor [x_s, y_s, t_s], represents intersection loc for which we must find theta
    :return: theta vector, same length as node vector, except a vector of [theta] scalars rather than [x, y, t] vectors
    """
    # using cos(theta) = dot(u,v)/(norm(u)*norm(v))...
    # consistent direction to introduce asymmetry
    sim_vector = (X_o[-1, :] - X_o[0, :])
    print(sim_vector)
    sim_vector = sim_vector.repeat(d_components.size()[0], 1)
    print(sim_vector)
    # print(d_components)
    # print(sim_vector.size())
    sim_mag = torch.norm(sim_vector)

    mag_product = torch.norm(d_components, dim=1) * sim_mag
    cos_theta_s = torch.dot(d_components, sim_vector) / mag_product
    theta = torch.acos(cos_theta_s)
    print(theta)
    return theta


def find_delta_d_s(d_vect, beta_params, sigma_params):

    delta_d_s = 0
    return delta_d_s


def find_delta_d_e(d_vect, beta_params, sigma_params):

    delta_d_e = 0
    return delta_d_e


def find_delta_theta_s(X_n, X_o, d_s, beta_params, sigma_params):
    theta = find_theta(X_n, X_o, X_o[0, :], d_s)
    delta_theta_s = 0
    return delta_theta_s


def find_delta_theta_e(X_n, X_o, d_e, beta_params, sigma_params):
    theta = find_theta(X_n, X_o, X_o[-1, :], d_e)
    delta_theta_e = 0
    return delta_theta_e


def find_delta_n(X_n, X_o, beta_params, sigma_params):

    delta_n = 0
    return delta_n


def compute_delta_vector(X_n, X_o, d_s, d_e, beta_params, sigma_params):
    delta_d_s = find_delta_d_s(d_s, beta_params, sigma_params)
    delta_d_e = find_delta_d_e(d_e, beta_params, sigma_params)
    delta_theta_s = find_delta_theta_s(
        X_n, X_o, d_s, beta_params, sigma_params)
    delta_theta_e = find_delta_theta_e(
        X_n, X_o, d_e, beta_params, sigma_params)
    delta_n = find_delta_n(X_n, X_o, beta_params, sigma_params)
    delta = 0
    return delta


nodes = np.asarray([
    [1.1,	2.9,	8.12],
    [1.2,	2.8,	8.25],
    [1.31,	2.69,	8.39],
    [1.43,	2.57,	8.54],
    [1.56,	2.44,	8.7],
    [1.67,	2.33,	8.84],
    [1.75,	2.25,	8.94],
    [1.8,	2.2,	9],
    [1.86,	2.14,	9.07],
    [1.94,	2.06,	9.17],
    [2.05,	1.95,	9.31],
    [2.17,	1.83,	9.47],
    [2.29,	1.71,	9.61],
    [2.4,	1.6,	9.75],
    [2.5,	1.5,	9.88],
    [2.6,	1.4,	10],
    [2.7,	1.3,	10.12],
    [2.8,	1.2,	10.25],
    [2.9,	1.1,	10.38],
    [3,	1,	10.5]])

objects = np.asarray([
    [1.81,	2.14,	8.95],
    [1.805,	2.17,	8.975],
    [1.8,	2.2,	9],
    [1.795,	2.23,	9.025],
    [1.79,	2.26,	9.05]])


X_n = torch.from_numpy(nodes)
X_o = torch.from_numpy(objects)
# print('NODES:')
# print(X_n)
# print('\nOBJECTS:')
# print(X_o)
d_s, d_e = find_distance(X_n, X_o)
# print('\nd_s, d_e:')
# print(d_s)
# print(d_e)

torch.manual_seed(0)
beta_params = torch.randn(5)
sigma_params = torch.randn(5)
# print('\nPARAMS:')
# print(beta_params)
# print(sigma_params)

delta = compute_delta_vector(X_n, X_o, d_s, d_e, beta_params, sigma_params)
