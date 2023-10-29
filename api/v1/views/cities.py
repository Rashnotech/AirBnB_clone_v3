#!/usr/bin/python3
"""a module that handles all RESTFUL API actions """
from api.v1.views import app_views, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<sid>/cities', methods=['GET', 'POST'], strict_slashes=False)
def show_statelist(sid=None):
    """Retrieves the list of all city in state object"""
    state = storage.get(State, sid)
    if state is None:
        abort(404)
    if request.method == 'GET':
        city_list = [city.to_dict() for city in state.cities]
        return jsonify(city_list), 200

    # create a city
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        new_city = City(**data)
        new_city.state_id = sid
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<cid>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def city_list(cid=None):
    """Retrieves the list of searched city """
    city = storage.get(City, cid)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict()), 200

    # updates a city object
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        match = ['id', 'state_id', 'created_at', 'updated_at']
        for key, val in data.items():
            if key not in match:
                setattr(city, key, val)
        storage.save()
        return (city.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
