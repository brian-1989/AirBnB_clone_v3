#!/usr/bin/python3
""" Module of initialization with the route(/status) to
show the status of the application web """

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """ This function return the response with the
    JSON representation """
    return jsonify({"status": "OK"})
