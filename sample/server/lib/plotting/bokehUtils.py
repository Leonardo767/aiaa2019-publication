from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label


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