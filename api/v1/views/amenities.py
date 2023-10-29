#!/usr/bin/python3
""" a module that view amenity """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views, jsonify, request, abort


@app_views.route('/amenities', methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_list(amenity_id=None):
    """ a function that list amenities """
    if amenity_id is None and request.method == 'GET':
        amenities = storage.all(Amenity)
        amenity_list = [amenity.to_dict() for amenity in amenities.values()]
        return jsonify(amenity_list), 200
    elif request.method == 'POST' and amenity_id is None:
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        amenity = storage.get(Amenity, amenity_id)
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
                    setattr(state, attr, value)
            storage.save()
            return jsonify(state.to_dict()), 200

        if request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
