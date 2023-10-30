#!/usr/bin/python3
""" a module that handles all default RESTFul API actions"""
from api.v1.views import app_views, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_list(city_id=None):
    """Retrieve and create places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        place_list = [place.to_dict() for place in city.places]
        return jsonify(place_list), 200

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('user_id') is None:
            abort(400, 'Missing user_id')
        users = storage.get(User, data.get('user_id'))
        if users is None:
            abort(404)
        if data.get('name') is None:
            abort(400, 'Missing name')
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def place(place_id=None):
    """ a function that list all states"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        match = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in match:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
