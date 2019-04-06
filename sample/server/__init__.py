from flask import Flask
from flask_mysqldb import MySQL
import yaml

# NOTE: yaml file is pulled outside of app directory to obscure sensitive information
# to use your own database, please modify open_resources() path to your own yaml file containing the keys called here

app = Flask(__name__)
with app.open_resource('../../../YAML/aiaa_2019_sensitive.yaml') as f:
    sensitive_info = yaml.safe_load(f)
app.config['MYSQL_HOST'] = sensitive_info['mysql_host']
app.config['MYSQL_USER'] = sensitive_info['mysql_user']
app.config['MYSQL_PASSWORD'] = sensitive_info['mysql_password']
app.config['MYSQL_DB'] = sensitive_info['mysql_db']

app.config['SECRET KEY'] = sensitive_info['secret_key']

mysql = MySQL(app)

from server import routes
