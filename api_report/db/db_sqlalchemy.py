from flask_sqlalchemy import SQLAlchemy
from api_report.models.utils import CustomBaseQuery

db = SQLAlchemy(query_class=CustomBaseQuery)
