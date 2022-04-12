from flask import request, make_response, jsonify
from flask_restful import Resource
from api_report.models.student import StudentModel
from api_report.schemas.student import ShortStudentSchema, FullStudentSchema
from api_report.sqlalchemy_queries.queries import ComplexQueries

short_student_schema = ShortStudentSchema()
short_students_schema = ShortStudentSchema(many=True)
full_student_schema = FullStudentSchema()
full_students_schema = FullStudentSchema(many=True)


class Student(Resource):
    @classmethod
    def get(cls, student_id):
        """file: api_report/Swagger/Student/get.yml"""
        student = StudentModel.find_by_id(student_id)
        if request.args.get('full') == 'yes':
            return full_student_schema.dump(student), 200

        return short_student_schema.dump(student), 200


class StudentList(Resource):
    @classmethod
    def get(cls):
        """file: api_report/Swagger/StudentList/get.yml"""
        full_stat = request.args.get('full')
        group_name = request.args.get('group')
        if group_name:
            student_list = ComplexQueries.get_students_from_group(group_name)
        else:
            student_list = StudentModel.get_all_students()
        if full_stat == 'yes':
            return full_students_schema.dump(student_list), 200

        return short_students_schema.dump(student_list), 200

    # @classmethod
    # def post(cls):
    #     """file: api_report/Swagger/StudentList/post.yml"""
    #     student_json = request.get_json()
    #     student = short_student_schema.load(student_json)
    #
    #     student.save_to_db()
    #
    #     return make_response(jsonify({'status': 200, 'message': 'user_registered'}), 200)
