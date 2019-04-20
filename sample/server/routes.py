from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.data_wrangling.objects import Geo
from server.lib.data_wrangling.dbUtils import (informGeoSelection, informSimSelection,
                                               input2db_geo, save_settings, extract_settings,
                                               get_geo_info, get_sim_info, package_results,
                                               extract_results)
from server.lib.data_wrangling.dataUtils import (
    append_endpoints, create_interpolated_nodes, find_contact)
from server.lib.plotting.bokehPlotter import make_geo_plot, make_results_plot
from server.lib.plotting.plotlyPlotter import make_progress_plot
from server.src.main import main_path_optimizer


# NOTE: look inside the server __init__.py file for app initialization and configuration

@app.route('/', methods=['GET', 'POST'])
@app.route('/input_environment', methods=['GET', 'POST'])
def input_environment():
    return render_template('input_environment.html')


@app.route('/input_environment_select', methods=['GET', 'POST'])
def input_environment_select():
    EntryData, AirportData, GeoData, Airports, Entries = informGeoSelection(
        mysql)
    if request.method == 'POST':
        # fetch the form data (taking the form of a selection)
        selectionInput = request.form
        print(selectionInput)
        save_settings(mysql, "geo_selected",
                      selectionInput["geo_selected"])
        print(selectionInput["geo_selected"] +
              ' is selected as the geography.')
        return redirect(url_for('input_environment'))
    return render_template('input_environment_select.html', EntryData=EntryData, AirportData=AirportData, GeoData=GeoData, Airports=Airports, Entries=Entries)


@app.route('/input_environment_create', methods=['GET', 'POST'])
def input_environment_create():
    if request.method == 'POST':
        # fetch the form data (taking the form of a creation)
        newGeoDataInput = request.form
        input2db_geo(newGeoDataInput, mysql)
        return redirect(url_for('input_environment'))
    return render_template('input_environment_create.html')


@app.route('/input_sim', methods=['GET', 'POST'])
def input_sim():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('input_sim.html')


@app.route('/input_sim_select', methods=['GET', 'POST'])
def input_sim_select():
    SuiteData = informSimSelection(mysql)
    if request.method == 'POST':
        # fetch the form data (taking the form of a selection)
        selectionInput = request.form
        save_settings(mysql, "sim_selected",
                      selectionInput["sim_selected"])
        print(selectionInput["sim_selected"] +
              ' is selected as the sim suite.')
        return redirect(url_for('input_environment'))
    return render_template('input_sim_select.html', SuiteData=SuiteData)


@app.route('/input_sim_create', methods=['GET', 'POST'])
def input_sim_create():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('input_sim_create.html')


@app.route('/execute/', methods=['GET', 'POST'])
def execute():
    if request.method == 'POST':
        # run algorithm
        return redirect(url_for('progress'))
    return render_template('execute.html')


@app.route('/execute_settings', methods=['GET', 'POST'])
def execute_settings():
    if request.method == 'POST':
        # save settings and exit
        return redirect(url_for('execute'))
    all_settings = extract_settings(mysql, "geo_selected", all_settings=True)
    return render_template('execute_settings.html', all_settings=all_settings)


@app.route('/execute_plot', methods=['GET', 'POST'])
def execute_plot():
    if request.method == 'POST':
        # acknowledge plot and exit
        return redirect(url_for('execute'))
    selection_geo = extract_settings(mysql, called="geo_selected")
    selection_sim = extract_settings(mysql, called="sim_selected")
    print('We are using ' + selection_geo + ' as our geo.')
    print('We are using ' + selection_sim + ' as our sim.')
    geo_info, airport_info, flights = get_geo_info(mysql, selection_geo)
    sim_info, sim_info_style = get_sim_info(mysql, selection_sim)
    geo_plot = make_geo_plot(geo_info, airport_info, flights,
                             sim_info, sim_info_style)  # pass in plotting info
    return render_template('execute_plot.html', geo_plot=geo_plot)


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    # initialization
    # ----------------------------------------
    selection_geo = extract_settings(mysql, called="geo_selected")
    selection_sim = extract_settings(mysql, called="sim_selected")
    print('We are using ' + selection_geo + ' as our geo for 3dplot.')
    print('We are using ' + selection_sim + ' as our sim for 3d plot.')
    geo_info, _, flights = get_geo_info(mysql, selection_geo)
    sim_info, _ = get_sim_info(mysql, selection_sim)
    flights, sim_info = append_endpoints([flights, sim_info], geo_info)
    created_nodes = create_interpolated_nodes(flights)
    original_nodes = created_nodes.copy()
    sim_nodes_per_leg = extract_settings(mysql, called="sim_nodes_per_leg")
    created_nodes_sim = create_interpolated_nodes(
        sim_info, nodes_per_leg=sim_nodes_per_leg, clean=False)
    sight = extract_settings(mysql, called="sight")
    contact_points = find_contact(created_nodes, created_nodes_sim, sight)
    # user run settings
    # ----------------------------------------
    if request.method == 'POST':
        selected_run_mode = request.form
        run_mode = selected_run_mode["run_option"]
        if run_mode == 'reset' or run_mode == 'debug':
            iter_val = 1
            save_settings(mysql, "iter", iter_val)
        elif run_mode == 'iterate':
            iter_val += 1
            save_settings(mysql, "iter", iter_val)
        # main src loop
        # ----------------------------------------
        iter_val = extract_settings(mysql, "iter")
        results_package = main_path_optimizer(
            created_nodes, contact_points, created_nodes_sim, sight, original_nodes, iter_val=iter_val)
        package_results(mysql, results_package)  # inserts results into db
        # plot 3d results
        # ----------------------------------------
        if not run_mode == 'debug':
            created_nodes = extract_results(
                mysql, created_nodes, 'node', iter_val)
            contact_points = extract_results(
                mysql, contact_points, 'contact', iter_val)
            make_progress_plot(geo_info, sim_info, flights,
                               created_nodes, created_nodes_sim, contact_points)
    iter_val = extract_settings(mysql, "iter")
    return render_template('progress.html', iter_val=iter_val)


@app.route('/results', methods=['GET', 'POST'])
def results():
    # initialization
    # ----------------------------------------
    selection_geo = extract_settings(mysql, called="geo_selected")
    selection_sim = extract_settings(mysql, called="sim_selected")
    print('We are using ' + selection_geo + ' as our geo for 3dplot.')
    print('We are using ' + selection_sim + ' as our sim for 3d plot.')
    geo_info, _, flights = get_geo_info(mysql, selection_geo)
    sim_info, _ = get_sim_info(mysql, selection_sim)
    flights, sim_info = append_endpoints([flights, sim_info], geo_info)
    created_nodes = create_interpolated_nodes(flights)
    created_nodes_sim = create_interpolated_nodes(
        sim_info, nodes_per_leg=100, clean=False)
    sight = extract_settings(mysql, called="sight")
    contact_points = find_contact(created_nodes, created_nodes_sim, sight)
    # extract data
    # ----------------------------------------
    all_plot_divs = []
    iter_val = extract_settings(mysql, "iter")
    for i in range(1, iter_val + 1):
        created_nodes = extract_results(mysql, created_nodes, 'node', i)
        contact_points = extract_results(
            mysql, contact_points, 'contact', i)
        all_plot_divs.append(make_results_plot(
            geo_info, created_nodes, contact_points, i))
    return render_template('results.html', all_plot_divs=all_plot_divs)
