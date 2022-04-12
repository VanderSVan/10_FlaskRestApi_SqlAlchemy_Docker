from sqlalchemy import asc
from api_report.db.db_sqlalchemy import db


class GroupModel(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    students = db.relationship('StudentModel', back_populates="group",
                               order_by='StudentModel.student_id')

    @classmethod
    def get_all_groups(cls):
        return cls.query.order_by(asc(cls.group_id))

    # @classmethod
    # def get_groups_filter_by_student_count(cls, student_count: int):
    #     query = cls.query.with_entities(cls.group_id, cls.name).\
    #         outerjoin(StudentModel).\
    #         group_by(cls.group_id).\
    #         having(func.count(StudentModel.student_id) <= student_count)
    #     print(query)
    #     return query
