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
    if request.method == 'GET':
        _cities = storage.get(City, city_id)
        if _cities is not None:
            list_places = list()
            for city in _cities.places:
                list_places.append(city.to_dict())
            return jsonify(list_places)
        abort(404)
    if request.method == 'POST':
        _cities = storage.get(City, city_id)
        if _cities is None:
            abort(404)
        conv_body = request.get_json()
        if not conv_body:
            abort(404, description="Not a JSON")
        if 'user_id' not in conv_body:
                return "Missing user_id\n", 400
        _user = storage.get(User, conv_body.get('user_id'))
        if _user is None:
                abort(404)
        if 'name' not in conv_body:
            return "Missing name\n", 400
        new_inst = Place(**conv_body, city_id=_cities.id)
        storage.new(new_inst)
        storage.save()
        return jsonify(new_inst.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_places(place_id=None):
    """ this function retrieves the list of all Place objects """
    if request.method == 'GET':
        _place = storage.get(Place, place_id)
        if _place is None:
            abort(404)
        return jsonify(_place.to_dict())
    if request.method == 'DELETE':
        obj_place = storage.get(Place, place_id)
        if obj_place:
            storage.delete(obj_place)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'PUT':
        new_inst = storage.get(Place, place_id)
        if not new_inst:
            abort(404)
        try:
            list_ignore = [
                'id', 'created_at', 'updated_at', 'user_id', 'city_id']
            conv_body = request.get_json()
            for key, value in conv_body.items():
                if key not in list_ignore:
                    setattr(new_inst, key, value)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 200
        except:
            abort(400, description="Not a JSON")
