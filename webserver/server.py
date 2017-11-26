
import os
from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
import backend
from json import dumps

app = Flask(__name__, static_url_path="")
CORS(app)

@app.before_first_request
def activate_job():
    backend.start_collector()

@app.route("/")
def index():
    return render_template("index.html", stops=backend.get_stop_names())

@app.route("/semantic/<path:path>")
def send_file(path):
    return send_from_directory("semantic/", path)

@app.route("/js/script.js")
def send_script():
    return send_from_directory("js/", "script.js")

@app.route("/gps")
def nearest_stop():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    return backend.find_closest_stop(lat, lon)

@app.route("/getdata/<string:stop>")
def get_data(stop):
    results = backend.get_latest(stop)
    return dumps(results)

@app.route("/gettop/<string:stop>/<string:route>/")
def get_top_n(stop, route):
    results = backend.get_top(stop, route, 400)
    return dumps(results)

@app.route("/getcolors")
def get_colors():
    results = backend.get_colors()
    return dumps(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

def get_app():
    return app