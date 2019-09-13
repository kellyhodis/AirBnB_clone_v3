#!/usr/bin/python3
""" This is a module that defines the users view
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, jsonify, make_response, abort


@app_views.route('/users', methods=['GET', 'POST'])
def users_route():
    '''Returns a JSON of a user object'''
    if request.method == 'GET':
        users = storage.all('User').values()
        user_list = []
        for user in users:
            user_list.append(user.to_dict())
        return jsonify(user_list)
    if request.method == 'POST':
        new_user = request.get_json()
        if new_user is None:
            abort(400, {"Not a JSON"})
        if "email" not in new_user:
            abort(400, {"Missing email"})
        if "password" not in new_user:
            abort(400, {"Missing password"})
        new_user_obj = User(**new_user)
        new_user_obj.save()
        return jsonify(new_user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_id_route(user_id):
    '''Retrieves a user object'''
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        user_update = request.get_json()
        if user_update is None:
            abort(400, {"Not a JSON"})
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, val in user_update.items():
            if key not in ignore_keys:
                setattr(user, key, val)
                user.save()
        return make_response(jsonify(user.to_dict()), 200)
