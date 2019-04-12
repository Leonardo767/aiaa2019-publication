from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import io
import random

# from jinja2 import Template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view


def make_geo_plot():

    ########## BUILD FIGURES ################

    PLOT_OPTIONS = dict(plot_width=800, plot_height=300)
    SCATTER_OPTIONS = dict(size=12, alpha=0.5)

    def data(): return [random.choice([i for i in range(100)])
                        for r in range(10)]

    red = figure(sizing_mode='scale_width', tools='pan', **PLOT_OPTIONS)
    red.scatter(data(), data(), color="red", **SCATTER_OPTIONS)

    blue = figure(sizing_mode='fixed', tools='pan', **PLOT_OPTIONS)
    blue.scatter(data(), data(), color="blue", **SCATTER_OPTIONS)

    green = figure(sizing_mode='scale_width', tools='pan', **PLOT_OPTIONS)
    green.scatter(data(), data(), color="green", **SCATTER_OPTIONS)

    """
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    # output_file("lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    show(p)
    script, div_dict = components({"plot": p})
    return [script, div_dict]
    """
    resources = INLINE.render()
    script, div = components({'red': red, 'blue': blue, 'green': green})
    return [script, div, resources]
