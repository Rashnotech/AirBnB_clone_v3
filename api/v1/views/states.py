#!/usr/bin/python3
""" a module that retrieves states """
from api.v1.views import app_views, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def state_list(state_id=None):
    """ a function that list all states"""
    if state_id is None and request.method == 'GET':
        states = storage.all(State)
        state_list = [state.to_dict() for state in states.values()]
        return jsonify(state_list), 200

    if request.method == 'POST' and state_id is None:
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        if request.method == 'GET':
            return jsonify(state.to_dict())

        if request.method == 'PUT':
            data = request.get_json()
            if data is None:
                abort(400, 'Not a JSON')
            for key, value in data.items():
                if key != 'id' and key != 'created_at' and key != 'updated-at':
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200
