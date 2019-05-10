from plotly.offline import plot
from plotly import graph_objs as go
from server.lib.plotting.plotlyUtils import (specify_axes, specify_layout, plot_all_sim_paths,
                                             plot_all_flights, plot_all_nodes, plot_all_nodes_sim, plot_all_contact_nodes)


def make_progress_plot(geo_info, sim_info, flights, created_nodes, created_nodes_sim, contact_points, iter_val):
    xaxis, yaxis, zaxis = specify_axes(geo_info)
    sim_paths = plot_all_sim_paths(sim_info)
    flight_paths = plot_all_flights(flights)
    node_scatter_plot = plot_all_nodes(created_nodes)
    node_scatter_plot_sim = plot_all_nodes_sim(created_nodes_sim)
    contact_point_scatter_plot = plot_all_contact_nodes(contact_points)
    # airport_locs = go.Scatter3d()
    data = sim_paths + flight_paths + node_scatter_plot + \
        node_scatter_plot_sim + contact_point_scatter_plot
    layout = specify_layout(xaxis, yaxis, zaxis, iter_val)
    figure = dict(data=data, layout=layout)
    plot(figure, filename="sample/server/plots3d/progress_3d-plot.html")
