#!/usr/bin/python3
""" Module of initialization with the route(/status and /stats) to
show the status of the application web and some stats that retrieves
the number of each objects by type"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ This function return the response with the
    JSON representation """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def number_of_objects():
    """ This function returns of the number of objects by each class """
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review
    dicc_class = {
               'users': storage.count(User),
               'places': storage.count(Place),
               'states': storage.count(State),
               'cities': storage.count(City),
               'amenities': storage.count(Amenity),
               'reviews': storage.count(Review)
              }
    return jsonify(dicc_class)
