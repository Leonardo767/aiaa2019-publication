from flask import Flask
app = Flask(__name__)


@app.route('/')
def primaryEndpoint():


return "/ GET Endpoint"

app.run()
