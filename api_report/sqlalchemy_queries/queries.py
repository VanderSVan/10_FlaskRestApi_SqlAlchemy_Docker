# This module contains flask-sqlalchemy queries.
# It is needed to avoid circular imports in models.

from sqlalchemy import func

from api_report.models.student import StudentModel
from api_report.models.group import GroupModel


class ComplexQueries:
    @staticmethod
    def get_students_from_group(group_name: str):
        query = StudentModel.query\
                            .outerjoin(GroupModel)\
                            .filter_by(name=group_name)\
                            .order_by(StudentModel.student_id)
        return query

    @staticmethod
    def get_groups_filter_by_student_count(student_count: int):
        query = GroupModel.query\
                          .outerjoin(StudentModel)\
                          .group_by(GroupModel.group_id)\
                          .having(func.count(StudentModel.student_id) <= student_count)\
                          .order_by(GroupModel.group_id)
        return query
