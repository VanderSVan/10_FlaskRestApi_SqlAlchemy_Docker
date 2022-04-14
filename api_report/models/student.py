from api_report.db.db_sqlalchemy import db
from .relationships import students_courses
from sqlalchemy import func, asc


class StudentModel(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"))
    group = db.relationship('GroupModel')

    courses = db.relationship('CourseModel', secondary=students_courses,
                              backref=db.backref('all_students'),
                              lazy='subquery')

    @classmethod
    def find_by_id(cls, _id: int) -> "StudentModel":
        return cls.query.filter_by(student_id=_id).first()

    @classmethod
    def get_number_of_students(cls) -> "StudentModel":
        return cls.query.count()

    @classmethod
    def get_max_student_id(cls) -> "StudentModel":
        return cls.query.with_entities(func.max(cls.student_id)).first()

    @classmethod
    def get_all_students(cls) -> "StudentModel":
        return cls.query.order_by(asc(cls.student_id)).all()

    @classmethod
    def get_full_info(cls) -> "StudentModel":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
