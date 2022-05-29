from flask import jsonify, make_response


def make_error(status_code: int, message: str, err_name: str = None) -> jsonify:
    err_data = {
        'status': status_code,
        'message': message
    }
    if err_name:
        err_data['err_name'] = err_name
    response = jsonify(err_data)
    response.status_code = status_code
    return response


def handle_404_error_api(error=None) -> make_response:
    if error:
        return make_response(jsonify({'status': 404, 'message': str(error)}), 404)
    return make_response(jsonify({'status': 404, 'message': 'Not found'}), 404)
