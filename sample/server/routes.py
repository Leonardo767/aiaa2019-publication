from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.objects import Geo


@app.route('/', methods=['GET', 'POST'])
@app.route('/input_environment', methods=['GET', 'POST'])
def input_environment():
    if request.method == 'POST':
        # fetch form data
        GeoData = request.form
        name = GeoData['GeoName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Geo(GeoName) VALUES(%s)", [name])
        mysql.connection.commit()
        cur.close()
    return render_template('input_environment.html')


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
