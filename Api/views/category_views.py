from flask import request

from ..api import app
from ..error_handlers import *
from ..auth_handlers import decode_auth_token, invalid_token, invalid_key_data
from Api.contollers.categories import Category


@app.route('/category', methods=['POST'])
def add_category():
    """Method to handle creating a category of a recipe"""
    request.get_json(force=True)
    try:
        user_id = decode_auth_token(request.headers.get("Authorization"))
        if isinstance(user_id, int):
            name = request.json['name']
            parent_id = request.json.get('parent_id')
            category = Category()
            response = category.create_category(
                name, parent_id)
            return response

        return invalid_token()

    except KeyError:
        return invalid_key_data()


@app.route('/categories', methods=['GET'])
def get_categories():
    """Method to handle getting all recipe categories"""
    user_id = int(decode_auth_token(request.headers.get("Authorization")))

    if isinstance(user_id, int):
        limit = request.args.get('limit', 5, int)
        search = request.args.get("q", "")

        category = Category()
        if limit:
            limit = int(limit)
            response = category.get_categories(search, limit)
            return response
        response = category.get_categories(search, limit)
        return response

    else:
        return invalid_token()


@app.route('/categories/<int:id>', methods=['GET'])
def get_a_category(id):
    """Method to handle get a single category"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        category = Category()
        response = category.get_single_category(id)
        return response

    else:
        return invalid_token()


@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_a_category(id):
    """Method to handle delete a single category"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        category = Category()
        response = category.delete_category(id)
        return response

    else:
        return invalid_token()


@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    """Method to handle update a user"""
    try:
        data = request.get_json() or {}
        category = Category()
        response = category.update_category(id, data)
        return response

    except KeyError:
        return ({"Error": "An issue with the key"})
