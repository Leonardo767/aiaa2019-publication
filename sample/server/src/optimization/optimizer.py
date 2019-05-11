import torch
from server.src.optimization.feed_forward_utils import find_distance
from server.lib.data_wrangling.dataUtils import find_contact
from server.src.main_utils import tensorize_nodes
from server.src.optimization.optimizer_utils import (construct_input, find_new_contact, construct_output, create_plane,
                                                     find_plane_bias, generate_delta_distribution, mutate_param,
                                                     blend_deviations, find_percent_covered, is_valid_xn)


def mutate(plane_basis, X_n0, object_point, init=True, old_best=None, mutation_setting=None):
    j = X_n0.size()[0]
    # calculate parameters informing the mutation
    path_scale_length = j
    diffs = torch.norm(X_n0 - object_point.repeat(j, 1), dim=1)
    min_dist, closest_point_idx = torch.min(diffs, 0)

    # use the heuristics found here to generate informed distribution parameters
    informed_beta = min_dist*16  # conservative deviation, about half of sight range
    # 1/16 of path affected within 1 z-score
    informed_sigma = path_scale_length/16
    informed_mu = closest_point_idx  # peaks at closest point to object
    if init or old_best is None:
        beta, sigma, mu = informed_beta, informed_sigma, informed_mu
    else:
        if old_best is None:
            print('Missing old best parameters.')
            return 0
        beta, sigma, mu = old_best
    # mutate the informed starting points
    batch = 8
    if mutation_setting is None:
        mutation_factor = 0.05
    else:
        mutation_factor = mutation_setting
    beta = mutate_param(beta, informed_beta, j, batch, mutation_factor)
    sigma = mutate_param(sigma, informed_sigma, j, batch, mutation_factor)
    mu = mutate_param(mu, informed_mu, j, batch, mutation_factor)
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
    # make sure our old best is considered in the competition
    if not init and old_best is not None:
        params.append(old_best)
    return X_n_mutations, params


def feed_forward(X_n0, X_o, init_feed=True, params_s=None, params_e=None, mutation_setting=0.05):
    timeout = 10
    need_valid_X_n = True
    while need_valid_X_n:
        d_s, d_e = construct_input(X_n0, X_o)
        # mutate s
        plane_s = create_plane(d_s[0], X_n0)
        if init_feed:
            X_n_mutations_s, params_s = mutate(plane_s, X_n0, X_o[0])
        else:
            X_n_mutations_s, params_s = mutate(
                plane_s, X_n0, X_o[0], init=False, old_best=params_s,
                mutation_setting=mutation_setting)
        # mutate e
        plane_e = create_plane(d_e[0], X_n0)
        if init_feed:
            X_n_mutations_e, params_e = mutate(plane_e, X_n0, X_o[-1])
        else:
            X_n_mutations_e, params_e = mutate(
                plane_e, X_n0, X_o[-1], init=False, old_best=params_e,
                mutation_setting=mutation_setting)
        # blend
        X_n = []
        plane_s_bias = find_plane_bias(d_s, d_e)
        for s_mutation, e_mutation in zip(X_n_mutations_s, X_n_mutations_e):
            new_X_n = blend_deviations(s_mutation, e_mutation, plane_s_bias)
            # print(is_valid_xn(new_X_n, X_n0))
            if is_valid_xn(new_X_n, X_n0):
                X_n.append(new_X_n)
        # handle validity
        if not(len(X_n)) and timeout < 100:
            print('No valid mutations. Retrying with more conservative mutations...\n')
            timeout += 1
            mutation_setting *= 0.8  # let's be more conservative next time
        elif not timeout < 100:
            print('Tried to mutate too many times. Sticking with current path.')
            print('Try modifying your initial path to be more amicable to mutation.')
            need_valid_X_n = True
        else:
            need_valid_X_n = False
    return X_n, params_s, params_e


def determine_best(X_n_list, params_s, params_e, flight_number, leg_time, created_nodes_sim, sight, flight_time, old_performance=0):
    performance = []
    X_o_trials = []
    for trial in X_n_list:
        # define a valid timestep of continuity by the Nyquist criterion
        valid_timestep = (trial[1, 2] - trial[0, 2]).item()/2
        X_o = find_new_contact(trial, flight_number,
                               leg_time, created_nodes_sim, sight)
        performance.append(find_percent_covered(
            X_o, flight_time, valid_timestep))
        X_o_trials.append(X_o)
    # print('\n\n\nGENERATION BATCH:')
    # select the best-performing
    best_idx = performance.index(max(performance))
    best_performance = performance[best_idx]
    X_n_opt = X_n_list[best_idx]
    X_o_opt = X_o_trials[best_idx]
    param_best_s = params_s[best_idx]
    param_best_e = params_e[best_idx]
    # print(params_s)
    # print(params_e)
    if old_performance == best_performance:
        improvement = False
        print('Did not improve. Increasing mutation rate next iteration...')
    else:
        improvement = True
    return X_n_opt, X_o_opt, param_best_s, param_best_e, improvement, best_performance


def main_opt(X_n, X_o, flight_number, leg_time, created_nodes_sim, sight, iter_val):
    """
    :param X_n: tensor [[x_0, y_0, t_0], ..., [x_j, y_j, t_j]], containing all manipulable nodes for a given leg
    :param X_o: tensor [[x_s, y_s, t_s], ..., [x_e, y_e, t_e]] points of sim contact
    :return X_n_opt: optimized X_n
    :return X_o_opt: X_o using X_n_opt
    """
    torch.manual_seed(0)
    X_n0 = X_n
    flight_time = (X_n0[-1][2] - leg_time).item()
    # test mutated flight paths in batch
    X_n_list, params_s, params_e = feed_forward(X_n0, X_o)
    # test mutated flight paths in batch
    mutation_setting = 0.05
    # return X_n, find_new_contact(X_n, flight_number, leg_time, created_nodes_sim, sight)
    param_hist = [[], [], [], [], [], [], [], [], X_n.tolist(), []]
    best_performance = 0
    for i in range(iter_val):
        # print(best_performance)
        X_n_opt, X_o_opt, param_best_s, param_best_e, improvement, best_performance = determine_best(
            X_n_list, params_s, params_e, flight_number, leg_time,
            created_nodes_sim, sight, flight_time, old_performance=best_performance)
        X_n, X_o = X_n_opt, X_o_opt
        # print(params_s)
        # print(params_e)
        # print('mutation:', mutation_setting)
        # print('\nBEST:')
        # print(X_o_opt.size()[0])
        # print(param_best_s)
        # print(param_best_e)
        param_hist[0].append(param_best_s[0])  # beta_s
        param_hist[1].append(param_best_s[1])  # sigma_s
        param_hist[2].append(param_best_s[2])  # mu_s
        param_hist[3].append(param_best_e[0])  # beta_e
        param_hist[4].append(param_best_e[1])  # sigma_e
        param_hist[5].append(param_best_e[2])  # mu_e
        param_hist[6].append(mutation_setting)  # eta
        param_hist[7].append(X_o_opt.size()[0])  # max(len(X_o))
        param_hist[9].append(best_performance)  # performance
        if not improvement and mutation_setting < 0.1:
            mutation_setting *= 2
        else:
            mutation_setting = max(0.01, mutation_setting * 0.8)
        X_n_list, params_s, params_e = feed_forward(
            X_n0, X_o, init_feed=False, params_s=param_best_s,
            params_e=param_best_e, mutation_setting=mutation_setting)
        print('Optimizing LEG {} OF FLIGHT {} ({}% Completed)'.format(
            leg_time, flight_number, 100*(i + 1)/iter_val))
    print('Packing optimized results for LEG {} OF FLIGHT {}...'.format(
        leg_time, flight_number))
    print()
    # print(param_hist)
    return X_n_opt, X_o_opt, param_hist
