import pytest

from api_university.app import create_app
from api_university.db.db_sqlalchemy import db as db_
from api_university.ma import ma as ma_
from tests.test_data.data import group_list, course_list, student_list
from api_university.config import TestingConfiguration
from api_university.db.db_operations import DatabaseOperation
from api_university.db.tools.utils import PsqlDatabaseConnection

db_config = TestingConfiguration.DATABASE


@pytest.fixture(scope="session")
def app():
    with PsqlDatabaseConnection() as conn:
        database = DatabaseOperation(connection=conn,
                                     db_name=db_config['db_name'],
                                     user_name=db_config['user_name'],
                                     user_password=db_config['user_password'],
                                     role_name=db_config['role_name'])
        database.drop_all()
        database.create_all()

    app_ = create_app(test_config=True)
    with app_.app_context():

        yield app_


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app):
    db_.init_app(app)
    ma_.init_app(app)
    db_.create_all()
    db_.session.add_all(group_list)
    db_.session.add_all(course_list)
    db_.session.add_all(student_list)
    db_.session.commit()

    yield db_

    db_.drop_all()


@pytest.fixture(scope="function", autouse=True)
def session(db, app):
    session_ = db.session
    session_.begin_nested()

    yield session_

    session_.rollback()
    session_.close()
    session_.remove()
