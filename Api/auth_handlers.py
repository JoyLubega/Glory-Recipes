import datetime
import jwt
from flask import json, jsonify

from Api.views.user_views import app


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(token):
    """
    Decodes the authentication token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            token, app.config.get('SECRET_KEY'), algorithms=['HS256'], verify= False)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        response = jsonify({
            'Expired': 'Signature expired. Please log in again.'
        })
        response.status_code = 401
        return response

    except jwt.InvalidTokenError:
        response = jsonify({
            'Invalid': 'Invalid token. Please log in again.'
        })
        response.status_code = 401
        return response


def authentication_success(response):
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        data['token'] = encode_auth_token(data['token']).decode()
        response = jsonify(data)
        response.status_code = 201
    return response


def invalid_key_data():
    response = jsonify({'Error': 'Check the keys and try again'})
    response.status_code = 400
    return response


def invalid_token():
    response = jsonify({'Error': 'Token not found'})
    response.status_code = 401
    return response
