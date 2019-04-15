from datetime import timedelta


def append_endpoints(path_dict_list, geo_info):
    timespan = geo_info["timespan"]
    for path_dict in path_dict_list:
        for name, points_list in path_dict.items():
            start_point = [
                [points_list[0][0], points_list[0][1], timedelta(seconds=0)]]
            finish_point = [[points_list[-1][0], points_list[-1][1], timespan]]
            path_dict[name] = start_point + points_list + finish_point
    return path_dict_list[0], path_dict_list[1]
