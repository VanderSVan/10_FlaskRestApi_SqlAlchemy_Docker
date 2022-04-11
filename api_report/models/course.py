from sqlalchemy import asc
from api_report.db.db_sqlalchemy import db


class CourseModel(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    students = db.relationship('StudentModel', secondary='students_courses',
                               back_populates="courses", overlaps="all_students",
                               order_by='StudentModel.student_id')

    @classmethod
    def get_all_courses(cls):
        return cls.query.order_by(asc(cls.course_id))
