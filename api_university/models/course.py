from sqlalchemy import asc
from api_university.db.db_sqlalchemy import db
from .relationships import students_courses


class CourseModel(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    students = db.relationship('StudentModel',
                               secondary='students_courses',
                               backref=db.backref('courses',
                                                  order_by='CourseModel.course_id.asc()'),
                               order_by='StudentModel.student_id.asc()')

    def __repr__(self):
        return f"CourseModel {self.course_id}"

    @classmethod
    def get_all_courses(cls):
        return cls.query.order_by(asc(cls.course_id))

    @classmethod
    def get_course_students(cls, course_id):
        return cls.query.filter_by(course_id=course_id).first().students

    @classmethod
    def find_by_name(cls, course_name: str) -> "CourseModel":
        return cls.query.filter_by(name=course_name).first()

    @classmethod
    def find_by_id_or_404(cls, course_id: int) -> "CourseModel":
        return cls.query.get_or_404(course_id, description=f"course '{course_id}' not found")

    @classmethod
    def not_find_by_id_or_400(cls, course_id: int) -> None:
        return cls.query.not_exists_or_400(course_id, description=f"course '{course_id}' already exists")

    @classmethod
    def get_courses_by_ids(cls, course_ids: list) -> list["CourseModel"] or None:
        if course_ids is None:
            selected_courses = None
        else:
            selected_courses = [cls.find_by_id_or_404(course) for course in course_ids]
        return selected_courses

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
