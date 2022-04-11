from flask_restful import Resource
from api_report.models.group import GroupModel
from api_report.schemas.group import GroupSchema


group_schema = GroupSchema(many=True)


class Groups(Resource):
    @classmethod
    def get(cls):
        groups = GroupModel.get_all_groups()
        return group_schema.dump(groups), 200


class SearchGroup(Resource):
    @classmethod
    def get(cls, student_count):
        groups = GroupModel.get_groups_filter_by_student_count(student_count)
        return group_schema.dump(groups), 200
