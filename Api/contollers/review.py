from flask import jsonify, request, url_for

from Api.models.category import CategoryModel
from Api.models.recipes import RecipeModel
from Api.models.user import UserModel
from Api.models.reviews import ReviewsModel
from Api.api import db


class Review(object):
    """
    Handles all review operations
    """

    @staticmethod
    def add_review(user_id, recipe_id, comment_text, rate):
        """
        Adds a review
        :param user_id:
        :param recipe_id:
        :param rate:
        :param comment_text:
        """
        if not isinstance(rate, int):
            response = jsonify({'Error': 'Missing rate'})
            response.status_code = 404
            return response

        if rate not in range(1, 5):
            response = jsonify({'Error': 'The rating is between 1 to 5'})
            response.status_code = 400
            return response

        if not isinstance(comment_text, str):
            response = jsonify({'Error': 'Missing comment_text'})
            response.status_code = 404
            return response

        recipe = RecipeModel.query.filter_by(id=recipe_id).first()
        if not recipe:
            response = jsonify({'Error': 'Recipe not found'})
            response.status_code = 404
            return response

        created_by = recipe.user_id
        if user_id == created_by:
            response = jsonify({'Error': 'You can not rate your own recipe'})
            response.status_code = 400
            return response
        else:
            review = ReviewsModel(
                recipe_id=recipe_id,
                comment_text=comment_text,
                rate=rate)

            try:
                review.save()
                result = {
                    'id': review.id,
                    'rating': review.rate,
                    'comment_text': review.comment_text
                }
                response = jsonify({
                    "msg": "Review added successfully",
                    "review": result
                })
                response.status_code = 201
                return response
            except Exception:
                response = jsonify({'Error': 'Already exists'})
                response.status_code = 409
                return response
