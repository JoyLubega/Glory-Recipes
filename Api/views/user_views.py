from flask import request

from ..api import app
from ..error_handlers import *
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


@app.route('/auth/users', methods=['GET'])
def get_users():
    """Method to handle get all users"""
    try:
        user = Authentication()
        response = user.get_all_users()
        return response

    except KeyError:
        return ("Bad data")


@app.route('/auth/users/<int:id>', methods=['GET'])
def get_a_user(id):
    """Method to handle get a single user"""
    try:
        user = Authentication()
        response = user.get_single_user(id)
        return response

    except KeyError:
        return ("No user Found")


@app.route('/auth/user/<int:id>', methods=['DELETE'])
def delete_users(id):
    """Method to handle delete a user"""
    try:
        user = Authentication()
        response = user.delete_user(id)
        return response

    except KeyError:
        return ("Bad data")


@app.route('/auth/user/<int:id>', methods=['PUT'])
def update_user(id):
    """Method to handle update a user"""
    try:
        data = request.get_json() or {}
        user = Authentication()
        response = user.update_user(id, data)
        return response

    except KeyError:
        return ({"Error": "An error occured"})
