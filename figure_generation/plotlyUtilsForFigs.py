from plotly import graph_objs as go


def specify_axes(geo_info, timespan=None):
    dim_x = geo_info["dims"][0]
    dim_y = geo_info["dims"][1]
    if timespan is None:
        timespan = geo_info["timespan"].total_seconds()/3600
    xaxis = dict(
        title='East/West, nm.',
        range=[2, dim_x],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    yaxis = dict(
        title='North/South, nm.',
        range=[0, dim_y],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    zaxis = dict(
        title='Time, hrs',
        range=[20.0, timespan],
        gridcolor='rgb(190, 190, 190)',
        zerolinecolor='rgb(190, 190, 190)',
        showbackground=True,
        backgroundcolor='rgb(230, 230,230)'
    )
    return xaxis, yaxis, zaxis


def specify_layout(xaxis, yaxis, zaxis, iter_val, given_title=None):
    if given_title is None:
        used_title = "Iteration = " + str(iter_val)
    else:
        used_title = given_title
    layout = dict(
        width=1900,
        height=1000,
        autosize=False,
        title=used_title,
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
            aspectratio=dict(x=0.6, y=1, z=0.8),
            aspectmode='manual'
        ),
    )
    return layout


def plot_single_flight(flight_points, color_choice='black'):
    x = []
    y = []
    t = []
    for point in flight_points:
        x.append(point[0])
        y.append(point[1])
        t.append(point[2])
    flight_path = go.Scatter3d(
        x=x, y=y, z=t, opacity=0.8,
        marker=dict(
            size=4,
            color=color_choice
        ),
        line=dict(
            color=color_choice,
            width=4
        )
    )
    return [flight_path]


def plot_all_contact_nodes(contact_points):
    x = []
    y = []
    t = []
    for node in contact_points:
        x.append(node[0])
        y.append(node[1])
        t.append(node[2])
    contact_point_scatter_plot = [go.Scatter3d(
        x=x, y=y, z=t, opacity=0.8,
        mode='markers',
        marker=dict(
            size=4,
            color='#630a0a'
        )
    )]
    return contact_point_scatter_plot


def plot_dist_vectors(dist_vectors, color_choice):
    all_dist_vectors = []
    for dist in dist_vectors:
        x = [dist[0][0], dist[1][0]]
        y = [dist[0][1], dist[1][1]]
        t = [dist[0][2], dist[1][2]]
        one_line = go.Scatter3d(
            x=x, y=y, z=t, opacity=0.3, mode='lines',
            line=dict(
                color=color_choice,
                width=2
            )
        )
        all_dist_vectors.append(one_line)
    return all_dist_vectors


def plot_arrows(points_tuple_list, color_choice='black', width_choice=2):
    vect_plotted = []
    for points_tuple in points_tuple_list:
        x = [points_tuple[0][0], points_tuple[1][0]]
        y = [points_tuple[0][1], points_tuple[1][1]]
        t = [points_tuple[0][2], points_tuple[1][2]]
        one_line = go.Scatter3d(
            x=x, y=y, z=t, opacity=0.8, mode='lines',
            line=dict(
                color=color_choice,
                width=width_choice
            )
        )
        vect_plotted.append(one_line)
    return vect_plotted
