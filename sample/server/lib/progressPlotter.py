from plotly.offline import plot
from plotly import graph_objs as go
from server.lib.plotUtils3d import specify_axes, specify_layout, plot_all_sim_paths, plot_all_flights, plot_all_nodes


def make_progress_plot(geo_info, sim_info, flights, created_nodes):
    xaxis, yaxis, zaxis = specify_axes(geo_info)
    sim_paths = plot_all_sim_paths(sim_info)
    flight_paths = plot_all_flights(flights)
    node_scatter_plot = plot_all_nodes(created_nodes)
    airport_locs = go.Scatter3d()
    data = sim_paths + flight_paths + node_scatter_plot
    layout = specify_layout(xaxis, yaxis, zaxis)
    figure = dict(data=data, layout=layout)
    plot(figure, filename="sample/server/plots3d/progress_3d-plot.html")
