from flask_restful import Resource
from api_report.models.course import CourseModel
from api_report.schemas.course import CourseSchema


course_schema = CourseSchema(many=True)


class Courses(Resource):
    @classmethod
    def get(cls):
        courses = CourseModel.get_all_courses()
        return course_schema.dump(courses), 200
