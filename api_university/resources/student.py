from flask import request
from flask_restful import Resource
from marshmallow import INCLUDE

from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from api_university.models.group import GroupModel
from api_university.schemas.student import ShortStudentSchema, FullStudentSchema
from api_university.sqlalchemy_queries.queries import ComplexQuery
from api_university.resources.utils import StudentListResponse

short_student_schema = ShortStudentSchema()
full_student_schema = FullStudentSchema()

short_student_list_schema = ShortStudentSchema(many=True)
full_student_list_schema = FullStudentSchema(many=True)


class Student(Resource):
    @classmethod
    def get(cls, student_id):
        """file: api_university/Swagger/Student/delete.yml"""
        student = StudentModel.find_by_id_or_404(student_id)
        if request.args.get('full', 'false').lower() == 'true':
            response = full_student_schema.dump(student), 200
        else:
            response = short_student_schema.dump(student), 200
        return response

    @classmethod
    def put(cls, student_id):
        """file: api_university/Swagger/Student/put.yml"""
        StudentModel.find_by_id_or_404(student_id)
        student_json = request.get_json()
        student_json['student_id'] = student_id
        updated_student = full_student_schema.load(student_json, partial=True, unknown=INCLUDE)
        updated_student.save_to_db()
        return {'status': 201, 'message': f"student '{student_id}' was successfully updated"}, 201

    @classmethod
    def post(cls, student_id):
        """file: api_university/Swagger/Student/put.yml"""
        student_json = request.get_json()
        student_json['student_id'] = student_id
        new_student = full_student_schema.load(student_json, unknown=INCLUDE)
        new_student.save_to_db()
        return {'status': 201, 'message': f"student '{student_id}' was successfully created"}, 201

    @classmethod
    def delete(cls, student_id):
        """file: api_university/Swagger/StudentList/post.yml"""
        student = StudentModel.find_by_id_or_404(student_id)
        student.delete_from_db()
        return {'status': 200, 'message': f"student '{student_id}' was successfully deleted"}, 200


class StudentList(Resource):
    @classmethod
    def get(cls):
        """file: api_university/Swagger/StudentList/get.yml"""
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
    def put(cls):
        """file: api_university/Swagger/StudentList/put.yml"""
        student_list_json = request.get_json()
        updated_students = []
        nonexistent_students = []
        for student_json in student_list_json:
            student_id = student_json.get('student_id')
            student = StudentModel.find_by_id(student_id)
            if student:
                updated_students.append(student_id)
            else:
                nonexistent_students.append(student_id)
        return StudentListResponse.create_response_for_put_method(updated_students,
                                                                  nonexistent_students,
                                                                  full_student_list_schema,
                                                                  student_list_json)

    @classmethod
    def post(cls):
        """file: api_university/Swagger/StudentList/post.yml"""
        max_student_id, = StudentModel.get_max_student_id()
        print(StudentModel.get_max_student_id())
        student_list_json = request.get_json()

        for student_json in student_list_json:
            max_student_id += 1
            student_json['student_id'] = max_student_id

        new_students = full_student_list_schema.load(student_list_json, unknown=INCLUDE)
        added_students_counter = []
        for student in new_students:
            student.save_to_db()
            added_students_counter.append(student.student_id)
        return {'status': 201,
                'message': f"students '{added_students_counter}' were successfully added"}, 201

    @classmethod
    def delete(cls):
        """file: api_university/Swagger/StudentList/post.yml"""
        deletion_students_json = request.get_json()
        student_id_list = deletion_students_json.get('student_id_list')
        if student_id_list:
            nonexistent_students = []
            deleted_students = []
            for student_id in student_id_list:
                student = StudentModel.find_by_id(student_id)
                if not student:
                    nonexistent_students.append(student_id)
                else:
                    student.delete_from_db()
                    deleted_students.append(student_id)
            return StudentListResponse.create_response_for_delete_method(deleted_students, nonexistent_students)
