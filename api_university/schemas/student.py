from marshmallow import Schema, fields, validate, pre_load, post_load
from flask import request, abort

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from .group import GroupSchema
from .course import CourseSchema


class ShortStudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StudentModel
        ordered = True

    student_id = ma.auto_field()
    first_name = ma.auto_field(validate=[validate.Length(min=1, max=50)])
    last_name = ma.auto_field(validate=[validate.Length(min=1, max=50)])
    group_name = ma.Function(lambda obj: None if obj.group is None else obj.group.name)
    course_names = ma.Function(lambda obj: ", ".join(list(map(lambda course: course.name, obj.courses))))


class FullStudentSchema(ma.SQLAlchemyAutoSchema):
    student_id = ma.auto_field()
    first_name = ma.auto_field(validate=[validate.Length(min=1, max=50)])
    last_name = ma.auto_field(validate=[validate.Length(min=1, max=50)])
    group_id = ma.auto_field()
    group = ma.Nested(GroupSchema(only=('group_id', 'name',)))
    courses = ma.Nested(CourseSchema(only=('course_id', 'name')), many=True)

    class Meta:
        model = StudentModel
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        load_only = ('group_id',)
        dump_only = ('group_id', 'courses')
        sqla_session = db.session

    @pre_load
    def process_data(self, data, **kwargs):
        if type(data) is dict:
            if request.method == 'POST':
                StudentModel.not_find_by_id_or_400(data.get('student_id'))
                if data.get('courses'):
                    data['courses'] = CourseModel.get_courses_by_ids(data['courses'])

            if request.method == 'PUT':
                if data.get('courses'):
                    abort(400, description="only 'add_courses' and 'delete_courses'"
                                           " fields are available in the 'PUT' method,"
                                           " but was given 'courses' field")

                student = StudentModel.find_by_id_or_404(data.get('student_id'))

                if data.get('add_courses'):
                    new_courses = CourseModel.get_courses_by_ids(data['add_courses'])
                    student.courses.extend(new_courses)

                if data.get('delete_courses'):
                    deletion_courses = CourseModel.get_courses_by_ids(data['delete_courses'])
                    student_courses_dict = dict.fromkeys(student.courses, True)
                    for course in deletion_courses:
                        student_courses_dict.pop(course, None)
                    student.courses = list(student_courses_dict)
        return data
