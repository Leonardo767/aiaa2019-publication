import torch
import numpy as np


def create_dist_vectors(X_n, anchor_point):
    dist_vectors = []
    for node in X_n:
        dist_vectors.append((node, anchor_point))
    return dist_vectors


def generate_alteration_vectors(X_n, d_vect_input):
    # convert to torch
    X_n = torch.from_numpy(np.asarray(X_n))
    d_data = d_vect_input[0]
    d_vect_convert = [d_data[1][0] - d_data[0][0],
                      d_data[1][1] - d_data[0][1],
                      d_data[1][2] - d_data[0][2]]
    d_vect = torch.from_numpy(np.asarray(d_vect_convert))
    print(d_vect)
    # dummy vals
    beta = 1
    sigma = 1
    mu = 14
    # calc
    j = X_n.size()[0]
    j_vector = torch.linspace(0, j - 1, j, dtype=torch.float64).view(-1, 1)
    delta = generate_delta_distribution(j_vector, beta, sigma, mu)
    plane = create_plane(d_vect, X_n)
    new_X_n = X_n + delta*plane[1]
    return new_X_n.tolist()


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


def generate_delta_distribution(j_vector, beta, sigma, mu):
    scaling_factor = beta/(2 * 3.14159 * sigma**2)**0.5
    exp_factor = -(j_vector - mu)**2/(2*sigma**2)
    X_n_delta = scaling_factor*torch.exp(exp_factor)
    return X_n_delta
