from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.objects import Geo
from server.lib.dbUtils import informSelection, input2db_geo, save_settings, extract_selection, get_geo_info
from server.lib.executePlotter import make_geo_plot


@app.route('/', methods=['GET', 'POST'])
@app.route('/input_environment', methods=['GET', 'POST'])
def input_environment():
    return render_template('input_environment.html')


@app.route('/input_environment_select', methods=['GET', 'POST'])
def input_environment_select():
    EntryData, AirportData, GeoData, Airports, Entries = informSelection(mysql)
    if request.method == 'POST':
        # fetch the form data (taking the form of a selection)
        selectionInput = request.form
        save_settings(mysql, "geo_selected",
                      selectionInput["geo_selected"])
        print(selectionInput["geo_selected"] + ' is selected.')
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
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('input_sim_select.html')


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
        pass
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
        # save plot and exit
        return redirect(url_for('execute'))
    selection = extract_selection(mysql, called="geo_selected")
    print('We are using ' + selection + ' as our geo.')
    geo_info, airport_info = get_geo_info(mysql, selection)
    geo_plot = make_geo_plot(geo_info, airport_info)  # pass in database
    return render_template('execute_plot.html', geo_plot=geo_plot)


@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('progress.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('results.html')
