import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flasgger import Swagger
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.config import (
    Configuration,
    DevelopmentConfiguration,
    TestingConfiguration
)
from api_university.db.db_operations import DatabaseOperation
from api_university.data.insertion_data_into_db import insert_data_to_db
from api_university.resources.student import Student, StudentList
from api_university.resources.course import Course, CourseList
from api_university.resources.group import Group, GroupList
from api_university.handlers import make_error, handle_404_error_api

migrate = Migrate()
api_url = Configuration.API_URL
load_dotenv()


def create_app(test_config=False, dev_config=False):
    application = Flask(__name__)

    # Config
    if test_config:
        application.config.from_object(TestingConfiguration)
    elif dev_config:
        application.config.from_object(DevelopmentConfiguration)
    else:
        application.config.from_object(Configuration)

    api = Api(application)
    Swagger(
        application,
        template_file=os.path.join('Swagger', 'template.yml'),
        parse=True
    )
    if not test_config:
        # create db if not exists
        @application.before_first_request
        def create_tables():
            # create db (gets data from .env)
            database = DatabaseOperation()
            database.create_db()

            # create tables
            db.create_all()

            # insert prepared data
            insert_data_to_db(db,
                              group_count=10,
                              student_count=200,
                              lower_limit_of_students_in_group=10,
                              upper_limit_of_students_in_group=30)
            db.session.commit()

    # Handlers
    @application.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        status = 400
        err_name = "ValidationError"
        message = err.messages.get(0) or err.messages or err
        print('Got ValidationError =', message)
        return make_error(status, message, err_name)

    @application.errorhandler(IntegrityError)
    def handle_sqlalchemy_errors(err):
        status = 400
        err_name = "IntegrityError"
        message = err.orig.args[0] or err
        print('Got IntegrityError =', err)
        db.session.rollback()
        return make_error(status, message, err_name)

    @application.errorhandler(AttributeError)
    def handle_attribute_errors(err):
        status = 400
        err_name = "AttributeError"
        message = err.messages or err
        print('Got AttributeError =', err)
        return make_error(status, message, err_name)

    # RESOURCES:
    # Student
    api.add_resource(StudentList, f"{api_url}/students")
    api.add_resource(Student, f"{api_url}/students/<int:student_id>")

    # Courses
    api.add_resource(CourseList, f"{api_url}/courses")
    api.add_resource(Course, f"{api_url}/courses/<int:course_id>")

    # Groups
    api.add_resource(GroupList, f"{api_url}/groups")
    api.add_resource(Group, f"{api_url}/groups/<int:group_id>")

    # HANDLERS:
    application.register_error_handler(404, handle_404_error_api)

    # Initialization
    db.init_app(application)
    ma.init_app(application)
    migrate.init_app(application, db, directory=Configuration.MIGRATION_DIR)

    return application


if __name__ == '__main__':
    app = create_app(dev_config=True)
    app.run(host="0.0.0.0")
