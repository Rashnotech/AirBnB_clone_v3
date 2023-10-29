#!/usr/bin/python3
""" a module that retrieves states """
from api.v1.views import app_views, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def place_list(city_id=None):
    """Retrieve and create places"""
    if city_id is None and request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        place_list = [place.to_dict() for place in city.places]
        return jsonify(place_list), 200

    if request.method == 'POST' and city_id is None:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if data.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif data.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        users = storage.get(User, data.get('user_id'))
        if users is None:
            abort(404)
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
        return jsonify(places.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key != 'id' and key != 'user_id' and key != 'city_id' and key != 'created_at' and key != 'updated_at':
                setattr(places, key, value)
        storage.save()
        return jsonify(places.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(places)
        storage.save()
        return jsonify({}), 200
