from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.plotting import figure, show
from bokeh.util.compiler import TypeScript


def convert_to_timestring(time_in_sec):
    hours = int(time_in_sec//3600)
    minutes = int((time_in_sec % 3600)//60)
    seconds = int((minutes % 60)//60)
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    timestring = str(hours) + ':' + str(minutes) + ':' + str(seconds)
    # print(timestring)  # debugging
    return timestring


def plot_airports(plot, geo_info, airport_info):
    x_locs = []
    y_locs = []
    airport_labels = []
    # print(airport_info)  # debugging
    for airport_name, airport_data in airport_info.items():
        x_locs.append(airport_data[0][0])
        y_locs.append(airport_data[0][1])
        airport_labels.append(airport_name)
    source = ColumnDataSource(
        data=dict(x_locs=x_locs, y_locs=y_locs, airport_labels=airport_labels))
    airport_icon_size = 30
    plot.square(x='x_locs', y='y_locs', size=airport_icon_size,
                source=source, fill_alpha=0.3)
    labels = LabelSet(x='x_locs', y='y_locs', text='airport_labels', level='glyph',
                      x_offset=-5, y_offset=-10, source=source, render_mode='css')
    plot.add_layout(labels)
    return plot


def plot_sim(plot, sim_info, sim_style):
    x_locs = []  # list of list of x points
    y_locs = []  # list of list of y points
    t_labels = []  # list of list of timestamps
    object_names = []
    for sim_object_name, sim_points in sim_info.items():
        x_locs_object = []
        y_locs_object = []
        t_list = []
        for point in sim_points:
            x_locs_object.append(point[0])
            y_locs_object.append(point[1])
            t_list.append(point[2])
        x_locs.append(x_locs_object)
        y_locs.append(y_locs_object)
        t_labels.append(t_list)
        object_names.append(sim_object_name)
    plot.multi_line(x_locs, y_locs,
                    color="pink", alpha=0.9, line_width=4)
    # unpack x_locs and y_locs to create triangle endpoints
    x_loc_triangle = []
    y_loc_triangle = []
    t_triangle = []
    for x_object, y_object, t_object in zip(x_locs, y_locs, t_labels):
        for x, y, t in zip(x_object, y_object, t_object):
            x_loc_triangle.append(x)
            y_loc_triangle.append(y)
            t_triangle.append(t)
    plot.inverted_triangle(x_loc_triangle, y_loc_triangle, size=15,
                           color="pink", line_color="purple")
    # print(t_triangle)
    for i in range(len(t_triangle)):
        t_triangle[i] = convert_to_timestring(t_triangle[i].total_seconds())
    source = ColumnDataSource(
        data=dict(x_loc_triangle=x_loc_triangle, y_loc_triangle=y_loc_triangle, t_triangle=t_triangle))
    labels = LabelSet(x='x_loc_triangle', y='y_loc_triangle', text='t_triangle', level='glyph',
                      x_offset=0, y_offset=10, source=source, render_mode='css')
    plot.add_layout(labels)
    return plot


def plot_single_path(plot, flight_number, flight_endpoints):
    # NOTE: since this map is 2-dimensional, only the unique locations are used
    # This map is simply an overview before execution, showing the overall routes taken
    x_locs = []
    y_locs = []
    for endpoint in flight_endpoints:
        x_locs.append(endpoint[0])
        y_locs.append(endpoint[1])
    plot.line(x_locs, y_locs, color="grey", alpha=0.3, line_width=4)
    return plot


def plot_paths(plot, flights):
    for flight_number, flight_endpoints in flights.items():
        # print(flight_endpoints)
        plot_single_path(plot, flight_number, flight_endpoints)
    return plot


def plot_contact(plot, contact_points):
    x_locs = []
    y_locs = []
    for _, leg_times in contact_points.items():
        for _, points in leg_times.items():
            x_locs.append([point[0] for point in points])
            y_locs.append([point[1] for point in points])
    plot.multi_line(x_locs, y_locs, color="#630a0a", alpha=0.8, line_width=4)
    return plot


def plot_nodes(plot, created_nodes, contact_points):
    x_locs = []
    y_locs = []
    for flight_number, leg_times in created_nodes.items():
        for leg_time, points in leg_times.items():
            # only plot if the trajectory was altered
            if len(contact_points[flight_number][leg_time]):
                x_locs.append([point[0] for point in points])
                y_locs.append([point[1] for point in points])
    plot.multi_line(x_locs, y_locs, color="black", alpha=0.3, line_width=2)
    x_locs_flattened = []
    y_locs_flattened = []
    for x_list, y_list in zip(x_locs, y_locs):
        x_locs_flattened += x_list
        y_locs_flattened += y_list
    plot.scatter(x_locs_flattened, y_locs_flattened,
                 color="black", alpha=0.3, size=4)
    return plot


def plot_params(plot, param_hist):
    """
    param_hist[0] = beta_s
    param_hist[1] = sigma_s
    param_hist[2] = mu_s
    param_hist[3] = beta_e
    param_hist[4] = sigma_e
    param_hist[5] = mu_e
    param_hist[6] = eta
    param_hist[7] = max(len(X_o))
    param_hist[8] = len(X_n)
    """
    marker_size = 8
    alpha_level = 0.6
    iterations = [i for i in range(len(param_hist[0]))]
    # plot beta
    beta_s = param_hist[0]
    beta_e = param_hist[3]
    plot.line(iterations, beta_s, color='royalblue', legend='beta_s')
    plot.line(iterations, beta_e, color='royalblue', legend='beta_e')
    plot.circle(iterations, beta_s, color='royalblue',
                fill_color='white', size=marker_size, legend='beta_s')
    plot.circle(
        iterations, beta_e, color='royalblue', alpha=alpha_level, size=marker_size, legend='beta_e')
    # plot sigma
    sigma_s = param_hist[1]
    sigma_e = param_hist[4]
    plot.line(iterations, sigma_s, color='green', legend='sigma_s')
    plot.line(iterations, sigma_e, color='green', legend='sigma_e')
    plot.square(iterations, sigma_s, color='green',
                fill_color='white', size=marker_size, legend='sigma_s')
    plot.square(
        iterations, sigma_e, color='green', alpha=alpha_level, size=marker_size, legend='sigma_e')
    # plot mu
    mu_s = [param_hist[2][i]/param_hist[8] for i in range(len(param_hist[2]))]
    mu_e = [param_hist[5][i]/param_hist[8] for i in range(len(param_hist[5]))]
    plot.line(iterations, mu_s, color='black', legend='mu_s/j_max')
    plot.line(iterations, mu_e, color='black', legend='mu_e/j_max')
    plot.inverted_triangle(iterations, mu_s, color='black',
                           fill_color='white', size=marker_size, legend='mu_s/j_max')
    plot.inverted_triangle(
        iterations, mu_e, color='black', size=marker_size, alpha=alpha_level, legend='mu_e/j_max')
    return plot
