#!/usr/bin/python3
""" Module that represent the view for City objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'],
                 strict_slashes=False)
def all_city_of_state(state_id=None):
    """ this function retrieves the list of all cities objects
        belonging to a specific state_id """
    if request.method == 'GET':
        _states = storage.get(State, state_id)
        if _states is not None:
            list_cities = list()
            for city in _states.cities:
                list_cities.append(city.to_dict())
            return jsonify(list_cities[0])
        abort(404)
    if request.method == 'POST':
        _states = storage.get(State, state_id)
        if _states is None:
            abort(404)
        try:
            conv_body = request.get_json()
            if 'name' not in conv_body:
                return "Missing name\n", 400
            new_inst = City(name=conv_body.get('name'))
            new_inst.state_id = _states.id
            storage.new(new_inst)
            storage.save()
            return jsonify(new_inst.to_dict()), 201
        except:
            abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_cities(city_id=None):
    """ this function retrieves the list of all City objects """
    if request.method == 'GET':
        _cities = storage.get(City, city_id)
        if _cities is None:
            abort(404)
        return jsonify(_cities.to_dict())
    if request.method == 'DELETE':
        obj_city = storage.get(City, city_id)
        if obj_city:
            storage.delete(obj_city)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'PUT':
        new_inst = storage.get(City, city_id)
        if not new_inst:
            abort(404)
        try:
            list_ignore = ['id', 'created_at', 'updated_at']
            conv_body = request.get_json()
            for key, value in conv_body.items():
                if key not in list_ignore:
                    setattr(new_inst, key, value)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 200
        except:
            abort(400, description="Not a JSON")
