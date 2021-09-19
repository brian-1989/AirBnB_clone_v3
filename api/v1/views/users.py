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
    if request.method == 'GET':
        if user_id is None:
            _users = storage.all(User).values()
            list_users = list()
            for user in _users:
                list_users.append(user.to_dict())
            return jsonify(list_users)
        else:
            _user = storage.get(User, user_id)
            if _user is None:
                abort(404)
            return jsonify(_user.to_dict())
    if request.method == 'DELETE':
        obj_user = storage.get(User, user_id)
        if obj_user:
            storage.delete(obj_user)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'POST':
        try:
            conv_body = request.get_json()
            if 'email' not in conv_body:
                return "Missing email\n", 400
            if 'password' not in conv_body:
                return "Missing password\n", 400
            new_inst = User(email=conv_body.get(
                'email'), password=conv_body.get('password'))
            storage.new(new_inst)
            storage.save()
            return jsonify(new_inst.to_dict()), 201
        except:
            abort(400, description="Not a JSON")
    if request.method == 'PUT':
        new_inst = storage.get(User, user_id)
        if not new_inst:
            abort(404)
        try:
            list_ignore = ['id', 'created_at', 'updated_at', 'email']
            conv_body = request.get_json()
            for key, value in conv_body.items():
                if key not in list_ignore:
                    setattr(new_inst, key, value)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 200
        except:
            abort(400, description="Not a JSON")
