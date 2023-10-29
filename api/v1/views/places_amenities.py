#!/usr/bin/python3
""" a module that create a new view between objects"""
from models import storage
from models import place
from models import amenity
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<id>/amenities', methods=['GET'], strict_slashes=False)
def view_amenities(id=None):
    """a function that view objects"""
    places = storage.get(Place, id)
    if places is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities
                      for place in places.values()]
    return jsonify(amenities_list), 200


@app_views.route('places/<pid>/amenities/<aid>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenities(pid=None, aid=None):
    """a function that view objects"""
    places = storage.get(Place, pid)
    amenities = storage.get(Amenity, aid)
    if places is None and amenities is None:
        abort(404)
    for place in places.values():
        for amenity in place.amenities:
            if aid == amenity.id:
                storage.delete(amenity)
            else:
                abort(404)
    return jsonify({}), 200


@app_views.route('places/<pid>/amenities/<aid>', methods=['POST'],
                 strict_slashes=False)
def post_amenities(pid=None, aid=None):
    """a function that view objects"""
    if pid is None and aid is None:
        abort(404)
    amenities = storage.get(Amenity, aid)
    places = storage.get(Place, pid)
    if places is None:
        abort(404)
    return jsonify(amenities_list), 201


