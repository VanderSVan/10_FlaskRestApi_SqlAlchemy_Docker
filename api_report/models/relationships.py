from api_report.db.db_sqlalchemy import db

# relationship many to many
students_courses = db.Table('students_courses',
                            db.Column('student_id', db.Integer, db.ForeignKey('students.student_id')),
                            db.Column('course_id', db.Integer, db.ForeignKey('courses.course_id'))
                            )
