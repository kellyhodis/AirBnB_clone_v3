#!/usr/bin/python3
'''Creates places route and returns valid JSON'''
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def cities_places_route(city_id):
    '''Returns a JSON of a place object'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)

    if request.method == 'POST':
        new_place = request.get_json()
        if not new_place:
            abort(400, 'Not a JSON')
        if "name" not in new_place:
            abort(400, 'Missing name')
        new_place['city_id'] = city_id
        new_place_obj = Place(**new_place)
        new_place_obj.save()
        return jsonify(new_place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_route(place_id):
    '''Retrieves places within the city object'''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        '''GET retrieves from the db a specific place by id'''
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        '''DELETE removes from db the specific city object'''
        storage.delete(place)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        '''PUT updates the city object with name of the city changed'''
        place_update = request.get_json()
        if place_update is None:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in place_update.items():
            if key not in ignore_keys:
                setattr(place, key, value)
                place.save()
        return make_response(jsonify(place.to_dict()), 200)
