#!/usr/bin/python3
""" Module that represents the main application """

from flask import Flask, jsonify
from flask.helpers import make_response
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def reset_session(exception):
    """ This function use the handler teardown_appcontext to
        close or otherwise deallocates the resource if it exists """
    storage.close()


@app.errorhandler(404)
def show_error(error):
    """ This function is a handler for 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')
    if HOST:
        _host = HOST
    else:
        _host = "0.0.0.0"
    if PORT:
        _port = PORT
    else:
        _port = "5000"
    app.run(host=_host, port=_port, debug=True, threaded=True)
