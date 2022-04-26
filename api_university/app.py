import os
from flask import Flask, jsonify
from flask_restful import Api
from flasgger import Swagger
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.config import (Configuration,
                                   DevelopmentConfiguration,
                                   TestingConfiguration)
from api_university.data.data_insertion_into_db import insert_data_to_db
from api_university.resources.student import Student, StudentList
from api_university.resources.course import Course, CourseList
from api_university.resources.group import Group, GroupList


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
    api_url = Configuration.API_URL
    Swagger(
        application,
        template_file=os.path.join('Swagger', 'template.yml'),
        parse=True
    )

    # create db if not exists
    @application.before_first_request
    def create_tables():
        db.create_all()
        insert_data_to_db(db,
                          group_count=10,
                          student_count=200,
                          lower_limit_students_in_group=10,
                          upper_limit_of_students_in_group=30)
        db.session.commit()

    # Handlers
    @application.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        print('Got ValidationError =', err)
        return jsonify(err.messages), 400

    @application.errorhandler(IntegrityError)
    def handle_sqlalchemy_errors(err):
        print('Got IntegrityError =', err)
        return jsonify(err.orig.diag.message_detail), 400

    @application.errorhandler(AttributeError)
    def handle_attribute_errors(err):
        print('Got AttributeError =', err)
        return jsonify(err.args), 400

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
    return application


if __name__ == '__main__':
    app = create_app(dev_config=True)
    db.init_app(app)
    ma.init_app(app)
    app.run()
