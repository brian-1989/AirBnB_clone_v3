#!/usr/bin/python3
""" Module that represent the view for Review objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews_of_place(place_id=None):
    """ this function retrieves the list of all reviews objects
        belonging to a specific place_id """


# Con el método POST: hacer lo mismo que hicimos en cities.py (líneas 25, 26, 27 y 33) con Place y con User
# (pues tiene llaves foraneas de cada tabla: place_id y user_id)

@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_reviews(review_id=None):
    """ this function retrieves the list of all Review objects """
