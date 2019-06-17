
def validate_register(name, email, password):
    if not name or not email or not password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 404
            return response

    if isinstance(name, int):
        response = jsonify({'Error': 'Numbers cant be a Name'})
        response.status_code = 400
        return response

    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        response = jsonify(
        {'message':
        'Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com' }
        )
        response.status_code = 401
        return response


    if re.match(r"(^[ ]*$)", name):
        response = jsonify(
        {'message':
        'A space is not a name' }
        )
        response.status_code = 401
        return response


    if not re.match(r"(^[a-zA-Z_ ]*$)", name):
        response = jsonify(
        {'message':
        'Name should be in alphabetical' }
        )
        response.status_code = 401
        return response



