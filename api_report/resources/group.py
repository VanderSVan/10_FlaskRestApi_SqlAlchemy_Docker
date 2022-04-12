from flask import request
from flask_restful import Resource
from api_report.models.group import GroupModel
from api_report.schemas.group import GroupSchema
from api_report.sqlalchemy_queries.queries import ComplexQueries


group_schema = GroupSchema(many=True)


class Groups(Resource):
    @classmethod
    def get(cls):
        """file: api_report/Swagger/Groups/get.yml"""
        student_count = request.args.get('student_count')
        if student_count:
            try:
                student_count = int(student_count)
            except Exception as err:
                print(err)
            groups = ComplexQueries.get_groups_filter_by_student_count(student_count)
        else:
            groups = GroupModel.get_all_groups()
        return group_schema.dump(groups), 200


# class SearchGroup(Resource):
#     @classmethod
#     def get(cls, student_count: int):
#         groups = ComplexQueries.get_groups_filter_by_student_count(student_count)
#         return group_schema.dump(groups), 200
