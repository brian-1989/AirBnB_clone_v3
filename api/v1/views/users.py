#!/usr/bin/python3
""" Module that represent the view for User objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_users(user_id=None):
    """ this function retrieves the list of all users objects """
