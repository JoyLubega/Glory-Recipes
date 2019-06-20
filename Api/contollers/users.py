import re
from flask import jsonify
from ..models.user import UserModel


class Authentication(object):
    """
    Handles all user operations
    """

    @staticmethod
    def register(email, password, name):
        """
        Registers a new user to the application
        and returns an API response with status
        code set to 201 on success

        :param email:
        :param password:
        :param name:
        """
        if not name or not email or not password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 404
            return response

        if type(name) is int:
            response = jsonify({'Error': 'Numbers cant be a Name'})
            response.status_code = 400
            return response

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):  # noqa E501
            response = jsonify(
                {'message':
                 'Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com'}  # noqa E501
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

        if not re.match(r"(^[a-zA-Z_ ]*$)", name):
            response = jsonify(
                {'message':
                 'Name should be in alphabetical'}
            )
            response.status_code = 400
            return response

        user = UserModel(email=email, password=password, name=name)

        if user.query.filter_by(email=email).first():
            response = jsonify({'Error': 'Email Already exists'})
            response.status_code = 401
            return response

        user.save()
        response = jsonify({
            'Message': user.email + ' has Successfully registered',
            'token': user.id
        })
        response.status_code = 201
        return response

    @staticmethod
    def login(email, password):
        """
        logs in an existing user to the application
        and returns an API response with status
        code set to 201 on success

        :param email:
        :param password:
        """
        if not email or not password:
            response = jsonify({'Error': 'Missing login credentials'})
            response.status_code = 400
            return response

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):  # noqa E501
            response = jsonify(
                {'message':
                 'Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com'} # noqa E501
            )
            response.status_code = 401
            return response

        user = UserModel(email=email, password=password)
        user_data = user.query.filter_by(email=email).first()

        # If Login successful
        if user_data and user.check_password(user_data.password,
                                             password):
            response = jsonify({
                'Status': user.email + ' Login Successful',
                'token': user_data.id
            })
            response.status_code = 201
            return response

        response = jsonify({'Error': 'Incorrect email or password'})
        response.status_code = 401
        return response
