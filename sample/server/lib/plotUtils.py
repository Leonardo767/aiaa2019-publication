from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label


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
    plot.x_range = Range1d(0, geo_info["dims"][0])
    plot.y_range = Range1d(0, geo_info["dims"][1])
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
    object_names = []
    for sim_object_name, sim_points in sim_info.items():
        x_locs_object = []
        y_locs_object = []
        for point in sim_points:
            x_locs_object.append(point[0])
            y_locs_object.append(point[1])
        x_locs.append(x_locs_object)
        y_locs.append(y_locs_object)
        object_names.append(sim_object_name)
    print(x_locs)
    plot.multi_line(x_locs, y_locs,
                    color=["pink", "pink"], alpha=[0.9, 0.9], line_width=4)
    # unpack x_locs and y_locs to create triangle endpoints
    x_loc_triangle = []
    y_loc_triangle = []
    for x_object, y_object in zip(x_locs, y_locs):
        for x, y in zip(x_object, y_object):
            x_loc_triangle.append(x)
            y_loc_triangle.append(y)
    plot.inverted_triangle(x_loc_triangle, y_loc_triangle, size=15,
                           color="pink", line_color="purple")
    return plot
