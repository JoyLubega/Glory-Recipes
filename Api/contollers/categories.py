import re

from flask import jsonify, url_for
from flask import request

from ..models.category import CategoryModel


class Category(object):
    """
    Handles all category operations
    """

    @staticmethod
    def create_category(name, parent_id):
        """
        Creates a new recipe category
        :param name:
        :return: object
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 400
            return response

        if type(name) is int:
            response = jsonify({'Error': 'Numbers cant be a Name'})
            response.status_code = 400
            return response

        if not re.match(r"(^[a-zA-Z_ ]*$)", name):
            response = jsonify(
                {'message':
                 'Name should be in alphabetical'}
            )
            response.status_code = 400
            return response

        if re.match(r"(^[ ]*$)", name):
            response = jsonify(
                {'message':
                 'A space is not a name'}
            )
            response.status_code = 400
            return response
        category_name = name.lower()
        category = CategoryModel(
            name=category_name, parent_id=parent_id)
        try:
            category.save()
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_added': category.date_added,
                'parent_id': category.parent_id
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify(
                {
                    'Error': 'Name ' + category.name.capitalize() + ' exists'
                }
            )
            response.status_code = 409
            return response

    @staticmethod
    def get_categories(search, limit):
        """
        Gets all recipe categories
        :param user_id:
        :param search:
        :return:
        """
        page = request.args.get('page', 1, type=int)

        response = CategoryModel.query.limit(limit).all()
        if not response:
            response = jsonify({"Msg": "No categories found"})
            response.status_code = 400
            return response
        else:
            results = []

            if search:
                categories = CategoryModel.query.filter(
                        CategoryModel.name.ilike('%{0}%'.format(search)))
            else:
                categories = CategoryModel.query.order_by(CategoryModel.id)

            if categories:

                pagination = categories.paginate(
                    page, per_page=limit, error_out=False)
                category_lists = pagination.items
                if pagination.has_prev:
                    prev = url_for('get_categories', page=page -
                                   1, limit=limit, _external=True)
                else:
                    prev = None
                if pagination.has_next:
                    next = url_for('get_categories', page=page +
                                   1, limit=limit, _external=True)
                else:
                    next = None
                if category_lists:
                    for cat in category_lists:
                        obj = {
                            'id': cat.id,
                            'name': cat.name,
                            'date_created': cat.date_added,
                            'parent_id': cat.parent_id,
                        }
                        results.append(obj)
                    response = jsonify({
                        'Category': results,
                        'prev': prev,
                        'next': next,
                        'count': pagination.total
                    })
                    response.status_code = 200
                    return response
                else:
                    return {'message': 'No Categories to display'}, 404

    @staticmethod
    def get_single_category(category_id):
        """
        Gets single category
        :param category_id:
        """
        category = CategoryModel.query.filter_by(id=category_id).first()
        if not category:
            response = jsonify({
                'error': 'category with id: ' +
                         str(category_id) + ' is not found'
            })
            response.status_code = 404
            return response

        category_data = {
            'id': category.id,
            'name': category.name,
            'Parent': category.parent_id,
            'date_added': category.date_added,

        }
        response = jsonify(category_data)
        response.status_code = 200
        return response

    @staticmethod
    def delete_category(category_id):
        """
        Delete single category
        :param category_id:
        """
        category = CategoryModel.query.filter_by(id=category_id).first()
        if not category:
            response = jsonify({
                'error': 'category with id: ' +
                         str(category_id) + ' is not found'
            })
            response.status_code = 404
            return response
        else:
            category.delete()
            category_data = {
                'id': category.id,
                'name': category.name,
                'Parent': category.parent_id,
                'date_added': category.date_added,

            }
            response = jsonify({"msg": "category deleted permanently",
                                "data": category_data})
            response.status_code = 200
            return response

    @staticmethod
    def update_category(category_id, data):
        """
        Updates a category
        :param category_id:
        :param category_name:
        :param parent_id:
        """
        category = CategoryModel.query.filter_by(id=category_id).first()

        if category:
            if 'name' in data:
                if data['name'] != category.name and \
                        CategoryModel.query.filter_by(
                            name=data['name']).first():

                    return jsonify({'msg': 'please use a different username'})
                else:
                    category.name = data['name']

            if 'parent_id' in data:
                if data['parent_id'] == category.id:
                    return jsonify({'msg': 'Can not be a parent to self'})
                else:
                    category.parent_id = data['parent_id']

            category.update()
            Category = CategoryModel.query.filter_by(id=category_id).first()
            result = {
                        'id': Category.id,
                        'name': Category.name,
                        'Parent': Category.parent_id
                        }
            response = jsonify(
                {
                    'message': 'Category has been successfully updated',
                    'category': result
                }
            )
            response.status_code = 200
            return response
        else:
            response = jsonify({"Error": "The category does not exist"})
            response.status_code = 404
            return response
