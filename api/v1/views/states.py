#!/usr/bin/python3
""" Module that represent the view for State objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_states(state_id=None):
    """ this function retrieves the list of all State objects """
    if request.method == 'GET':
        _states = storage.all(State).values()
        if state_id is None:
            list_states = list()
            for state in _states:
                list_states.append(state.to_dict())
            return jsonify(list_states)
        else:
            list_states = list()
            for state in _states:
                if state.id == state_id:
                    list_states.append(state.to_dict())
                    return jsonify(list_states[0])
            abort(404)
    if request.method == 'DELETE':
        obj_state = storage.get(State, state_id)
        if obj_state:
            storage.delete(obj_state)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'POST':
        conv_body = request.get_json()
        if 'name' not in conv_body:
            abort(400, description="Missing name")
        try:
            new_inst = State(name=conv_body['name'])
            storage.new(new_inst)
            storage.save()
            return jsonify(new_inst.to_dict()), 201
        except Exception:
            abort(400, description="Not a JSON")
    if request.method == 'PUT':
        new_inst = storage.get(State, state_id)
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
        except Exception:
            abort(400, description="Not a JSON")
