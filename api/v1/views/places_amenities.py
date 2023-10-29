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
    """View a list of amenities associated with a Place"""
    places = storage.get(Place, id)
    if places is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list), 200


@app_views.route('places/<pid>/amenities/<aid>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenities(pid=None, aid=None):
    """Delete an amenity object from a place"""
    place = storage.get(Place, pid)
    amenity = storage.get(Amenity, aid)
    if place is None or amenity is None:
        abort(404)
    # Amenity is not linked to the place, raise a 404 error
    if amenity not in places.amenities:
        abort(404)
    # Delete the amenity from the place's amenities
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<pid>/amenities/<aid>', methods=['POST'],
                 strict_slashes=False)
def post_amenities(pid=None, aid=None):
    """Link an amenity object to a place"""
    if pid is None and aid is None:
        abort(404)
    amenity = storage.get(Amenity, aid)
    place = storage.get(Place, pid)
    if place is None or amenity is None:
        abort(404)
    # The amenity is already linked to the place
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    # Link the amenity to the place
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenities_list), 201
