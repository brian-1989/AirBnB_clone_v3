#!/usr/bin/python3
""" Module that represent the view for Place objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places_of_city(city_id=None):
    """ this function retrieves the list of all places objects
        belonging to a specific city_id """


# En POST: hacer lo mismo que hicimos en cities.py (líneas 25, 26, 27 y 33) con City y con User
# (pues tiene llaves foraneas de cada tabla: city_id y user_id)

@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_places(place_id=None):
    """ this function retrieves the list of all Place objects """
