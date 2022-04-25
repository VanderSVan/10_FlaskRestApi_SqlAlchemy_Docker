from marshmallow import Schema, fields, validate, pre_load, post_load
from flask import abort
from api_report.db.db_sqlalchemy import db
from api_report.ma import ma
from api_report.models.student import StudentModel
from api_report.models.course import CourseModel
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
        load_only = ('group_id', )
        dump_only = ('group_id', 'courses')
        sqla_session = db.session

    @pre_load
    def process_data(self, data, **kwargs):
        if data.get('courses'):
            data['courses'] = CourseModel.get_courses_by_ids(data['courses'])
        return data


# # pure marshmallow
# class FullStudentSchema(Schema):
#     student_id = fields.Integer(required=True, dump_only=True)
#     first_name = fields.String(required=True,
#                                validate=[validate.Length(min=1, max=50)])
#     last_name = fields.String(required=True,
#                               validate=[validate.Length(min=1, max=50)])
#
#     group_id = fields.Integer(dump_only=True)
#
#     group = ma.Nested(GroupSchema(only=('name',)), dump_only=True)
#     courses = fields.Nested(CourseSchema(only=('course_id', 'name')), many=True, dump_only=True)
#
#     class Meta:
#         ordered = True
#
#     @pre_load
#     def process_data(self, data, **kwargs):
#         existent_student = StudentModel.find_by_id(data.pop('student_id'))
#         print(existent_student)
#         if data.get('first_name'):
#             data['first_name'] = " ".join(data['first_name'].title().split())
#         else:
#             data['first_name'] = existent_student.first_name
#         if data.get('last_name'):
#             data['last_name'] = " ".join(data['last_name'].title().split())
#         else:
#             data['last_name'] = existent_student.last_name
#         if data.get('courses'):
#             data['courses'] = CourseModel.get_courses_by_ids(data['courses'])
#         print(data)
#         return data
#
#     @post_load
#     def make_student_obj(self, data, **kwargs):
#         return StudentModel(**data)
