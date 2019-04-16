from datetime import timedelta


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


def create_interpolated_nodes(flights, nodes_per_leg=20, clean=True):
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
            nodes_for_flight[prev_point[2].total_seconds() /
                             3600] = nodes_for_leg
        nodes_dict[flight_number] = nodes_for_flight
    if clean:
        return remove_stationary_legs(nodes_dict)
    return nodes_dict


def remove_stationary_legs(created_nodes):
    # remove created nodes for which the drone is in port
    for _, legs in created_nodes.items():
        to_delete = []
        for leg_time, points in legs.items():
            if (points[0][0], points[0][1]) == (points[-1][0], points[-1][1]):
                to_delete.append(leg_time)
        for nonflight_leg_time in to_delete:
            del legs[nonflight_leg_time]
    return created_nodes


def find_contact_with_sim(points, created_nodes_sim, sight):
    contact_points = []
    return contact_points


def find_contact(created_nodes, created_nodes_sim, sight=0.2):
    print(created_nodes)
    contact_points_dict = {}
    for flight_number, legs in created_nodes.items():
        contact_points_dict[flight_number] = []
        for leg_time, points in legs.items():
            contact_points_dict[flight_number].append(
                find_contact_with_sim(points, created_nodes_sim, sight=sight))
    return 0
