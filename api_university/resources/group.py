from flask import request
from flask_restful import Resource
from flasgger import swag_from
from marshmallow import INCLUDE
from typing import OrderedDict

from api_university.config import swag_dir
from api_university.models.group import GroupModel
from api_university.schemas.group import GroupSchema
from api_university.db.sqlalchemy_queries.queries import ComplexQuery
from api_university.responses.response_strings import gettext_


short_group_schema = GroupSchema(only=('group_id', 'name',))
full_group_schema = GroupSchema()

short_group_list_schema = GroupSchema(many=True, only=('group_id', 'name',))
full_group_list_schema = GroupSchema(many=True)


class Group(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/Group/get.yml")
    def get(cls, group_id: int) -> tuple[OrderedDict, int]:
        group = GroupModel.find_by_id_or_404(group_id)
        if request.args.get('full', 'false').lower() == 'true':
            response = full_group_schema.dump(group), 200
        else:
            response = short_group_schema.dump(group), 200
        return response

    @classmethod
    @swag_from(f"{swag_dir}/Group/post.yml")
    def post(cls, group_id: int) -> tuple[dict, int]:
        group_json = request.get_json()
        group_json['group_id'] = group_id
        new_group = full_group_schema.load(group_json, unknown=INCLUDE)
        new_group.save_to_db()
        return {'status': 200, 'message': gettext_("group_post").format(group_id)}, 200

    @classmethod
    @swag_from(f"{swag_dir}/Group/put.yml")
    def put(cls, group_id: int) -> tuple[dict, int]:
        group_json = request.get_json()
        group_json['group_id'] = group_id
        updated_group = full_group_schema.load(group_json, partial=True, unknown=INCLUDE)
        print(updated_group.__dict__)
        updated_group.save_to_db()
        return {'status': 200, 'message': gettext_("group_put").format(group_id)}, 200
    
    @classmethod
    @swag_from(f"{swag_dir}/Group/delete.yml")
    def delete(cls, group_id: int) -> tuple[dict, int]:
        group = GroupModel.find_by_id_or_404(group_id)
        group.delete_from_db()
        return {'status': 200, 'message': gettext_("group_delete").format(group_id)}, 200


class GroupList(Resource):
    @classmethod
    @swag_from(f"{swag_dir}/GroupList/get.yml")
    def get(cls) -> tuple[OrderedDict, int]:
        student_count = request.args.get('student_count')
        if student_count:
            try:
                student_count = int(student_count)
            except Exception as err:
                print(err)
            groups = ComplexQuery.get_groups_filter_by_student_count(student_count)
        else:
            groups = GroupModel.get_all_groups()

        if request.args.get('full', 'false').lower() == 'true':
            response = full_group_list_schema.dump(groups), 200
        else:
            response = short_group_list_schema.dump(groups), 200
        return response
