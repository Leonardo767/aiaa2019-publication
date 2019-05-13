from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.plotting import figure, show
from bokeh.util.compiler import TypeScript
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead
import numpy as np


def plot_path(plot, X_n):

    plot.circle(X_n[:, 0], X_n[:, 1], color="black", alpha=0.8, size=8)
    plot.line(X_n[:, 0], X_n[:, 1], color="black", alpha=1, line_width=2)
    return plot


def plot_sim(plot, sim_points):
    plot.diamond(sim_points[:, 0], sim_points[:, 1],
                 color="grey", alpha=0.8, size=10)
    plot.line(sim_points[:, 0], sim_points[:, 1],
              color="grey", alpha=1, line_width=2)
    return plot


def plot_contact(plot, X_o):
    plot.diamond(X_o[:, 0], X_o[:, 1],
                 color="#630a0a", alpha=0.8, size=14)
    plot.line(X_o[:, 0], X_o[:, 1],
              color="#630a0a", alpha=1, line_width=2)
    return plot


def plot_anchors(plot, anchors, X_n):
    plot.diamond(anchors[:, 0], anchors[:, 1],
                 color="#630a0a", alpha=0.3, size=36)
    anchors_list = anchors.tolist()
    X_n_list = X_n.tolist()
    # s
    for i in X_n_list:
        plot.line([i[0], anchors_list[0][0]], [
                  i[1], anchors_list[0][1]], color='green', alpha=0.3)
    # e
    for i in X_n_list:
        plot.line([i[0], anchors_list[1][0]], [
                  i[1], anchors_list[1][1]], color='blue', alpha=0.3)
    return plot


def plot_ortho(plot, X_n, neg=1, color_choice='blue'):
    X_n_list = X_n.tolist()
    for i in X_n_list:
        new_point = [i[0] + neg*1/(5**0.5), i[1] + neg*4/(5**0.5)]
        plot.add_layout(Arrow(end=NormalHead(fill_color=color_choice, size=10),
                              x_start=i[0], y_start=i[1], x_end=new_point[0],
                              y_end=new_point[1], line_color=color_choice,
                              line_alpha=0.8))
    return plot


def generate_delta_distribution(j_vector, beta, sigma, mu):
    scaling_factor = beta/(2 * 3.14159 * sigma**2)**0.5
    exp_factor = -(j_vector - mu)**2/(2*sigma**2)
    X_n_delta = scaling_factor*np.exp(exp_factor)
    return X_n_delta


def plot_dev(plot, X_n, params, neg=1):
    beta, sigma, mu = params
    j = 33
    j_vector = np.linspace(0, j - 1, j)
    dev = generate_delta_distribution(j_vector, beta, sigma, mu)
    X_n_list = X_n.tolist()
    j_count = 0
    ultra_x = []
    ultra_y = []
    for i in X_n_list:
        new_point = [i[0] + dev[j_count]*neg*1 /
                     (5**0.5), i[1] + dev[j_count]*neg*4/(5**0.5)]
        x = [i[0], new_point[0]]
        y = [i[1], new_point[1]]
        plot.line(x, y, color='black', alpha=0.3)
        plot.circle(x, y, color='black', alpha=0.8, size=5)
        j_count += 1
        ultra_x.append(new_point[0])
        ultra_y.append(new_point[1])
    plot.line(ultra_x, ultra_y, color='black', alpha=0.3, line_width=2)
    return plot


def plot_new_path(plot, X_n, winners, neg=1):
    j = 33
    j_vector = np.linspace(0, j - 1, j)
    beta1, sigma1, mu1 = winners[0]
    dev1 = generate_delta_distribution(j_vector, beta1, sigma1, mu1)
    beta2, sigma2, mu2 = winners[1]
    dev2 = generate_delta_distribution(j_vector, beta2, sigma2, mu2)
    X_n_list = X_n.tolist()
    j_count = 0
    ultra_x = []
    ultra_y = []
    for i in X_n_list:
        new_point = [i[0] + (dev1[j_count] - dev2[j_count])*neg*1 /
                     (5**0.5), i[1] + (dev1[j_count] - dev2[j_count])*neg*4/(5**0.5)]
        x = [i[0], new_point[0]]
        y = [i[1], new_point[1]]
        plot.line(x, y, color='black', alpha=0.3)
        plot.circle(x, y, color='black', alpha=0.5, size=2)
        j_count += 1
        ultra_x.append(new_point[0])
        ultra_y.append(new_point[1])
    plot.line(ultra_x, ultra_y, color='black', alpha=1, line_width=2)
    plot.circle(ultra_x, ultra_y, color='black', alpha=0.8, size=8)
    return plot
