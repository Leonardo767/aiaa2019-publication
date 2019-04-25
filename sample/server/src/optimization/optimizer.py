def main_opt(beta_params, metrics, results_flight_nodes):
    """
    :param beta_params: list [beta_d_s, beta_d_e, beta_theta_s, beta_theta_e, beta_n,
                        sigma_d_s, sigma_d_e, sigma_theta_s, sigma_theta_e, sigma_n]
    :param metrics: ({flight_no:{leg_time: cost_of_leg}}, total_cost)
    :param results_flight_nodes: {flight_no:{leg_time: new node points}}
    :return new_beta_params: new tuned beta params after grad descent
    """
    new_beta_params = 0
    return new_beta_params
