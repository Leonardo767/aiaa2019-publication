from flask import Flask
from flask_mysqldb import MySQL
import yaml

# NOTE: yaml file is pulled outside of app directory to obscure sensitive information
# to use your own database, please modify app.open_resources() path to your own yaml file containing the keys called here

# NOTE: specifically for this __init__.py file, save file without auto-formatting
# on VSCode, the keyboard command to save without auto-formatting is: "Ctrl + K", and then "Ctrl + Shift + S"

app = Flask(__name__)
with app.open_resource('../../../YAML/aiaa_2019_sensitive.yaml') as f:  # path is unique to local machine
    sensitive_info = yaml.safe_load(f)
app.config['MYSQL_HOST'] = sensitive_info['mysql_host']
app.config['MYSQL_USER'] = sensitive_info['mysql_user']
app.config['MYSQL_PASSWORD'] = sensitive_info['mysql_password']
app.config['MYSQL_DB'] = sensitive_info['mysql_db']

app.config['SECRET KEY'] = sensitive_info['secret_key']

mysql = MySQL(app)

from server import routes
