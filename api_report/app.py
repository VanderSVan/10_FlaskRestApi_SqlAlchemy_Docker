from flask import Flask
from flask_restful import Api
from api_report.db.data_insertion_into_db import insert_data_to_db
from api_report.resources.student import Student, Students, FullStudentStat, FullStudentsStat
from api_report.resources.course import Courses
from api_report.resources.group import Groups, SearchGroup


def create_app(test_config=False):
    application = Flask(__name__)

    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:1111@localhost:5432/university"
    application.config['JSON_SORT_KEYS'] = False
    api = Api(application)

    @application.before_first_request
    def create_tables():
        db.create_all()

        insert_data_to_db(db)

        db.session.commit()
        print('Tables has been created')
    if test_config:
        application.config['TESTING'] = True

    # RESOURCES:
    # Student
    api.add_resource(Students, "/students")
    api.add_resource(Student, "/students/<int:student_id>")
    api.add_resource(FullStudentsStat, "/students/stat")
    api.add_resource(FullStudentStat, "/students/stat/<int:student_id>")

    # Courses
    api.add_resource(Courses, "/courses")

    # Groups
    api.add_resource(Groups, "/groups")
    api.add_resource(SearchGroup, "/groups/<int:student_count>")
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


