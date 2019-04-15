from datetime import timedelta
from numpy import asarray
from numpy.linalg import norm


def append_endpoints(path_dict_list, geo_info):
    timespan = geo_info["timespan"]
    for path_dict in path_dict_list:
        for name, flight_endpoints in path_dict.items():
            start_point = [
                [flight_endpoints[0][0], flight_endpoints[0][1], timedelta(seconds=0)]]
            finish_point = [[flight_endpoints[-1][0],
                             flight_endpoints[-1][1], timespan]]
            path_dict[name] = start_point + flight_endpoints + finish_point
    return path_dict_list[0], path_dict_list[1]


def create_interpolated_nodes(flights, nodes_per_leg=20):
    nodes_dict = {}
    for flight_number, flight_endpoints in flights.items():
        nodes_for_flight = {}
        for i in range(1, len(flight_endpoints)):
            prev_point = flight_endpoints[i - 1]
            next_point = flight_endpoints[i]
            diff_vector = [next_point[0] - prev_point[0], next_point[1] - prev_point[1],
                           next_point[2].total_seconds()/3600 - prev_point[2].total_seconds()/3600]
            nodes_for_leg = []
            for j in range(1, nodes_per_leg + 1):
                current_step_size = j/nodes_per_leg
                nodes_for_leg.append(
                    [prev_point[0] + current_step_size*diff_vector[0],
                     prev_point[1] + current_step_size*diff_vector[1],
                     prev_point[2].total_seconds()/3600 + current_step_size*diff_vector[2]])
            nodes_for_flight[next_point[2].total_seconds() /
                             3600] = nodes_for_leg
        nodes_dict[flight_number] = nodes_for_flight
    return nodes_dict
