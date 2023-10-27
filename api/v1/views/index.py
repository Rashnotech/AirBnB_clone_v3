#!/usr/bin/python3
""" an app view module """
from api.v1.views import app_views, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# list of classes
classes = {'amenities': Amenity, 'cities': City,
            'reviews': Review, 'states': State,
            'users': User}

@app_views.route('/status')
def status():
    """ a function returns status"""
    return jsonify({'status': 'OK'}), 200

@app_views.route('/stats')
def stats():
    """ a function that return stats"""
    statistics = {}
    for key, value in classes.items():
        statistics[key] = storage.count(value)
    return jsonify(statistics), 200, {'Content-Type': 'application/json'}
