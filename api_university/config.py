import os
api_dir = os.path.abspath(os.path.dirname(__file__))
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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
    # JSON_SORT_KEYS = False
    API_URL = "/api/v1"
    SWAGGER = {
        'doc_dir': f'{api_dir}/Swagger',
        "specs_route": API_URL
    }


class DevelopmentConfiguration(Configuration):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfiguration(Configuration):
    # test_db_path = os.path.dirname(os.path.dirname(__file__))
    DATABASE = {
        'test_db_name': 'test_university.db'
    }
    # DATABASE = {
    #     'role_name': 'test_admins',
    #     'user_name': 'test_admin',
    #     'user_password': '1111',
    #     'db_name': 'test_university'
    # }
    ENV = 'test'
    TESTING = True
    TESTDB_PATH = project_dir + f"/tests/{DATABASE['test_db_name']}"
    TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///tests.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.dirname(os.path.dirname(__file__))
    # SQLALCHEMY_DATABASE_URI = (f"postgresql+psycopg2://"
    #                            f"{DATABASE['user_name']}:"
    #                            f"{DATABASE['user_password']}@"
    #                            f"localhost:5432/"
    #                            f"{DATABASE['db_name']}")






    # SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:12345@localhost:5432/test_db"
