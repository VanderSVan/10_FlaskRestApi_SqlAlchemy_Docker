from flask import jsonify


def make_error(status_code: int, message: str, err_name=None):
    err_data = {
        'status': status_code,
        'message': message
    }
    if err_name:
        err_data['err_name'] = err_name
    response = jsonify(err_data)
    response.status_code = status_code
    return response
