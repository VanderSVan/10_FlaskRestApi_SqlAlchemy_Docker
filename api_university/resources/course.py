from flask import request
from flask_restful import Resource
from flasgger import swag_from
from marshmallow import INCLUDE
from typing import OrderedDict

from api_university.config import swag_dir
from api_university.models.course import CourseModel
from api_university.schemas.course import CourseSchema
from api_university.responses.response_strings import gettext_
from api_university.resources.type_hintings import Query_parameter_value

short_course_schema = CourseSchema(only=('course_id', 'name',))
full_course_schema = CourseSchema()

short_course_list_schema = CourseSchema(many=True, only=('course_id', 'name',))
full_course_list_schema = CourseSchema(many=True)


class Course(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/Course/get.yml")
    def get(cls, course_id: int) -> tuple[OrderedDict, int]:
        course = CourseModel.find_by_id_or_404(course_id)
        full: Query_parameter_value = request.args.get('full', 'false').lower()
        match full:
            case 'true':
                return full_course_schema.dump(course), 200
            case _:
                return short_course_schema.dump(course), 200

    @classmethod
    @swag_from(f"{swag_dir}/Course/post.yml")
    def post(cls, course_id: int) -> tuple[dict, int]:
        course_json = request.get_json()
        course_json['course_id'] = course_id
        new_course = full_course_schema.load(course_json, unknown=INCLUDE)
        new_course.save_to_db()
        return {'status': 200, 'message': gettext_("course_post").format(course_id)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/Course/put.yml")
    def put(cls, course_id: int) -> tuple[dict, int]:
        course_json = request.get_json()
        course_json['course_id'] = course_id
        updated_course = full_course_schema.load(course_json, partial=True, unknown=INCLUDE)
        updated_course.save_to_db()
        return {'status': 200, 'message': gettext_("course_put").format(course_id)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/Course/delete.yml")
    def delete(cls, course_id: int) -> tuple[dict, int]:
        course = CourseModel.find_by_id_or_404(course_id)
        course.delete_from_db()
        return {'status': 200, 'message': gettext_("course_delete").format(course_id)}, 200


class CourseList(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/CourseList/get.yml")
    def get(cls) -> tuple[OrderedDict, int]:
        course_list = CourseModel.get_all_courses()
        full: Query_parameter_value = request.args.get('full', 'false').lower()
        match full:
            case 'true':
                return full_course_list_schema.dump(course_list), 200
            case _:
                return short_course_list_schema.dump(course_list), 200
