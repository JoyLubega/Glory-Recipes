import re

from flask import jsonify, url_for
from flask import request

from ..models.category import CategoryModel


class Category(object):
    """
    Handles all category operations
    """

    @staticmethod
    def create_category(name, user_id, parent_id):
        """
        Creates a new recipe category
        :param name:
        :param user_id:
        :return:
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 404
            return response

        if type(name) is int:
            response = jsonify({'Error': 'Numbers cant be a Name'})
            response.status_code = 401
            return response

        if not re.match(r"(^[a-zA-Z_ ]*$)", name):
            response = jsonify(
                {'message':
                 'Name should be in alphabetical'}
            )
            response.status_code = 401
            return response

        if re.match(r"(^[ ]*$)", name):
            response = jsonify(
                {'message':
                 'A space is not a name'}
            )
            response.status_code = 401
            return response

        category = CategoryModel(
            name=name, created_by=user_id, parent_id=parent_id)
        try:
            category.save()
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_added': category.date_added,
                'created_by': category.created_by,
                'parent_id': category.parent_id
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify(
                {'Error': 'Category' + category.name.capitalize() + 'already exists, add a sub category to it'}) # noqa E501
            response.status_code = 409
            return response

    @staticmethod
    def get_categories(user_id, search, limit):
        """
        Gets all recipe categories
        :param user_id:
        :param search:
        :return:
        """
        page = request.args.get('page', 1, type=int)

        response = CategoryModel.query.filter_by(
            created_by=user_id).limit(limit).all()
        if not response:
            response = jsonify([])
            response.status_code = 400
            return response
        else:
            results = []

            if search:
                categories = CategoryModel.query.filter_by(
                    created_by=user_id).filter(
                        CategoryModel.name.ilike('%{0}%'.format(search)))
            else:
                categories = CategoryModel.query.filter_by(created_by=user_id)

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
                            'created_by': cat.created_by,
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
