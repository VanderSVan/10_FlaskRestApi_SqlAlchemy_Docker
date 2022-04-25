import os
from flask import Flask, jsonify
from flask_restful import Api
from flasgger import Swagger
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from api_report.data.data_insertion_into_db import insert_data_to_db
from api_report.resources.student import Student, StudentList
from api_report.resources.course import Course, CourseList
from api_report.resources.group import Group, GroupList


def create_app(test_config=False):
    application = Flask(__name__)

    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:1111@localhost:5432/university"
    application.config['JSON_SORT_KEYS'] = False
    application.config['SWAGGER'] = {
        'doc_dir': './Swagger'
    }
    api = Api(application)
    Swagger(
        application,
        template_file=os.path.join('Swagger', 'template.yml'),
        parse=True
    )

    @application.before_first_request
    def create_tables():
        db.create_all()

        insert_data_to_db(db)

        db.session.commit()
        # print('Tables has been created')

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

    if test_config:
        application.config['TESTING'] = True

    # RESOURCES:
    # Student
    api.add_resource(StudentList, "/students")
    api.add_resource(Student, "/students/<int:student_id>")

    # Courses
    api.add_resource(CourseList, "/courses")
    api.add_resource(Course, "/courses/<int:course_id>")

    # Groups
    api.add_resource(GroupList, "/groups")
    api.add_resource(Group, "/groups/<int:group_id>")
    return application


if __name__ == '__main__':
    from api_report.db.db_sqlalchemy import db
    from api_report.ma import ma

    app = create_app()
    db.init_app(app)
    ma.init_app(app)

    # with app.app_context():
    #     print(StudentModel.query.first())
    #     print(StudentModel.find_by_id(12))
    app.run(debug=True)


