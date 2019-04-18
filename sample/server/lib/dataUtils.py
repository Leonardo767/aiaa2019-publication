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


def drone_able_to_see(node, sim_point, sight):
    dist = ((node[0] - sim_point[0])**2 + (node[1] - sim_point[1])**2)**0.5
    if dist < sight:
        return True
    return False


def find_contact_for_one_node(node, sim_point_set, sight, timestep):
    contacted_points = []
    # name_of_sim_object = sim_point_set[0]
    sim_object_points = sim_point_set[1]
    for sim_point in sim_object_points:
        if abs(sim_point[2] - node[2]) < timestep/2:
            if drone_able_to_see(node, sim_point, sight):
                contacted_points.append(sim_point)
    return contacted_points


def find_contact_for_one_leg(flight_number, leg_time, paired_legs, node_points, sight):
    contact_points = []
    timestep = node_points[1][2] - node_points[0][2]
    sim_points_to_observe = paired_legs[(flight_number, leg_time)]
    for node in node_points:
        for sim_point_set in sim_points_to_observe:
            contact_points += find_contact_for_one_node(
                node, sim_point_set, sight, timestep)
    return contact_points


def find_contact(created_nodes, created_nodes_sim, sight=0.2):
    # pair legs of a flight with legs of a sim object
    paired_legs = {}
    for flight_number, legs in created_nodes.items():
        for leg_time, node_points in legs.items():
            paired_legs[(flight_number, leg_time)] = []
            leg_start_time = leg_time
            leg_end_time = node_points[-1][2]
            for sim_object, sim_object_legs in created_nodes_sim.items():
                for sim_leg_time, sim_leg_points in sim_object_legs.items():
                    sim_leg_start_time = sim_leg_time
                    sim_leg_end_time = sim_leg_points[-1][2]
                    if sim_leg_end_time > leg_start_time or sim_leg_start_time < leg_end_time:
                        paired_legs[(flight_number, leg_time)].append(
                            (sim_object, sim_leg_points))
    # find contact points
    contact_points_dict = {}
    for flight_number, legs in created_nodes.items():
        contact_points_dict[flight_number] = {}
        for leg_time, node_points in legs.items():
            contact_points_dict[flight_number][leg_time] = find_contact_for_one_leg(
                flight_number, leg_time, paired_legs, node_points, sight=sight)
    return contact_points_dict
