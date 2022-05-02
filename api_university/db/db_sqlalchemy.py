from flask_sqlalchemy import SQLAlchemy
from flask import abort, jsonify, Response
from flask_sqlalchemy import BaseQuery


def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message
    })
    response.status_code = status_code
    return response


class CustomBaseQuery(BaseQuery):
    def not_exists_or_400(self, ident, description=None):
        rv = self.get(ident)
        if rv is None:
            return rv

        return abort(400, description=description)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if rv is None:
            if isinstance(description, Response):
                abort(description)
            else:
                abort(404, description=description)
        return rv


db = SQLAlchemy(query_class=CustomBaseQuery)
