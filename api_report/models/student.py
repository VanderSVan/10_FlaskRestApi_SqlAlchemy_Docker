from api_report.db.db_sqlalchemy import db
from .relationships import students_courses


class StudentModel(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"), nullable=False)
    courses = db.relationship('CourseModel', secondary=students_courses,
                              backref=db.backref('all_students'),
                              lazy='dynamic')

    @staticmethod
    def get_all_students():
        return StudentModel.query.all()
