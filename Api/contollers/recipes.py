from flask import jsonify, request

from Api.models.category import CategoryModel
from Api.models.recipes import RecipeModel
from Api.models.user import UserModel
from Api.api import db


class Recipe(object):
    """
    Handles all recipe operations
    """

    @staticmethod
    def add_recipe(user_id, category_id, recipe_text, name_of_recipe):
        """
        Adds a recipe
        :param user_id:
        :param category_id:
        :param recipe_text:
        :param name_of_recipe:
        """
        if not name_of_recipe:
            response = jsonify({'Error': 'Missing Recipe name'})
            response.status_code = 404
            return response

        category = CategoryModel.query.filter_by(id=category_id).first()
        if not category:
            response = jsonify({'Error': 'Category not found'})
            response.status_code = 404
            return response

        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            response = jsonify({'Error': 'User not in table'})
            response.status_code = 404
            return response

        recipe = RecipeModel(name=name_of_recipe, category_id=category_id,
                             user_id=user_id, recipe_text=recipe_text)
        try:
            recipe.save()
            response = jsonify({
                'id': recipe.id,
                'name': recipe.name,
                'recipe_text': recipe.recipe_text,
                'date_added': recipe.date_added,
                'category_id': recipe.category_id,
                'user_id': recipe.user_id
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify({'Error': 'Recipe name Already exists'})
            response.status_code = 409
            return response

    @staticmethod
    def get_recipes(search, limit, category_id):
        """
        Gets all recipes
        :param category_id:
        :param search:
        :return:
        """
        page = request.args.get('page', 1, type=int)

        response = RecipeModel.query.filter_by(
                    category_id=category_id).limit(limit).all()
        if not response:
            response = jsonify({"Msg": "No Recipes found"})
            response.status_code = 400
            return response
        else:
            results = []

            if search:
                recipes = RecipeModel.query.filter_by(
                    category_id=category_id).filter(
                        RecipeModel.name.ilike('%{0}%'.format(search)))
            else:
                recipes = RecipeModel.query.filter_by(category_id=category_id)

            if recipes:

                pagination = recipes.paginate(
                    page, per_page=limit, error_out=False)
                recipe_lists = pagination.items
                if pagination.has_prev:
                    prev = url_for('get_recipes', page=page -
                                   1, limit=limit, _external=True)
                else:
                    prev = None
                if pagination.has_next:
                    next = url_for('get_recipes', page=page +
                                   1, limit=limit, _external=True)
                else:
                    next = None
                if recipe_lists:
                    for recipe in recipe_lists:
                        obj = {
                            'id': recipe.id,
                            'name': recipe.name,
                            'date_created': recipe.date_added,
                            'recipe_text': recipe.recipe_text,
                            'user': recipe.user_id,
                            'category_id': recipe.category_id
                        }
                        results.append(obj)
                    response = jsonify({
                        'recipes': results,
                        'prev': prev,
                        'next': next,
                        'count': pagination.total
                    })
                    response.status_code = 200
                    return response
                else:
                    return {'message': 'No Recipes to display'}, 404

    @staticmethod
    def get_single_recipe(recipe_id, category_id):
        """
        Gets single category
        :param category_id:
        :param recipe_id:
        """
        recipe = RecipeModel.query.filter_by(id=recipe_id,
                                             category_id=category_id).first()
        if not recipe:
            response = jsonify({
                'error': 'recipe with id: ' +
                         str(recipe_id) + ' is not found in that category'
            })
            response.status_code = 404
            return response

        recipe_data = {
            'id': recipe.id,
            'name': recipe.name,
            'recipe_text': recipe.recipe_text,
            'date_added': recipe.date_added,
            'user_id': recipe.user_id,
            'category_id': recipe.category_id
        }
        response = jsonify(recipe_data)
        response.status_code = 200
        return response

    @staticmethod
    def delete_recipe(category_id, recipe_id):
        """
        Delete single recipe permanently
        :param category_id:
        :param recipe_id:
        """
        recipe = RecipeModel.query.filter_by(id=recipe_id,
                                             category_id=category_id).first()
        if not recipe:
            response = jsonify({
                'error': 'recipe with id: ' +
                         str(recipe_id) + ' is not found'
            })
            response.status_code = 404
            return response
        else:
            recipe.delete()
            recipe_data = {
                'id': recipe.id,
                'name': recipe.name,
                'recipe_text': recipe.recipe_text,
                'date_added': recipe.date_added,
                'user_id': recipe.user_id,
                'category_id': recipe.category_id
            }
            response = jsonify({"msg": "recipe deleted permanently",
                                "data": recipe_data})
            response.status_code = 200
            return response

    @staticmethod
    def update_recipe(category_id, recipe_id, data):
        """
        Updates a recipe
        :param category_id:
        :param recipe_id:
        :param name_of_recipe:
        :param recipe_text:
        """
        recipe = RecipeModel.query.filter_by(id=recipe_id,
                                             category_id=category_id).first()

        if recipe:
            if 'name_of_recipe' in data:
                if data['name_of_recipe'] != recipe.name and \
                        RecipeModel.query.filter_by(
                            name=data['name_of_recipe']).first():

                    return jsonify({'msg': 'please use a different username'})
                else:
                    recipe.name = data['name_of_recipe']

            if 'recipe_text' in data:
                recipe.recipe_text = data['recipe_text']

            recipe.update()
            recipe = RecipeModel.query.filter_by(id=recipe_id).first()
            result = {
                        'id': recipe.id,
                        'name': recipe.name,
                        'recipe_text': recipe.recipe_text,
                        'category_id': recipe.category_id,
                        'user_id': recipe.user_id
                        }
            response = jsonify(
                {
                    'message': 'recipe has been successfully updated',
                    'category': result
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify({"Error": "The recipe does not exist"})
            response.status_code = 404
            return response
