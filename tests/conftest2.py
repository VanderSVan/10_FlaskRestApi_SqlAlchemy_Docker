import os
import pytest
from sqlalchemy import event

from api_university.app import create_app
from api_university.db.db_sqlalchemy import db as db_
from api_university.ma import ma as ma_
from tests.test_data.data import group_list, course_list, student_list
from api_university.config import TestingConfiguration

from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from api_university.models.group import GroupModel
from string import ascii_uppercase
from random import choices, sample, choice, randint

db_config = TestingConfiguration.DATABASE


# def _foreign_key_pragma_on_connect(dbapi_connection, connection_record):
#     dbapi_connection.execute('pragma foreign_keys=ON')
#
#
# @pytest.fixture(scope='session')
# def app():
#     # if os.path.exists(TestingConfiguration.TESTDB_PATH):
#     #     os.unlink(TestingConfiguration.TESTDB_PATH)
#     app = create_app(test_config=True)
#
#     ctx = app.app_context()
#     ctx.push()
#
#     yield app
#     ctx.pop()
#
#
# @pytest.fixture(scope='session')
# def client(app):
#     return app.test_client()
#
#
# @pytest.fixture(scope='session')
# def db(app):
#     db_.init_app(app)
#     ma_.init_app(app)
#     if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
#         event.listen(db_.engine, 'connect', _foreign_key_pragma_on_connect)
#     db_.drop_all()
#     db_.create_all()
#     db_.session.add_all(group_list)
#     db_.session.add_all(course_list)
#     db_.session.add_all(student_list)
#     session = db_.session
#     # seed_data_if_not_exists(session)
#     session.commit()
#
#     yield db_
#
#     session.rollback()
#     db_.drop_all()  # if necessary
#
#
# @pytest.fixture(scope='function')
# def session(app, db):
#     session = db.session
#     session.begin_nested()
#
#     yield session
#
#     session.rollback()

def _generate_group_name(letters: str, separator: str) -> str:
    """Creates random string like type: AA-11"""
    result_list = choices(letters, k=2)
    two_digit_number = randint(10, 100)
    result_list.append(separator)
    result_list.append(str(two_digit_number))
    return "".join(result_list)


def generate_group_instances(number_of_instance: int) -> list:
    """
    Model: AA-11
    Generates random group instances.
    """
    return [GroupModel(
                       name=_generate_group_name(ascii_uppercase, '-'))
            for group_id in range(1, number_of_instance + 1)]


def _foreign_key_pragma_on_connect(dbapi_connection, connection_record):
    dbapi_connection.execute('pragma foreign_keys=ON')


@pytest.fixture(scope="session")
def app():
    if os.path.exists(TestingConfiguration.TESTDB_PATH):
        os.unlink(TestingConfiguration.TESTDB_PATH)
    app_ = create_app(test_config=True)
    with app_.app_context():

        yield app_





@pytest.fixture(scope="session")
def db(app):
    db_.init_app(app)
    ma_.init_app(app)
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        event.listen(db_.engine, 'connect', _foreign_key_pragma_on_connect)
    # db_.create_all()

    yield db_
    # db_.drop_all()


@pytest.fixture(scope="function")
def session(db):
    # connection = db.engine.connect()
    # transaction = connection.begin()
    # session = db.session
    # # meta = db.metadata
    # # for table in reversed(meta.sorted_tables):
    # #     print('Clear table %s' % table)
    # #     session.execute(table.delete())
    # # session.commit()
    # print('new session')
    #
    # session.add_all(group_list)
    # session.add_all(course_list)
    # session.add_all(student_list)
    # session.commit()
    # print(StudentModel.find_by_id(5))
    #
    # yield session
    #
    # transaction.rollback()
    # connection.close()
    # session.remove()

    # db.drop_all()
    session = db.session
    db.create_all()

    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()
    print('new session')

    # db.create_all()
    print(GroupModel.find_by_id(2))
    session.add_all(generate_group_instances(number_of_instance=3))
    session.commit()
    # session.add_all(course_list)
    # session.commit()
    # session.add_all(student_list)
    # session.commit()
    # session.flush()

    print('tables have been created')
    print(GroupModel.find_by_id(2))
    # session.commit()
    # a = session.begin_nested()

    yield session
    # a.rollback()
    # a.close()
    db.drop_all()
    session.close()
    # session.remove()
    # db.session.query(StudentModel).delete()
    # db.session.query(CourseModel).delete()
    # db.session.query(GroupModel).delete()
    # session.commit()
    # session.rollback()
    # session.close_all()

    # db.drop_all()
    # session.remove()
    # session.commit()


@pytest.fixture(scope='function')
def client(app, session):
    return app.test_client()



# @pytest.fixture(scope="function", autouse=True)
# def session(db):
#     # db.drop_all()
#     # db.create_all()
#     # db.session.add_all(group_list)
#     # db.session.add_all(course_list)
#     # db.session.add_all(student_list)
#     # db.session.commit()
#     #
#     # save_point1 = db.session.begin_nested()
#     # save_point2 = db.session.begin_nested()
#     # session_backup = db.session
#     # db.session = save_point2.session
#
#     yield db.session
#     db.session.rollback()
#     # save_point1.rollback()
#     # db.session = session_backup
#     # db.drop_all()
#     # session_.close()
#     # session_.remove()
