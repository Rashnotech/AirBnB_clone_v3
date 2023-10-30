#!/usr/bin/python3
""" a module that view amenity """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views, jsonify, request, abort


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities_list():
    """ a function that list amenities """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenity_list = [amenity.to_dict() for amenity in amenities.values()]
        return jsonify(amenity_list), 200
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<aid>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def update_amenities(aid=None):
    amenity = storage.get(Amenity, aid)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        match = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in match:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
