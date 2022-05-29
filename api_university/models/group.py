from sqlalchemy import asc
from typing import NoReturn

from api_university.handlers import make_error
from api_university.db.db_sqlalchemy import db
from api_university.responses.response_strings import gettext_


class GroupModel(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    students = db.relationship('StudentModel',
                               backref=db.backref('group'),
                               order_by='StudentModel.student_id',
                               lazy=True)

    def __repr__(self):
        return f"GroupModel {self.group_id}"

    @classmethod
    def get_all_groups(cls) -> "GroupModel":
        return cls.query.order_by(asc(cls.group_id)).all()

    @classmethod
    def get_group_students(cls, group_id: int) -> "GroupModel":
        return cls.query.filter_by(group_id=group_id).first().students

    @classmethod
    def find_by_name(cls, group_name: str) -> "GroupModel":
        return cls.query.filter_by(name=group_name).first()

    @classmethod
    def find_by_id(cls, group_id: int) -> "GroupModel":
        return cls.query.filter_by(group_id=group_id).first()

    @classmethod
    def find_by_id_or_404(cls, group_id: int) -> "GroupModel":
        message = gettext_("group_not_found").format(group_id)
        status = 404
        return cls.query.get_or_404(group_id, make_error(status, message))

    @classmethod
    def not_find_by_id_or_400(cls, group_id: int) -> None:
        message = gettext_("group_exists").format(group_id)
        status = 400
        return cls.query.not_exists_or_400(group_id, make_error(status, message))

    def save_to_db(self) -> NoReturn:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> NoReturn:
        db.session.delete(self)
        db.session.commit()
