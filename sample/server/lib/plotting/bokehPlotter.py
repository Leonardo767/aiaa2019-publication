from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.layouts import gridplot
from server.lib.plotting.bokehUtils import (
    plot_airports, plot_sim, plot_paths, plot_contact, plot_nodes,
    plot_params)


def make_geo_plot(geo_info, airport_info, flights, sim_info, sim_info_style):
    plot_execute = figure()
    plot_execute.x_range = Range1d(0, geo_info["dims"][0])
    plot_execute.y_range = Range1d(0, geo_info["dims"][1])
    x_corners = [-0.05, geo_info["dims"][0] + 0.05,
                 geo_info["dims"][0] + 0.05, -0.05, -0.05]
    y_corners = [-0.05, -0.05, geo_info["dims"]
                 [1] + 0.05, geo_info["dims"][1] + 0.05, -0.05]
    plot_execute.line(x_corners, y_corners, color="black")
    plot_sim(plot_execute, sim_info, sim_info_style)
    plot_paths(plot_execute, flights)
    plot_airports(plot_execute, geo_info, airport_info)
    plot_execute.legend.location = "top_left"
    plot_execute.xaxis[0].axis_label = '<- West  |  East ->'
    plot_execute.yaxis[0].axis_label = '<- South  |  North ->'

    script, div = components(plot_execute)
    return [script, div]


def make_results_plot(geo_info, created_nodes, contact_points, i):
    plot_results = figure(title="Iteration #{}".format(i))
    plot_results.x_range = Range1d(0, geo_info["dims"][0])
    plot_results.y_range = Range1d(0, geo_info["dims"][1])
    x_corners = [-0.05, geo_info["dims"][0] + 0.05,
                 geo_info["dims"][0] + 0.05, -0.05, -0.05]
    y_corners = [-0.05, -0.05, geo_info["dims"]
                 [1] + 0.05, geo_info["dims"][1] + 0.05, -0.05]
    plot_results.line(x_corners, y_corners, color="black")
    plot_results.xaxis[0].axis_label = '<- West  |  East ->'
    plot_results.yaxis[0].axis_label = '<- South  |  North ->'
    plot_contact(plot_results, contact_points)
    plot_nodes(plot_results, created_nodes, contact_points)

    script, div = components(plot_results)
    return [script, div]


def plot_param_hist(param_hist_results_package):
    grid_input = []
    for flight_number, leg_times in param_hist_results_package.items():
        row_of_plots = []
        for leg_time, param_hist in leg_times.items():
            if len(param_hist):
                p = figure(title='Flight {}, Leg Time: {}'.format(
                    flight_number, leg_time), plot_width=800, plot_height=400)
                plot_params(p, param_hist)
                row_of_plots.append(p)
        grid_input += [row_of_plots]
    print(grid_input)
    grid = gridplot(grid_input)
    output_file("sample/server/plots/param_hist.html")
    show(grid)
    return
