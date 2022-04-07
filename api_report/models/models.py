from api_report.db.db_sqlalchemy import db

# relationship many to many
students_courses = db.Table('students_courses',
                            db.Column('student_id', db.Integer, db.ForeignKey('students.student_id')),
                            db.Column('course_id', db.Integer, db.ForeignKey('courses.course_id'))
                            )


class GroupModel(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class StudentModel(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    courses = db.relationship('CourseModel', secondary=students_courses,
                              backref=db.backref('all_students'),
                              lazy='dynamic')


class CourseModel(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    # students = db.relationship('StudentModel', secondary=students_courses, backref=db.backref("all_courses"))
    # # students = db.relationship('StudentModel', backref="courses")
