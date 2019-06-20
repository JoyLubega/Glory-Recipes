from flask import request

from ..api import app
from ..error_handlers import * # noqa F401
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
            category_name = name.lower()
            category = Category()
            response = category.create_category(
                category_name, user_id, parent_id)
            return response

        return invalid_token()

    except KeyError:
        return invalid_key_data()


@app.route('/categories', methods=['GET'])
def get_categories():
    """Method to handle getting all recipe categories"""
    try:
        user_id = decode_auth_token(request.headers.get("Authorization"))
        if isinstance(user_id, int):
            limit = request.args.get('limit', 5, int)
            search = request.args.get("q", "")

            category = Category()
            if limit:
                limit = int(limit)
                response = category.get_categories(user_id, search, limit)
                return response
            response = category.get_categories(user_id, search, limit)
            return response

        else:
            return invalid_token()

    except KeyError:
        return ("Bad request")
