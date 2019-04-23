from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from server.lib.plotting.bokehUtils import (
    plot_airports, plot_sim, plot_paths, plot_contact, plot_nodes)


def make_geo_plot(geo_info, airport_info, flights, sim_info, sim_info_style):
    plot_execute = figure()
    plot_execute.x_range = Range1d(0, geo_info["dims"][0])
    plot_execute.y_range = Range1d(0, geo_info["dims"][1])
    x_corners = [-0.05, geo_info["dims"][0] + 0.05,
                 geo_info["dims"][0] + 0.05, -0.05, -0.05]
    y_corners = [-0.05, -0.05, geo_info["dims"]
                 [1] + 0.05, geo_info["dims"][1] + 0.05, -0.05]
    plot_execute.line(x_corners, y_corners, color="black")
    plot_airports(plot_execute, geo_info, airport_info)
    plot_sim(plot_execute, sim_info, sim_info_style)
    plot_paths(plot_execute, flights)
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