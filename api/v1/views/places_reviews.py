#!/usr/bin/python3
'''Creates places route and returns valid JSON'''
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def places_reviews_route(place_id):
    '''Returns a JSON of a review object'''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)

    if request.method == 'POST':
        new_review = request.get_json()
        if not new_review:
            abort(400, 'Not a JSON')
        if "user_id" not in new_review:
            abort(400, 'Missing user_id')
        if "text" not in new_review:
            abort(400, 'Missing text')
        check_user = storage.get("User", new_review['user_id'])
        if not check_user:
            abort(404)
        new_review['place_id'] = place_id
        new_review_obj = Place(**new_review)
        new_review_obj.save()
        return jsonify(new_review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_route(review_id):
    '''Retrieves review within the place object'''
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        '''GET retrieves from the db a specific place by id'''
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        '''DELETE removes from db the specific city object'''
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        '''PUT updates the city object with name of the city changed'''
        review_update = request.get_json()
        if review_update is None:
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        for key, value in review_update.items():
            if key not in ignore_keys:
                setattr(review, key, value)
                review.save()
        return make_response(jsonify(review.to_dict()), 200)
