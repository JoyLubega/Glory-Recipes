from flask import request

from ..api import app
from ..error_handlers import *
from ..auth_handlers import decode_auth_token, invalid_token, invalid_key_data
from Api.contollers.review import Review


@app.route('/review/<int:recipe_id>', methods=['POST'])
def add_review(recipe_id):
    """Method to handle creating a review on a recipe"""
    request.get_json(force=True)
    try:
        loggedin_user_id = decode_auth_token(
            request.headers.get("Authorization"))
        if isinstance(loggedin_user_id, int):
            rate = request.json['rate']
            comment_text = request.json.get('comment_text')
            review = Review()
            response = review.add_review(loggedin_user_id, recipe_id,
                                         comment_text, rate)
            return response

        return invalid_token()

    except KeyError:
        return invalid_key_data()
