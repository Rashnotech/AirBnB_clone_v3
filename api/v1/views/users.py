#!/usr/bin/python3
from api.v1.views import app_views, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users_list():
    """Retrieve the list of user """
    if request.method == 'GET':
        users = storage.all(User)
        user_list = [user.to_dict() for user in users.values()]
        return jsonify(user_list), 200
    
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if data.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        if data.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201



@app_views.route('/users/<user_id>', methods=['DELETE', 'PUT', 'GET'], strict_slashes=False)
def user(user_id=None):
    """ Handles operation"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(users.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in data.items():
            if key != 'id' and key != 'email' and key != 'created_at' and key != 'updated_at':
                setattr(users, key, value)
        storage.save()
        return jsonify(users.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(users)
        storage.save()
        return jsonify({}), 200

