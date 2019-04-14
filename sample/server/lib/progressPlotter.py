from plotly.offline import plot
from plotly import graph_objs as go


def make_progress_plot():
    x = [1, 2, 3, 5]
    y = [2, 3, 4, 5]
    z = [3, 3, 5, 5]
    trace = go.Scatter3d(
        x=x, y=y, z=z,
        marker=dict(
            size=4,
            color=z,
            colorscale='Viridis',
        ),
        line=dict(
            color='#1f77b4',
            width=1
        )
    )
    data = [trace]
    layout = dict(
        width=1000,
        height=1000,
        autosize=True,
        title='Iris dataset',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
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
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual'
        ),
    )
    figure = dict(data=data, layout=layout)
    return plot(figure, filename="sample/server/templates/progress_3d-plot.html")
