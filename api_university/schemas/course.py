from marshmallow import validate, pre_load
from flask import request, abort

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.models.course import CourseModel
from api_university.models.student import StudentModel


class CourseSchema(ma.SQLAlchemyAutoSchema):
    name = ma.auto_field(validate=[validate.Length(min=1, max=100)])
    description = ma.auto_field(validate=[validate.Length(min=1, max=300)])

    class Meta:
        model = CourseModel
        fields = ('course_id', 'name', 'description', 'students')
        dump_only = ("course_id",)
        include_relationships = True
        ordered = True
        load_instance = True
        sqla_session = db.session

    @pre_load
    def process_data(self, data, **kwargs):
        if type(data) is dict:
            if request.method == 'POST':
                CourseModel.not_find_by_id_or_400(data.get('course_id'))
            if request.method == 'PUT':
                if data.get('students'):
                    abort(400, description="only 'add_students' and 'delete_students'"
                                           " fields are available in the 'PUT' method,"
                                           " but was given 'students' field")

                course = CourseModel.find_by_id_or_404(data.get('course_id'))

                if data.get('add_students'):
                    new_students = StudentModel.get_students_by_ids(data['add_students'])
                    course.students.extend(new_students)

                if data.get('delete_students'):
                    deletion_students = StudentModel.get_students_by_ids(data['delete_students'])
                    course_students_dict = dict.fromkeys(course.students, True)
                    for student in deletion_students:
                        course_students_dict.pop(student, None)
                    course.students = list(course_students_dict)
        return data
