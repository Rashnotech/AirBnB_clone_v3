#!/usr/bin/python3
""" a module that handles all default RESTFul API actions"""
from models import storage
from models.review import Review
from api.v1.views import app_views, jsonify, request, abort
from models.place import Place
from models.user import User


@app_views.route('/places/<pid>/reviews', methods=['GET', 'POST'])
def list_reviews(pid=None):
    """Transform review"""
    place = storage.get(Place, pid)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = [reviews.to_dict() for reviews in place.reviews]
        return jsonify(reviews), 200
    if request.method == 'POST':
        # Create a new review
        data = request.get_json()
        if data is None:
            abort(404, 'Not a JSON')
        user = storage.get(User, data.get('user_id'))
        if user is None:
            abort(404)
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if data.get('text') is None:
            abort(400, 'Missing text')
        new_review = Review(**data)
        new_review.place_id = place.id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<rid>', methods=['DELETE', 'PUT', 'GET'])
def do_reviews(rid=None):
    """ Transform reviews """
    review = storage.get(Review, rid)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        match = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, val in data.items():
            if key not in match:
                setattr(review, key, val)
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
