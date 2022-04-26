from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask_sqlalchemy import BaseQuery


class CustomBaseQuery(BaseQuery):
    def not_exists_or_400(self, ident, description=None):
        rv = self.get(ident)
        if rv is None:
            return rv

        return abort(400, description=description)


db = SQLAlchemy(query_class=CustomBaseQuery)
