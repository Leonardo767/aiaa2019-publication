from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label


def make_geo_plot(geo_info, airport_info):
    x_locs = []
    y_locs = []
    airport_labels = []
    print(airport_info)
    for airport_name, airport_data in airport_info.items():
        x_locs.append(airport_data[0][0])
        y_locs.append(airport_data[0][1])
        airport_labels.append(airport_name)
    source = ColumnDataSource(
        data=dict(x_locs=x_locs, y_locs=y_locs, airport_labels=airport_labels))

    plot = figure()
    airport_icon_size = 30
    plot.x_range = Range1d(0, geo_info["dims"][0])
    plot.y_range = Range1d(0, geo_info["dims"][1])
    plot.square(x='x_locs', y='y_locs', size=airport_icon_size,
                source=source, fill_alpha=0.3)

    plot.xaxis[0].axis_label = '<- West  |  East ->'
    plot.yaxis[0].axis_label = '<- South  |  North ->'

    labels = LabelSet(x='x_locs', y='y_locs', text='airport_labels', level='glyph',
                      x_offset=-5, y_offset=-10, source=source, render_mode='css')

    plot.add_layout(labels)

    script, div = components(plot)
    return [script, div]
