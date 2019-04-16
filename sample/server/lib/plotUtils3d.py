from plotly import graph_objs as go


def specify_axes(geo_info):
    dim_x = geo_info["dims"][0]
    dim_y = geo_info["dims"][1]
    timespan = geo_info["timespan"].total_seconds()/3600
    xaxis = dict(
        title='East/West',
        range=[0, dim_x],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    yaxis = dict(
        title='North/South',
        range=[0, dim_y],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    zaxis = dict(
        title='Time [hrs]',
        range=[0, timespan],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    return xaxis, yaxis, zaxis


def specify_layout(xaxis, yaxis, zaxis):
    layout = dict(
        width=1900,
        height=1000,
        autosize=False,
        title='Geo',
        scene=dict(
            xaxis=xaxis,
            yaxis=yaxis,
            zaxis=zaxis,
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=-1.7428,
                    y=1.0707,
                    z=0.7100,
                )
            ),
            aspectratio=dict(x=1, y=1, z=2),
            aspectmode='manual'
        ),
    )
    return layout


def plot_single_sim_path(sim_points):
    x = []
    y = []
    t = []
    for point in sim_points:
        x.append(point[0])
        y.append(point[1])
        t.append(point[2].total_seconds()/3600)
    sim_path = go.Scatter3d(
        x=x, y=y, z=t, opacity=0.5,
        marker=dict(
            symbol='diamond',
            size=8,
            color='#b949ff'
        ),
        line=dict(
            color='#b949ff',
            width=4
        )
    )
    return sim_path


def plot_all_sim_paths(sim_info):
    sim_paths = []
    for _, sim_points in sim_info.items():
        sim_paths.append(plot_single_sim_path(sim_points))
    return sim_paths


def plot_single_flight(flight_points):
    x = []
    y = []
    t = []
    for point in flight_points:
        x.append(point[0])
        y.append(point[1])
        t.append(point[2].total_seconds()/3600)
    flight_path = go.Scatter3d(
        x=x, y=y, z=t, opacity=0.3,
        marker=dict(
            size=10,
            color='#000000'
        ),
        line=dict(
            color='#000000',
            width=4
        )
    )
    return flight_path


def plot_all_flights(flights):
    flight_paths = []
    for _, flight_endpoints in flights.items():
        flight_paths.append(plot_single_flight(flight_endpoints))
    return flight_paths


def plot_all_nodes(created_nodes):
    x = []
    y = []
    t = []
    parent_flight = []
    for flight_number, nodes_for_flight in created_nodes.items():
        for _, nodes_list in nodes_for_flight.items():
            for node in nodes_list:
                x.append(node[0])
                y.append(node[1])
                t.append(node[2])
                parent_flight.append(flight_number)
    node_scatter_plot = [go.Scatter3d(
        x=x, y=y, z=t, opacity=0.3,
        mode='markers',
        marker=dict(
            size=3,
            color='#000000'
        )
    )]
    return node_scatter_plot


def plot_all_nodes_sim(created_nodes_sim):
    x = []
    y = []
    t = []
    parent_flight = []
    for sim_object_name, nodes_for_object in created_nodes_sim.items():
        for _, nodes_list in nodes_for_object.items():
            for node in nodes_list:
                x.append(node[0])
                y.append(node[1])
                t.append(node[2])
                parent_flight.append(sim_object_name)
    node_scatter_plot_sim = [go.Scatter3d(
        x=x, y=y, z=t, opacity=0.05,
        mode='markers',
        marker=dict(
            size=2,
            color='#b949ff'
        )
    )]
    return node_scatter_plot_sim
