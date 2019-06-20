from flask import jsonify
from Api.views.user_views import app

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''

'''
    (UTF) Unicode Transformation Format
    its a character encoding
    A character in UTF8 can be from 1 to 4 bytes long
    UTF-8 is backwards compatible with ASCII
    is the preferred encoding for e-mail and web pages
'''


@app.errorhandler(404)
def page_not_found(e):
    response = jsonify(
        {'error': 'The request can not be linked to,\
            Please check your endpoint url'}
        )
    response.status_code = 404
    return response


# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify(
        {
            'error': 'Invalid request method.\
                Please check the request method being used'
        })
    response.status_code = 405
    return response


# 401 error handler
@app.errorhandler(401)
def unauthorized_error(e):
    response = jsonify({"error": "The token has a problem"})
    response.status_code = 401
    return response


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({
        'error': 'something is wrong, please restart the server'
        })
    response.status_code = 500
    return response
