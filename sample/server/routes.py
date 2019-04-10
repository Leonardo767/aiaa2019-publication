from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.objects import Geo
from server.lib.dbUtils import input2db


@app.route('/', methods=['GET', 'POST'])
@app.route('/input_environment', methods=['GET', 'POST'])
def input_environment():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Geo")
    if resultValue > 0:
        GeoData = cur.fetchall()
    cur.close()

    return render_template('input_environment.html', GeoData=GeoData)


@app.route('/input_environment_select', methods=['GET', 'POST'])
def input_environment_select():
    # form fetch only gives selected geo, draw from database if it exists
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Geo")
    if resultValue > 0:
        GeoData = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        # fetch form data (selection)
        selectionInput = request.form
        print(selectionInput["geo_selected"] + ' is selected.')
        return redirect(url_for('input_environment'))
    return render_template('input_environment_select.html', GeoData=GeoData)


@app.route('/input_environment_create', methods=['GET', 'POST'])
def input_environment_create():
    # form fetch creates a new database entry (must be complete), and is selected
    if request.method == 'POST':
        # fetch form data (creation)
        newGeoDataInput = request.form
        input2db(newGeoDataInput, mysql)
        return redirect(url_for('input_environment'))
    return render_template('input_environment_create.html')


@app.route('/input_sim', methods=['GET', 'POST'])
def input_sim():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('input_sim.html')


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'POST':
        # fetch form data
        pass
    return render_template('execute.html')


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
