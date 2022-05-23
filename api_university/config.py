import os
api_dir = os.path.abspath(os.path.dirname(__file__))
swag_dir = os.path.join(api_dir, 'Swagger')
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Configuration:
    API_URL = "/api/v1"
    RESOURCES = {
        'students': f"{API_URL}/students",
        'student_id': f"{API_URL}/students/<int:student_id>",

        'courses': f"{API_URL}/courses",
        'course_id': f"{API_URL}/courses/<int:course_id>",

        'groups': f"{API_URL}/groups",
        'group_id': f"{API_URL}/groups/<int:group_id>"

    }
    SQLALCHEMY_DATABASE_URI = (f"postgresql+psycopg2://"
                               f"{os.getenv('PG_USER')}:"
                               f"{os.getenv('PG_USER_PASSWORD')}@"
                               f"{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/"
                               f"{os.getenv('PG_DB')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR = os.path.join(api_dir, 'db', 'migrations')
    SWAGGER = {
        'doc_dir': f'{api_dir}/Swagger',
        "specs_route": API_URL
    }
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class DevelopmentConfiguration(Configuration):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfiguration(Configuration):
    DATABASE = {
        'test_db_name': 'test_university.db'
    }
    ENV = 'test'
    TESTING = True
    TESTDB_PATH = project_dir + f"/tests/{DATABASE['test_db_name']}"
    TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
