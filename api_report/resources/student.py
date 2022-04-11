from flask_restful import Resource
from api_report.models.student import StudentModel
from api_report.schemas.student import ShortStudentSchema, FullStudentSchema


short_student_schema = ShortStudentSchema()
short_students_schema = ShortStudentSchema(many=True)
full_student_schema = FullStudentSchema()
full_students_schema = FullStudentSchema(many=True)


class Student(Resource):
    @classmethod
    def get(cls, student_id):
        student = StudentModel.find_by_id(student_id)
        return short_student_schema.dump(student), 200


class Students(Resource):
    @classmethod
    def get(cls):
        students = StudentModel.get_all_students()
        return short_students_schema.dump(students), 200


class FullStudentStat(Resource):
    @classmethod
    def get(cls, student_id):
        full_stat_students = StudentModel.find_by_id(student_id)
        return full_student_schema.dump(full_stat_students), 200


class FullStudentsStat(Resource):
    @classmethod
    def get(cls):
        full_stat_students = StudentModel.get_all_students()
        return full_students_schema.dump(full_stat_students), 200

