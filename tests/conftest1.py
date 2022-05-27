import os
import pytest
from sqlalchemy import event

from api_university.app import create_app
from api_university.db.db_sqlalchemy import db as db_
from api_university.ma import ma as ma_
from tests.test_data.data import group_list, course_list, student_list
from api_university.config import TestingConfiguration

db_config = TestingConfiguration.DATABASE


def _foreign_key_pragma_on_connect(dbapi_connection, connection_record):
    dbapi_connection.execute('pragma foreign_keys=ON')


@pytest.fixture(scope="session")
def app():
    if os.path.exists(TestingConfiguration.TESTDB_PATH):
        os.unlink(TestingConfiguration.TESTDB_PATH)
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
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        event.listen(db_.engine, 'connect', _foreign_key_pragma_on_connect)
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







    # connection = db.engine.connect()
    # transaction = connection.begin()
    #
    # options = dict(bind=connection, binds={})
    # session_ = db.create_scoped_session(options=options)
    # db.session = session_
    # # session_ = db.session
    # # session_.begin_nested()
    # db.session.begin_nested()
    #
    # # session_.add_all(group_list)
    # # session_.add_all(course_list)
    # # session_.add_all(student_list)
    # # session_.commit()
    # ses = db.session
    #
    # # yield session_
    # yield ses
    #
    # db.session.close()
    # # db.get_engine(app).dispose()
    # transaction.rollback()
    # connection.invalidate()
    #
    #
    # # # checkpoint.rollback()
    # # # session_.flush()
    # # session_.expire_all()
    # # session_.close()
    # # # transaction.rollback()
    # # # connection.close()
    # # # session_.rollback()
    # # session_.remove()

# @pytest.fixture(scope='class', autouse=True)
# def app():
#     application = create_app(test_config=True)
#     with application.app_context():
#         # SETUP
#         if os.path.exists(TestingConfiguration.TESTDB_PATH):
#             os.unlink(TestingConfiguration.TESTDB_PATH)
#         db_.init_app(application)
#         ma.init_app(application)
#         db_.create_all()
#         # Add data to db
#         db_.session.add_all(group_list)
#         db_.session.add_all(course_list)
#         db_.session.add_all(student_list)
#         db_.session.commit()
#         yield application
#         # TEARDOWN
#         db_.session.remove()
#         db_.drop_all()
#         if os.path.exists(TestingConfiguration.TESTDB_PATH):
#             os.unlink(TestingConfiguration.TESTDB_PATH)
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()


# print(TestingConfiguration.TESTDB_PATH)
# print(os.path.exists(TestingConfiguration.TESTDB_PATH))
# @pytest.fixture(scope='session')
# def app(request):
#     """Session-wide test `Flask` application."""
#     app = create_app(test_config=True)
# 
#     # Establish an application context before running the tests.
#     ctx = app.app_context()
#     ctx.push()
# 
#     def teardown():
#         ctx.pop()
# 
#     request.addfinalizer(teardown)
#     return app
# 
# 
# @pytest.fixture(scope='session')
# def db(app, request):
#     """Session-wide test database."""
#     if os.path.exists(TestingConfiguration.TESTDB_PATH):
#         os.unlink(TestingConfiguration.TESTDB_PATH)
# 
#     def teardown():
#         db_.drop_all()
#         os.unlink(TestingConfiguration.TESTDB_PATH)
# 
#     db_.app = app
#     db_.create_all()
# 
#     request.addfinalizer(teardown)
#     return db_
# 
# 
# @pytest.fixture(scope='function')
# def session(db, request):
#     """Creates a new database session for a test."""
#     connection = db.engine.connect()
#     transaction = connection.begin()
# 
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
# 
#     db.session = session
# 
#     def teardown():
#         transaction.rollback()
#         connection.close()
#         session.remove()
# 
#     request.addfinalizer(teardown)
#     return session


# @pytest.fixture(scope='function')
# def app():
#     application = create_app(test_config=True)
#     db.init_app(application)
#     ma.init_app(application)
#     with application.app_context():
#         # SETUP
#
#         # db.drop_all()
#         db.create_all()
#         # Add data to db
#         db.session.add_all(group_list)
#         db.session.add_all(course_list)
#         db.session.add_all(student_list)
#         db.session.commit()
#         yield application
#         # TEARDOWN
#         db.session.remove()
#         db.drop_all()
#         # db.session.close()
#         # db.session.commit()
#         # app.app_context.pop()
#     # return application


# @pytest.fixture()
# def session(db, request)


# @pytest.fixture()
# def client():
#     app = create_app(test_config=True)
#     db.init_app(app)
#     ma.init_app(app)
#     with app.test_client() as client:
#         with app.app_context():
#             # SETUP
#
#             db.create_all()
#             # Add data to db
#             db.session.add_all(group_list)
#             db.session.add_all(course_list)
#             db.session.add_all(student_list)
#             yield app
#             # TEARDOWN
#             db.session.remove()
#             db.drop_all()
#         return client


# @pytest.fixture(scope='function')
# def client():
#     app = create_app(test_config=True)
#
#     with app.test_client() as client:
#         with app.app_context():
#             # SETUP
#             db.init_app(app)
#             ma.init_app(app)
#             db.create_all()
#             # Add data to db
#             db.session.add_all(group_list)
#             db.session.add_all(course_list)
#             db.session.add_all(student_list)
#             db.session.commit()
#             yield client
#             # TEARDOWN
#             db.session.remove()
#             db.drop_all()
#             # db.session.commit()
#             # app.app_context.pop()


# print('ossssssssssssss =', os.remove("api_university/tests.db"))
# print('os =', os.listdir())
# db_path = os.path.dirname(os.path.dirname(__file__))
# print(db_path)
# print(os.path.abspath(db_path))
#
#
# def app():
#     application = create_app(test_config=True)
#     db.init_app(application)
#     return application
#
#
# def set_up():
#     db.create_all()
#     db.session.commit()
#
#
# def tear_down():
#     db.session.remove()
#     db.drop_all()
#
#
# @pytest.fixture
# def client():
#     """Create Flask's test client to interact with the application"""
#     client = app().test_client()
#     set_up()
#     yield client
#     tear_down()


# @pytest.fixture
# def app():
#     app = create_app(test_config=True)
#     db.init_app(app)
#     ma.init_app(app)
#     # with app.app_context():
#     #     db.create_all()
#     #     insert_data_to_db(db,
#     #                       group_count=10,
#     #                       student_count=200,
#     #                       lower_limit_students_in_group=10,
#     #                       upper_limit_of_students_in_group=30)
#     #     yield
#     #     # teardown
#     #     db.session.remove()
#     #     db.drop_all()
#     return app


# @pytest.fixture(scope='class')
# def connect_test_db(app):
#     """Fixture to connect and disconnect database for each test class"""
#     # setup
#     with app.app_context():
#         db.create_all()
#         insert_data_to_db(db,
#                           group_count=10,
#                           student_count=200,
#                           lower_limit_students_in_group=10,
#                           upper_limit_of_students_in_group=30)
#         yield db
#         # teardown
#         db.drop_all()
#         db.session.commit()
