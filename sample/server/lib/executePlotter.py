from bokeh.plotting import figure
from bokeh.embed import components


def make_geo_plot():
    plot = figure()
    plot.circle([1, 2], [3, 4])
    script, div = components(plot)
    return [script, div]
