import re
from flask import jsonify
from email_validator import validate_email, EmailNotValidError

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
        match = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(match, email):
            response = jsonify(
                {
                    'message': 'Invalid email! A valid email should in this'
                               'format me.name@gmail.com'
                }
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
        match = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(match, email):
            response = jsonify(
                {
                    'message': 'Invalid email! A valid email should '
                               'in this format me.name@gmail.com'
                }
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

    @staticmethod
    def get_all_users():
        """
        Gets all users in the database
        :param: user_id
        :return: str
        """
        response = UserModel.query.all()
        if not response:
            response = jsonify({
                "message": "No Users found"
            })
            response.status_code = 400
            return response
        else:
            all_users = []
            for data in response:
                users = {
                    "id": data.id,
                    "name": data.name,
                    "email": data.email
                }
                all_users.append(users)
            response = jsonify(all_users)
            return response

    @staticmethod
    def get_single_user(user_id):
        """
        Gets single user using ID
        :param user_id:
        """
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            response = jsonify({
                'error': 'User with id: ' + str(user_id) + ' is not found'
            })
            response.status_code = 404
            return response

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'status': user.status,
        }
        response = jsonify(user_data)
        response.status_code = 200
        return response

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user from the database
        :return:
        """
        response = UserModel.query.filter_by(id=user_id).first()
        if not response:
            response = jsonify({
                "Error": "User doesnot exist"
            })
            response.status_code = 400
            return response
        else:
            response.delete()
            message = jsonify({
                "Msg": "User deleted"
            })
            return message

    @staticmethod
    def update_user(user_id, data):
        """
        Updates User details

        :param user_id:
        :param name:
        :param email:
        """

        user = UserModel.query.filter_by(id=user_id).first()

        if user:
            if 'name' in data:
                if data['name'] != user.name and \
                        UserModel.query.filter_by(name=data['name']).first():

                    return jsonify({'msg': 'please use a different username'})
                else:
                    user.name = data['name']

            if 'email' in data:
                if data['email'] != user.email and \
                        UserModel.query.filter_by(email=data['email']).first():
                    return jsonify({'msg': 'please use a different email'})
                else:
                    try:
                        is_valid = validate_email(data['email'])
                        if is_valid['email']:
                            user.email = data['email']
                    except EmailNotValidError as e:
                        return ({"Error": str(e)})

            user.update()
            User = UserModel.query.filter_by(id=user_id).first()
            result = {
                        'id': User.id,
                        'name': User.name,
                        'email': User.email
                        }
            response = jsonify(
                {'message': 'User has been successfully updated',
                 'user': result
                 })
            response.status_code = 200
            return response
        else:
            return jsonify({"Error": "The user does not exist"})
