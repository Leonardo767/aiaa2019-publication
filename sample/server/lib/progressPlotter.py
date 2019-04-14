from plotly.offline import plot
from plotly import graph_objs as go
from server.lib.plotUtils3d import specify_axes, specify_layout, plot_all_sim_paths, plot_all_flights


def make_progress_plot(geo_info, sim_info, flights):
    xaxis, yaxis, zaxis = specify_axes(geo_info)
    sim_paths = plot_all_sim_paths(sim_info)
    flight_paths = plot_all_flights(flights)
    airport_locs = go.Scatter3d()
    data = sim_paths + flight_paths
    layout = specify_layout(xaxis, yaxis, zaxis)
    figure = dict(data=data, layout=layout)
    plot(figure, filename="sample/server/plots3d/progress_3d-plot.html")
