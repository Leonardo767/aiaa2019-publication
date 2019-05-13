from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from calcFor2d import (plot_path, plot_sim, plot_contact,
                       plot_anchors, plot_ortho, plot_dev, plot_new_path)
import numpy as np


def plot_2d(X_n, sim_points, X_o, anchors):
    p = figure(plot_width=1360, plot_height=840)
    p.x_range = Range1d(-0.5, 16.5)
    p.y_range = Range1d(-0.5, 10)
    p.xgrid.grid_line_color = 'black'
    p.xgrid.grid_line_alpha = 0.2
    p.xgrid.minor_grid_line_color = 'black'
    p.xgrid.minor_grid_line_alpha = 0.1
    p.ygrid.grid_line_color = 'black'
    p.ygrid.grid_line_alpha = 0.2
    p.ygrid.minor_grid_line_color = 'black'
    p.ygrid.minor_grid_line_alpha = 0.1

    # plot_anchors(p, anchors, X_n)
    # plot_path(p, X_n)
    plot_sim(p, sim_points)
    plot_contact(p, X_o)
    # plot_ortho(p, X_n)
    # plot_ortho(p, X_n, neg=-1, color_choice='green')
    params1 = (4, 4, 20)
    params2 = (3, 6, 19)
    params3 = (4, 4, 14)
    params4 = (3, 6, 10)
    # plot_dev(p, X_n, params1)
    # plot_dev(p, X_n, params2)
    # plot_dev(p, X_n, params3, neg=-1)
    # plot_dev(p, X_n, params4, neg=-1)
    plot_new_path(p, X_n, (params2, params4))

    output_file("figure_generation/experiment2d.html")
    show(p)
    return


# record the node paths
x_locs = np.linspace(16., 0., 33).reshape((1, -1))
y_locs = -x_locs/4 + 6
X_n = np.concatenate((x_locs, y_locs), axis=0).T

# record the sim paths
x_locs = np.linspace(16., 0., 33).reshape((1, -1))
y_locs = -0.5*x_locs + 8
sim_paths = np.concatenate((x_locs, y_locs), axis=0).T

# generate contact event
X_o = sim_paths[12:22, :]
anchors = np.concatenate((X_o[0, :], X_o[-1, :]), axis=0).reshape((2, 2))
print(anchors)

plot_2d(X_n, sim_paths, X_o, anchors)
