# This module contains flask-sqlalchemy queries.
# It is needed to avoid circular imports in models.

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
