from flask import request
from flask_restful import Resource, abort
from flasgger import swag_from
from marshmallow import INCLUDE

from api_university.config import swag_dir
from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from api_university.models.group import GroupModel
from api_university.schemas.student import ShortStudentSchema, FullStudentSchema
from api_university.sqlalchemy_queries.queries import ComplexQuery
from api_university.resources.utils import StudentListResponse
from api_university.responses.response_strings import gettext_
from api_university.handlers import make_error

short_student_schema = ShortStudentSchema()
full_student_schema = FullStudentSchema()

short_student_list_schema = ShortStudentSchema(many=True)
full_student_list_schema = FullStudentSchema(many=True)


class Student(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/Student/get.yml")
    def get(cls, student_id):
        student = StudentModel.find_by_id_or_404(student_id)
        if request.args.get('full', 'false').lower() == 'true':
            response = full_student_schema.dump(student), 200
        else:
            response = short_student_schema.dump(student), 200
        return response

    @classmethod
    @swag_from(f"{swag_dir}/Student/post.yml")
    def post(cls, student_id):
        student_json = request.get_json()
        student_json['student_id'] = student_id
        new_student = full_student_schema.load(student_json, unknown=INCLUDE)
        new_student.save_to_db()
        return {'status': 200, 'message': gettext_("student_post").format(student_id)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/Student/put.yml")
    def put(cls, student_id):
        StudentModel.find_by_id_or_404(student_id)
        student_json = request.get_json()
        student_json['student_id'] = student_id
        updated_student = full_student_schema.load(student_json, partial=True, unknown=INCLUDE)
        updated_student.save_to_db()
        return {'status': 200, 'message': gettext_("student_put").format(student_id)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/Student/delete.yml")
    def delete(cls, student_id):
        student = StudentModel.find_by_id_or_404(student_id)
        student.delete_from_db()
        return {'status': 200, 'message': gettext_("student_delete").format(student_id)}, 200


class StudentList(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/StudentList/get.yml")
    def get(cls):
        group_id = request.args.get('group')
        course_id = request.args.get('course')

        if group_id and course_id:
            student_list = ComplexQuery.get_students_filter_by_group_and_course(int(group_id), int(course_id))
        elif group_id:
            group_obj = GroupModel.find_by_id_or_404(int(group_id))
            student_list = group_obj.students
        elif course_id:
            course_obj = CourseModel.find_by_id_or_404(int(course_id))
            student_list = course_obj.students
        else:
            student_list = StudentModel.get_all_students()

        if request.args.get('full', 'false').lower() == 'true':
            response = full_student_list_schema.dump(student_list), 200
        else:
            response = short_student_list_schema.dump(student_list), 200

        return response

    @classmethod
    @swag_from(f"{swag_dir}/StudentList/post.yml")
    def post(cls):
        max_student_id = StudentModel.get_max_student_id()
        student_list_json = request.get_json()

        for student_json in student_list_json:
            max_student_id += 1
            student_json['student_id'] = max_student_id

        new_students = full_student_list_schema.load(student_list_json, unknown=INCLUDE)
        added_students_counter = []
        for student in new_students:
            student.save_to_db()
            added_students_counter.append(student.student_id)

        return {'status': 200,
                'message': gettext_("student_list_post").format(added_students_counter)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/StudentList/put.yml")
    def put(cls):
        student_list_json = request.get_json()
        updated_students = full_student_list_schema.load(student_list_json, partial=True, unknown=INCLUDE)
        updated_students_counter = []
        for student in updated_students:
            student.save_to_db()
            updated_students_counter.append(student.student_id)

        return {'status': 200,
                'message': gettext_("student_list_put").format(updated_students_counter)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/StudentList/delete.yml")
    def delete(cls):
        student_list_json = request.get_json()
        student_id_list = student_list_json.get('student_id_list')
        if not student_id_list:
            response = {'status': 400,
                        'message': gettext_("student_list_delete_err_missing")}, 400
        else:
            deleted_students_counter = []
            for student_id in student_list_json.get('student_id_list'):
                student = StudentModel.find_by_id(student_id)
                if student:
                    student.delete_from_db()
                    deleted_students_counter.append(student.student_id)
            if deleted_students_counter:
                response = {'status': 200,
                            'message': gettext_("student_list_delete").format(deleted_students_counter)}, 200
            else:
                response = {'status': 400,
                            'message': gettext_("student_list_delete_err_no_one").format(deleted_students_counter)}, 400
        return response
