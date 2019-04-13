from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from server.lib.plotUtils import plot_airports, plot_sim


def make_geo_plot(geo_info, airport_info, flights, sim_info, sim_info_style):
    plot_execute = figure()
    plot_airports(plot_execute, geo_info, airport_info)
    plot_sim(plot_execute, sim_info, sim_info_style)
    plot_execute.xaxis[0].axis_label = '<- West  |  East ->'
    plot_execute.yaxis[0].axis_label = '<- South  |  North ->'

    script, div = components(plot_execute)
    return [script, div]
