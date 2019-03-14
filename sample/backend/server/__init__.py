from flask import Flask
from flask.ext.pymongo import pymongo

app = Flask(__name__)
app.config['SECRET KEY'] = 'b2e7a328a524163dfb96a7a8a3b6c15a'
app.config['MONGO_DBNAME'] = 'dummy'
app.config['MONGO_URI'] = 'dummy'

from server import routes
