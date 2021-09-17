#!/usr/bin/python3
""" Module that represents the main application """

from threading import Thread
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

HOST = getenv('HBNB_API_HOST')
PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def reset_session(exception):
    """ This function use the handler teardown_appcontext to
        close or otherwise deallocates the resource if it exists """
    storage.close()


if __name__ == "__main__":
    if HOST:
        _host = HOST
    else:
        _host = "0.0.0.0"
    if PORT:
        _port = PORT
    else:
        _port = "5000"
    app.run(host=_host, port=_port, debug=True, threaded=True)
