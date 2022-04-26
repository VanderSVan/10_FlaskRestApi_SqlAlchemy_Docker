import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://admin:1111@localhost:5432/university"
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
