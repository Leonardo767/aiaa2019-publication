from plotly.offline import plot
from plotly import graph_objs as go
from plotlyUtilsForFigs import (
    plot_all_contact_nodes, specify_layout, specify_axes,
    plot_single_flight, plot_dist_vectors, plot_arrows)
from calcForFigs import (
    create_dist_vectors, generate_alteration_vectors, generate_ortho_vectors)


def make_alteration_plot(X_n, X_o, X_n_path, X_o_sim):
    # initial settings
    geo_info = {"dims": (5, 5)}
    contact_points = X_o
    iter_val = 0
    title = 'Alteration Planes'

    # some calcs
    d_s = create_dist_vectors(X_n, X_o[0])
    d_e = create_dist_vectors(X_n, X_o[-1])
    X_n_s = generate_alteration_vectors(X_n, d_s, beta=2., sigma=3.55, mu=4.2)
    X_n_e = generate_alteration_vectors(X_n, d_e, beta=3.0, sigma=5.45, mu=20)
    s_orthos = generate_ortho_vectors(X_n, X_n_s)
    e_orthos = generate_ortho_vectors(X_n, X_n_e)

    # plotting
    xaxis, yaxis, zaxis = specify_axes(geo_info, timespan=24.0)

    flight_paths = plot_single_flight(X_n)
    contact_point_scatter_plot = plot_all_contact_nodes(contact_points)
    plotted_d_s = plot_dist_vectors(d_s, 'green')
    plotted_d_e = plot_dist_vectors(d_e, 'blue')
    plotted_X_n_s = plot_single_flight(X_n_s, color_choice='green')
    plotted_X_n_e = plot_single_flight(X_n_e, color_choice='blue')
    plotted_path = plot_arrows(X_n_path, width_choice=6)
    plotted_sim = plot_arrows(X_o_sim, color_choice='#b949ff', width_choice=6)
    plotted_orthos_s = plot_arrows(s_orthos, color_choice='green')
    plotted_orthos_e = plot_arrows(e_orthos, color_choice='blue')

    data = plotted_path + plotted_sim + plotted_orthos_s + plotted_orthos_e + \
        contact_point_scatter_plot + flight_paths + plotted_d_s + plotted_d_e + \
        plotted_X_n_s + plotted_X_n_e
    layout = specify_layout(xaxis, yaxis, zaxis, iter_val, given_title=title)
    figure = dict(data=data, layout=layout)
    plot(figure, filename="figure_generation/alteration_plot.html")


X_n = [[3.0250,  1.0750, 21.0625],
       [3.0500,  1.1500, 21.1250],
       [3.0750,  1.2250, 21.1875],
       [3.1000,  1.3000, 21.2500],
       [3.1250,  1.3750, 21.3125],
       [3.1500,  1.4500, 21.3750],
       [3.1750,  1.5250, 21.4375],
       [3.2000,  1.6000, 21.5000],
       [3.2250,  1.6750, 21.5625],
       [3.2500,  1.7500, 21.6250],
       [3.2750,  1.8250, 21.6875],
       [3.3000,  1.9000, 21.7500],
       [3.3250,  1.9750, 21.8125],
       [3.3500,  2.0500, 21.8750],
       [3.3750,  2.1250, 21.9375],
       [3.4000,  2.2000, 22.0000],
       [3.4250,  2.2750, 22.0625],
       [3.4500,  2.3500, 22.1250],
       [3.4750,  2.4250, 22.1875],
       [3.5000,  2.5000, 22.2500],
       [3.5250,  2.5750, 22.3125],
       [3.5500,  2.6500, 22.3750],
       [3.5750,  2.7250, 22.4375],
       [3.6000,  2.8000, 22.5000],
       [3.6250,  2.8750, 22.5625],
       [3.6500,  2.9500, 22.6250],
       [3.6750,  3.0250, 22.6875],
       [3.7000,  3.1000, 22.7500],
       [3.7250,  3.1750, 22.8125],
       [3.7500,  3.2500, 22.8750],
       [3.7750,  3.3250, 22.9375],
       [3.8000,  3.4000, 23.0000],
       [3.8250,  3.4750, 23.0625],
       [3.8500,  3.5500, 23.1250],
       [3.8750,  3.6250, 23.1875],
       [3.9000,  3.7000, 23.2500],
       [3.9250,  3.7750, 23.3125],
       [3.9500,  3.8500, 23.3750],
       [3.9750,  3.9250, 23.4375],
       [4.0000,  4.0000, 23.5000]]

X_o = [[3.2944,  1.3106, 21.2219],
       [3.2950,  1.3150, 21.2250],
       [3.2956,  1.3194, 21.2281],
       [3.2963,  1.3237, 21.2312],
       [3.2969,  1.3281, 21.2344],
       [3.3069,  1.3981, 21.2844],
       [3.3075,  1.4025, 21.2875],
       [3.3081,  1.4069, 21.2906],
       [3.3087,  1.4112, 21.2937],
       [3.3094,  1.4156, 21.2969],
       [3.3100,  1.4200, 21.3000],
       [3.3106,  1.4244, 21.3031],
       [3.3112,  1.4287, 21.3062],
       [3.3119,  1.4331, 21.3094],
       [3.3125,  1.4375, 21.3125],
       [3.3131,  1.4419, 21.3156],
       [3.3194,  1.4856, 21.3469],
       [3.3200,  1.4900, 21.3500],
       [3.3206,  1.4944, 21.3531],
       [3.3213,  1.4988, 21.3562],
       [3.3219,  1.5031, 21.3594],
       [3.3225,  1.5075, 21.3625],
       [3.3231,  1.5119, 21.3656],
       [3.3237,  1.5162, 21.3687],
       [3.3244,  1.5206, 21.3719],
       [3.3250,  1.5250, 21.3750],
       [3.3256,  1.5294, 21.3781],
       [3.3262,  1.5337, 21.3813],
       [3.3269,  1.5381, 21.3844],
       [3.3319,  1.5731, 21.4094],
       [3.3325,  1.5775, 21.4125],
       [3.3331,  1.5819, 21.4156],
       [3.3338,  1.5863, 21.4187],
       [3.3344,  1.5906, 21.4219],
       [3.3350,  1.5950, 21.4250],
       [3.3356,  1.5994, 21.4281],
       [3.3363,  1.6038, 21.4312],
       [3.3369,  1.6081, 21.4344],
       [3.3375,  1.6125, 21.4375],
       [3.3381,  1.6169, 21.4406],
       [3.3388,  1.6212, 21.4438],
       [3.3394,  1.6256, 21.4469],
       [3.3400,  1.6300, 21.4500],
       [3.3406,  1.6344, 21.4531],
       [3.3444,  1.6606, 21.4719],
       [3.3450,  1.6650, 21.4750],
       [3.3456,  1.6694, 21.4781],
       [3.3462,  1.6738, 21.4812],
       [3.3469,  1.6781, 21.4844],
       [3.3475,  1.6825, 21.4875],
       [3.3481,  1.6869, 21.4906],
       [3.3487,  1.6913, 21.4937],
       [3.3494,  1.6956, 21.4969],
       [3.3500,  1.7000, 21.5000],
       [3.3506,  1.7044, 21.5031],
       [3.3512,  1.7087, 21.5063],
       [3.3519,  1.7131, 21.5094],
       [3.3525,  1.7175, 21.5125],
       [3.3531,  1.7219, 21.5156],
       [3.3537,  1.7262, 21.5188],
       [3.3569,  1.7481, 21.5344],
       [3.3575,  1.7525, 21.5375],
       [3.3581,  1.7569, 21.5406],
       [3.3588,  1.7612, 21.5437],
       [3.3594,  1.7656, 21.5469],
       [3.3600,  1.7700, 21.5500],
       [3.3606,  1.7744, 21.5531],
       [3.3613,  1.7788, 21.5562],
       [3.3619,  1.7831, 21.5594],
       [3.3625,  1.7875, 21.5625],
       [3.3631,  1.7919, 21.5656],
       [3.3638,  1.7963, 21.5688],
       [3.3644,  1.8006, 21.5719],
       [3.3650,  1.8050, 21.5750],
       [3.3656,  1.8094, 21.5781],
       [3.3662,  1.8138, 21.5813],
       [3.3694,  1.8356, 21.5969],
       [3.3700,  1.8400, 21.6000],
       [3.3706,  1.8444, 21.6031],
       [3.3712,  1.8487, 21.6062],
       [3.3719,  1.8531, 21.6094],
       [3.3725,  1.8575, 21.6125],
       [3.3731,  1.8619, 21.6156],
       [3.3737,  1.8662, 21.6187],
       [3.3744,  1.8706, 21.6219],
       [3.3750,  1.8750, 21.6250],
       [3.3756,  1.8794, 21.6281],
       [3.3763,  1.8838, 21.6313],
       [3.3769,  1.8881, 21.6344],
       [3.3775,  1.8925, 21.6375],
       [3.3781,  1.8969, 21.6406],
       [3.3788,  1.9013, 21.6438],
       [3.3819,  1.9231, 21.6594],
       [3.3825,  1.9275, 21.6625],
       [3.3831,  1.9319, 21.6656],
       [3.3838,  1.9363, 21.6687],
       [3.3844,  1.9406, 21.6719],
       [3.3850,  1.9450, 21.6750],
       [3.3856,  1.9494, 21.6781],
       [3.3862,  1.9538, 21.6812],
       [3.3869,  1.9581, 21.6844],
       [3.3875,  1.9625, 21.6875],
       [3.3881,  1.9669, 21.6906],
       [3.3887,  1.9712, 21.6938],
       [3.3894,  1.9756, 21.6969],
       [3.3900,  1.9800, 21.7000],
       [3.3906,  1.9844, 21.7031],
       [3.3944,  2.0106, 21.7219],
       [3.3950,  2.0150, 21.7250],
       [3.3956,  2.0194, 21.7281],
       [3.3963,  2.0237, 21.7312],
       [3.3969,  2.0281, 21.7344],
       [3.3975,  2.0325, 21.7375],
       [3.3981,  2.0369, 21.7406],
       [3.3988,  2.0412, 21.7437],
       [3.3994,  2.0456, 21.7469],
       [3.4000,  2.0500, 21.7500],
       [3.4006,  2.0544, 21.7531],
       [3.4013,  2.0587, 21.7563],
       [3.4019,  2.0631, 21.7594],
       [3.4025,  2.0675, 21.7625],
       [3.4069,  2.0981, 21.7844],
       [3.4075,  2.1025, 21.7875],
       [3.4081,  2.1069, 21.7906],
       [3.4087,  2.1113, 21.7937],
       [3.4094,  2.1156, 21.7969],
       [3.4100,  2.1200, 21.8000],
       [3.4106,  2.1244, 21.8031],
       [3.4112,  2.1288, 21.8062],
       [3.4119,  2.1331, 21.8094],
       [3.4125,  2.1375, 21.8125],
       [3.4131,  2.1419, 21.8156],
       [3.4137,  2.1463, 21.8188],
       [3.4144,  2.1506, 21.8219],
       [3.4194,  2.1856, 21.8469],
       [3.4200,  2.1900, 21.8500],
       [3.4206,  2.1944, 21.8531],
       [3.4213,  2.1987, 21.8562],
       [3.4219,  2.2031, 21.8594],
       [3.4225,  2.2075, 21.8625],
       [3.4231,  2.2119, 21.8656],
       [3.4238,  2.2162, 21.8687],
       [3.4244,  2.2206, 21.8719],
       [3.4250,  2.2250, 21.8750],
       [3.4256,  2.2294, 21.8781],
       [3.4263,  2.2337, 21.8813],
       [3.4319,  2.2731, 21.9094],
       [3.4325,  2.2775, 21.9125],
       [3.4331,  2.2819, 21.9156],
       [3.4337,  2.2862, 21.9187],
       [3.4344,  2.2906, 21.9219],
       [3.4350,  2.2950, 21.9250],
       [3.4356,  2.2994, 21.9281],
       [3.4362,  2.3037, 21.9312],
       [3.4369,  2.3081, 21.9344],
       [3.4375,  2.3125, 21.9375],
       [3.4444,  2.3606, 21.9719],
       [3.4450,  2.3650, 21.9750],
       [3.4456,  2.3694, 21.9781],
       [3.4463,  2.3738, 21.9812],
       [3.4469,  2.3781, 21.9844],
       [3.4475,  2.3825, 21.9875],
       [3.4481,  2.3869, 21.9906],
       [3.4487,  2.3913, 21.9937],
       [3.4569,  2.4481, 22.0344],
       [3.4575,  2.4525, 22.0375],
       [3.4581,  2.4569, 22.0406],
       [3.4588,  2.4612, 22.0437],
       [3.4594,  2.4656, 22.0469],
       [3.4600,  2.4700, 22.0500],
       [3.4694,  2.5356, 22.0969],
       [3.4700,  2.5400, 22.1000],
       [3.4706,  2.5444, 22.1031],
       [3.4712,  2.5488, 22.1062],
       [3.4819,  2.6231, 22.1594]]

steps = 5
X_n_path = [([3, 1, 21], [4 + .025*steps, 4 + .075*steps, 23.5 + 0.0625*steps])]
X_o_sim = [([3.25, 1, 21.0], [3.75, 4.5, 23.5])]

make_alteration_plot(X_n, X_o, X_n_path, X_o_sim)
