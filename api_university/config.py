import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    DATABASE = {
        'role_name': 'admins',
        'user_name': 'admin',
        'user_password': '1111',
        'db_name': 'university'
    }
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (f"postgresql+psycopg2://"
                               f"{DATABASE['user_name']}:"
                               f"{DATABASE['user_password']}@"
                               f"localhost:5432/"
                               f"{DATABASE['db_name']}")
    JSON_SORT_KEYS = False
    API_URL = "/api/v1"
    SWAGGER = {
        'doc_dir': './Swagger',
        "specs_route": API_URL
    }


class DevelopmentConfiguration(Configuration):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfiguration(Configuration):
    TESTING = True
