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
    # print('\n\n\n\n\n\n')
    # print('\n\nd_comp size:', d_components.size())
    # print('d_comp:', d_components)
    # using cos(theta) = dot(u,v)/(norm(u)*norm(v)):
    # ---------------------------------------------------------
    # consistent direction to introduce asymmetry
    sim_vector = (X_o[-1, :] - X_o[0, :])
    sim_vector = sim_vector.repeat(d_components.size()[0], 1)
    # print('\n\nsim vect size:', sim_vector.size())
    # print('sim vect:', sim_vector)

    # compute dot product
    dot_prod = torch.bmm(d_components.view(
        20, 1, 3), sim_vector.view(20, 3, 1))
    dot_prod = dot_prod.view(-1, 1)
    # print('\n\ndot size:', dot_prod.size())
    # print('dot:', dot_prod)

    # compute mag denom
    sim_mag = torch.norm(sim_vector)
    mag_denom = torch.norm(d_components, dim=1) * sim_mag
    mag_denom = mag_denom.view(-1, 1)
    # print('\n\nmag size:', mag_denom.size())
    # print('mag:', mag_denom)

    # compute theta
    cos_theta_s = dot_prod / mag_denom
    theta = torch.acos(cos_theta_s)
    # print('\n\ntheta size:', theta.size())
    # print('theta:', np.degrees(theta))
    return theta


def find_delta_d_s(d_s, beta_params, sigma_params, mu_params):
    beta = beta_params[0]
    sigma = sigma_params[0]
    mu = mu_params[0]
    d_mag = torch.norm(d_s, dim=1)
    d_mag = d_mag.view(-1, 1)
    scaling_factor = 1/(2*np.pi*sigma**2)**0.5
    exp_factor = -beta*(d_mag - mu)**2/(2*sigma**2)
    delta_d_s = scaling_factor*torch.exp(exp_factor)
    max_val = torch.max(delta_d_s)
    delta_d_s /= max_val
    # print('s:', delta_d_s)
    return delta_d_s


def find_delta_d_e(d_e, beta_params, sigma_params, mu_params):
    beta = beta_params[1]
    sigma = sigma_params[1]
    mu = mu_params[0]
    d_mag = torch.norm(d_e, dim=1)
    d_mag = d_mag.view(-1, 1)
    scaling_factor = 1/(2*np.pi*sigma**2)**0.5
    exp_factor = -beta*(d_mag - mu)**2/(2*sigma**2)
    delta_d_e = scaling_factor*torch.exp(exp_factor)
    max_val = torch.max(delta_d_e)
    delta_d_e /= max_val
    # print('e:', delta_d_e)
    return delta_d_e


def find_delta_theta_s(X_n, X_o, d_s, beta_params, sigma_params, mu_params):
    theta = find_theta(X_n, X_o, X_o[0, :], d_s)
    beta = beta_params[2]
    sigma = sigma_params[2]
    mu = mu_params[1]
    scaling_factor = 1/(2*np.pi*sigma**2)**0.5
    exp_factor = -beta*(theta - mu)**2/(2*sigma**2)
    delta_theta_s = scaling_factor*torch.exp(exp_factor)
    max_val = torch.max(delta_theta_s)
    delta_theta_s /= max_val
    # print('s:', delta_theta_s)
    return delta_theta_s


def find_delta_theta_e(X_n, X_o, d_e, beta_params, sigma_params, mu_params):
    theta = find_theta(X_n, X_o, X_o[-1, :], d_e)
    beta = beta_params[3]
    sigma = sigma_params[3]
    mu = mu_params[1]
    scaling_factor = 1/(2*np.pi*sigma**2)**0.5
    exp_factor = -beta*(theta - mu)**2/(2*sigma**2)
    delta_theta_e = scaling_factor*torch.exp(exp_factor)
    max_val = torch.max(delta_theta_e)
    delta_theta_e /= max_val
    # print('e:', delta_theta_e)
    return delta_theta_e


def find_delta_j(X_n, X_o, beta_params, sigma_params, mu_params):
    j = torch.Tensor([[float(i)]
                      for i in range(X_n.size()[0])]).double()
    beta = beta_params[4]
    sigma = sigma_params[4]
    mu = mu_params[2]
    scaling_factor = 1/(2*np.pi*sigma**2)**0.5
    exp_factor = -beta*(j - mu)**2/(2*sigma**2)
    delta_j = scaling_factor*torch.exp(exp_factor)
    # print(delta_j)
    return delta_j


def compute_delta_vector(X_n, X_o, d_s, d_e, beta_params, sigma_params, mu_params, scale_bias):
    delta_d_s = find_delta_d_s(d_s, beta_params, sigma_params, mu_params)
    delta_d_e = find_delta_d_e(d_e, beta_params, sigma_params, mu_params)
    delta_theta_s = find_delta_theta_s(
        X_n, X_o, d_s, beta_params, sigma_params, mu_params)
    delta_theta_e = find_delta_theta_e(
        X_n, X_o, d_e, beta_params, sigma_params, mu_params)
    delta_j = find_delta_j(X_n, X_o, beta_params, sigma_params, mu_params)
    delta = torch.cat(
        (delta_d_s, delta_d_e, delta_theta_s, delta_theta_e, delta_j), dim=1)
    # print('\ndelta raw:', delta)
    delta = torch.prod(delta, dim=1)  # Hadamard product
    # print('\ndelta Hadamard prod:', delta)
    delta = torch.pow(delta, scale_bias)
    # print('\ndelta scaled:', delta)
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
    [3,	    1,	10.5]])

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
beta_params = torch.abs(torch.randn(5))     # only positive beta allowed
sigma_params = torch.abs(torch.randn(5))    # only positive sigma allowed
sigma_params[4] *= X_n.size()[0]            # sigma_j must be scaled to j size
mu_params = torch.randn(3)
# will scale each nodes individual delta as delta_j^((scale_bias)_j)
scale_bias = torch.abs(torch.randn(X_n.size()[0]).double()) + 1
max_val = torch.max(scale_bias)
scale_bias /= max_val
print('\nPARAMS:')
print(beta_params)
print(sigma_params)
print(mu_params)
print(scale_bias)
print('\n\n\n')

delta = compute_delta_vector(
    X_n, X_o, d_s, d_e, beta_params, sigma_params, mu_params, scale_bias)
# print(delta)
