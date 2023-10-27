#!/usr/bin/python3
""" a module that retrieves states """
from api.v1.views import app_views, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def state_list(state_id=None):
    """ a function that list all states"""
    if state_id is None:
        states = storage.all(State)
        state_list = [state.to_dict() for state in states.values()]
        return jsonify(state_list), 200
    else:
        state = storage.get(State, state_id)
        if state is None:
            return jsonify({'error': 'Not found'}), 404

        if request.method == 'GET':
            return jsonify(state.to_dict())
        
        if request.method == 'DELETE':
            storage.delete(state.to_dict())
            storage.save()
            return jsonify({}), 200

        if request.method == 'POST':
            data = request.get_json()
            if data is None:
                return jsonify({'error': 'Not a JSON'}), 400
            elif data.get('name') is None:
                return jsonify({'error': 'Missing name'}), 400
            storage.new(**data)
            storage.save()
            return jsonify(data.to_dict()), 201
        
        if request.method == 'PUT':
            data = request.get_json()
            if data is None:
                return jsonify({'error': 'Not a JSON'}), 400
            for key, value in data.items():
                if key != 'id' and key != 'created_at' and key != 'updated-at':
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200

                
