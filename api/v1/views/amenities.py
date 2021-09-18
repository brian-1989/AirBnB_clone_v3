#!/usr/bin/python3
""" Module that represent the view for Amenity objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_amenity(amenity_id=None):
    """ this function retrieves the list of all amenities objects """
    if request.method == 'GET':
        if amenity_id is None:
            _amenities = storage.all(Amenity).values()
            list_amenities = list()
            for amenity in _amenities:
                list_amenities.append(amenity.to_dict())
            return jsonify(list_amenities)
        else:
            _amenities = storage.get(Amenity, amenity_id)
            if _amenities is None:
                abort(404)
            return jsonify(_amenities.to_dict())
    if request.method == 'DELETE':
        obj_amenity = storage.get(Amenity, amenity_id)
        if obj_amenity:
            storage.delete(obj_amenity)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'POST':
        try:
            conv_body = request.get_json()
            if 'name' not in conv_body:
                return "Missing name\n", 400
            new_inst = Amenity(name=conv_body.get('name'))
            storage.new(new_inst)
            storage.save()
            return jsonify(new_inst.to_dict()), 201
        except:
            abort(400, description="Not a JSON")
    if request.method == 'PUT':
        new_inst = storage.get(Amenity, amenity_id)
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
