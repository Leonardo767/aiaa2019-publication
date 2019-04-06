from flask import render_template, url_for, flash, redirect, request
from flask_mysqldb import MySQL
from server import app, mysql
from server.lib.objects import Geo


@app.route('/', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        # fetch form data
        GeoData = request.form
        name = GeoData['GeoName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Geo(GeoName) VALUES(%s)", [name])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('database'))
    return render_template('input.html')


@app.route('/database')
def database():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Geo")
    if resultValue > 0:
        GeoData = cur.fetchall()
        return render_template('database.html', GeoData=GeoData)
