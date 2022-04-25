# This module contains flask-sqlalchemy queries.
# It is needed to avoid circular imports in models.

from sqlalchemy import func

from api_university.models.student import StudentModel
from api_university.models.group import GroupModel
from api_university.models.course import CourseModel
from api_university.models.relationships import students_courses


class ComplexQuery:
    @staticmethod
    def get_students_filter_by_group_and_course(group_id: int, course_id: int):
        query = StudentModel.query\
                            .outerjoin(GroupModel)\
                            .outerjoin(students_courses)\
                            .outerjoin(CourseModel)\
                            .where(GroupModel.group_id == group_id,
                                   CourseModel.course_id == course_id)\
                            .order_by(StudentModel.student_id)
        return query.all()

    @staticmethod
    def get_groups_filter_by_student_count(student_count: int):
        query = GroupModel.query\
                          .outerjoin(StudentModel)\
                          .group_by(GroupModel.group_id)\
                          .having(func.count(StudentModel.student_id) <= student_count)\
                          .order_by(GroupModel.group_id)
        return query
