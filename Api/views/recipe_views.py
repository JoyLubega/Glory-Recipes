from flask import request

from ..api import app
from ..error_handlers import *
from ..auth_handlers import decode_auth_token, invalid_token, invalid_key_data
from Api.contollers.recipes import Recipe


@app.route('/categories/<int:category_id>/recipe', methods=['POST'])
def add_recipe(category_id):
    """Method to handle creating a recipe"""
    request.get_json(force=True)
    try:
        user_id = decode_auth_token(request.headers.get("Authorization"))
        if isinstance(user_id, int):
            name_of_recipe = request.json['name_of_recipe']
            recipe_text = request.json.get('recipe_text')
            recipe = Recipe()
            response = recipe.add_recipe(user_id, category_id,
                                         recipe_text, name_of_recipe)
            return response

        return invalid_token()

    except KeyError:
        return invalid_key_data()


@app.route('/categories/<int:category_id>/recipes', methods=['GET'])
def get_recipes(category_id):
    """Method to handle getting all recipe"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        limit = request.args.get('limit', 5, int)
        search = request.args.get("q", "")

        recipe = Recipe()
        if limit:
            limit = int(limit)
            response = recipe.get_recipes(search, limit, category_id)
            return response
        response = recipe.get_recipes(search, limit, category_id)
        return response

    else:
        return invalid_token()


@app.route(
    '/categories/<int:category_id>/recipes/<int:recipe_id>', methods=['GET'])
def get_a_recipe(category_id, recipe_id):
    """Method to handle get a single recipe"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        recipe = Recipe()
        response = recipe.get_single_recipe(recipe_id, category_id)
        return response

    else:
        return invalid_token()


@app.route(
    '/<int:category_id>/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_a_recipe(category_id, recipe_id):
    """Method to handle delete permanently a single recipe"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        recipe = Recipe()
        response = recipe.delete_recipe(category_id, recipe_id)
        return response

    else:
        return invalid_token()


@app.route(
    '/categories/<int:category_id>/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(category_id, recipe_id):
    """Method to handle update a single recipe"""
    user_id = decode_auth_token(request.headers.get("Authorization"))
    if isinstance(user_id, int):
        data = request.get_json() or {}
        recipe = Recipe()
        response = recipe.update_recipe(category_id, recipe_id, data)
        return response

    else:
        return invalid_token()
