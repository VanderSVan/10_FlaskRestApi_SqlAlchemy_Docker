from flask import request
from flask_restful import Resource
from marshmallow import INCLUDE

from api_university.models.group import GroupModel
from api_university.schemas.group import GroupSchema
from api_university.sqlalchemy_queries.queries import ComplexQuery


short_group_schema = GroupSchema(only=('group_id', 'name',))
full_group_schema = GroupSchema()

short_group_list_schema = GroupSchema(many=True, only=('group_id', 'name',))
full_group_list_schema = GroupSchema(many=True)


class Group(Resource):
    @classmethod
    def get(cls, group_id):
        """file: api_university/Swagger/Group/get.yml"""
        group = GroupModel.find_by_id_or_404(group_id)
        if request.args.get('full', 'false').lower() == 'true':
            response = full_group_schema.dump(group), 200
        else:
            response = short_group_schema.dump(group), 200
        return response

    @classmethod
    def post(cls, group_id):
        """file: api_university/Swagger/Group/post.yml"""
        group_json = request.get_json()
        group_json['group_id'] = group_id
        new_group = full_group_schema.load(group_json, unknown=INCLUDE)
        new_group.save_to_db()
        return {'status': 201, 'message': f"group '{group_id}' was successfully created"}, 201

    @classmethod
    def put(cls, group_id):
        """file: api_university/Swagger/Group/put.yml"""
        group_json = request.get_json()
        group_json['group_id'] = group_id
        updated_group = full_group_schema.load(group_json, partial=True, unknown=INCLUDE)
        print(updated_group.__dict__)
        updated_group.save_to_db()
        return {'status': 201, 'message': f"group '{group_id}' was successfully updated"}, 201
    
    @classmethod
    def delete(cls, group_id):
        """file: api_university/Swagger/Group/delete.yml"""
        group = GroupModel.find_by_id_or_404(group_id)
        group.delete_from_db()
        return {'status': 200, 'message': f"group '{group_id}' was successfully deleted"}, 200


class GroupList(Resource):
    @classmethod
    def get(cls):
        """file: api_university/Swagger/GroupList/get.yml"""
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
