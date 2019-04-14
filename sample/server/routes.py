from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.objects import Geo
from server.lib.dbUtils import (informGeoSelection, informSimSelection,
                                input2db_geo, save_settings, extract_selection, get_geo_info, get_sim_info)
from server.lib.executePlotter import make_geo_plot
from server.lib.progressPlotter import make_progress_plot


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
    all_settings = extract_selection(mysql, "geo_selected", all_settings=True)
    return render_template('execute_settings.html', all_settings=all_settings)


@app.route('/execute_plot', methods=['GET', 'POST'])
def execute_plot():
    if request.method == 'POST':
        # acknowledge plot and exit
        return redirect(url_for('execute'))
    selection_geo = extract_selection(mysql, called="geo_selected")
    selection_sim = extract_selection(mysql, called="sim_selected")
    print('We are using ' + selection_geo + ' as our geo.')
    print('We are using ' + selection_sim + ' as our sim.')
    geo_info, airport_info, flights = get_geo_info(mysql, selection_geo)
    sim_info, sim_info_style = get_sim_info(mysql, selection_sim)
    geo_plot = make_geo_plot(geo_info, airport_info, flights,
                             sim_info, sim_info_style)  # pass in plotting info
    return render_template('execute_plot.html', geo_plot=geo_plot)


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    progress_plot = make_progress_plot()
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('progress.html', progress_plot=progress_plot)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('results.html')
