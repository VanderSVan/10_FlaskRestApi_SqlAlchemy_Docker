from flask_sqlalchemy import SQLAlchemy
from api_university.models.utils import CustomBaseQuery

db = SQLAlchemy(query_class=CustomBaseQuery)
