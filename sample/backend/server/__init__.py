from flask import Flask
app = Flask(__name__)
app.config['SECRET KEY'] = 'b2e7a328a524163dfb96a7a8a3b6c15a'

from server import routes
