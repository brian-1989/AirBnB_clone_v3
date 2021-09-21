#!/usr/bin/python3
""" Module that represent the view for Review objects """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.app import show_error


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews_of_place(place_id=None):
    """ this function retrieves the list of all reviews objects
        belonging to a specific place_id """
    if request.method == 'GET':
        _places = storage.get(Place, place_id)
        if _places is not None:
            list_reviews = list()
            for city in _places.reviews:
                list_reviews.append(city.to_dict())
            return jsonify(list_reviews)
        abort(404)
    if request.method == 'POST':
        _places = storage.get(Place, place_id)
        if _places is None:
            abort(404)
        conv_body = request.get_json()
        if not conv_body:
            abort(400, description="Not a JSON")
        if 'user_id' not in conv_body:
            return "Missing user_id\n", 400
        _user = storage.get(User, conv_body.get('user_id'))
        if _user is None:
            abort(404)
        if 'name' not in conv_body:
            return "Missing name\n", 400
        conv_body['place_id'] = _places.id
        new_inst = Review(**conv_body)
        storage.new(new_inst)
        storage.save()
        return jsonify(new_inst.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_reviews(review_id=None):
    """ this function retrieves the list of all Review objects """
    if request.method == 'GET':
        _review = storage.get(Review, review_id)
        if _review is None:
            abort(404)
        return jsonify(_review.to_dict())
    if request.method == 'DELETE':
        obj_review = storage.get(Review, review_id)
        if obj_review:
            storage.delete(obj_review)
            storage.save()
            return jsonify(dict()), 200
        abort(404)
    if request.method == 'PUT':
        new_inst = storage.get(Review, review_id)
        if not new_inst:
            abort(404)
        try:
            list_ignore = [
                'id', 'created_at', 'updated_at', 'user_id', 'place_id']
            conv_body = request.get_json()
            for key, value in conv_body.items():
                if key not in list_ignore:
                    setattr(new_inst, key, value)
            new_inst.save()
            return jsonify(new_inst.to_dict()), 200
        except:
            abort(400, description="Not a JSON")
