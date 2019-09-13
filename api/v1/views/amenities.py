#!/usr/bin/python3
'''Creates amenities route and returns valid JSON'''
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities_route():
    '''Returns a JSON of an amenity object'''
    if request.method == 'GET':
        amenities = storage.all('Amenity').values()
        amenity_list = []
        for amenity in amenities:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)

    if request.method == 'POST':
        new_amenity = request.get_json()
        if new_amenity is None:
            abort(400, 'Not  a JSON')
        if "name" not in new_amenity:
            abort(400, 'Missing name')
        new_amenity_obj = Amenity(**new_amenity)
        new_amenity_obj.save()
        return jsonify(new_amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id_route(amenity_id):
    '''Retrieves an Amenity object'''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        amenity_update = request.get_json()
        if amenity_update is None:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, val in amenity_update.items():
            if key not in ignore_keys:
                setattr(amenity, key, val)
                amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
