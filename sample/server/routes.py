from flask import render_template, url_for, flash, redirect
from server import app
from server.createPath import Geo


@app.route('/', methods=['GET', 'POST'])
def input():
    return render_template('input.html')
