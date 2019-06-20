from flask import request

from ..api import app
from ..error_handlers import * # noqa F401
from Api.contollers.users import Authentication
from Api.auth_handlers import authentication_success, invalid_key_data


@app.route('/auth/register', methods=['POST'])
def register():
    """Method to handle user registration"""
    request.get_json(force=True)

    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        user = Authentication()
        response = user.register(email, password, name)
        response = authentication_success(response)
        return response

    except KeyError:
        return invalid_key_data()


@app.route('/auth/login', methods=['POST'])
def login():
    """Method to handle user login"""
    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        user = Authentication()
        response = user.login(email, password)
        response = authentication_success(response)
        return response

    except KeyError:
        return invalid_key_data()
