from marshmallow import validate, pre_load
from flask import request, abort

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.models.group import GroupModel
from api_university.models.student import StudentModel


class GroupSchema(ma.SQLAlchemyAutoSchema):
    name = ma.auto_field(validate=[validate.Length(min=1, max=100)])

    class Meta:
        model = GroupModel
        fields = ('group_id', 'name', 'students')
        include_relationships = True
        ordered = True
        load_instance = True
        sqla_session = db.session

    @pre_load
    def process_data(self, data, **kwargs):
        if type(data) is dict:
            if request.method == 'POST':
                GroupModel.not_find_by_id_or_400(data.get('group_id'))
            if request.method == 'PUT':
                if data.get('students'):
                    abort(400, description="only 'add_students' and 'delete_students'"
                                           " fields are available in the 'PUT' method,"
                                           " but was given 'students' field")

                group = GroupModel.find_by_id_or_404(data.get('group_id'))

                if data.get('add_students'):
                    new_students = StudentModel.get_students_by_ids(data['add_students'])
                    group.students.extend(new_students)

                if data.get('delete_students'):
                    deletion_students = StudentModel.get_students_by_ids(data['delete_students'])
                    group_student_dict = dict.fromkeys(group.students, True)
                    for student in deletion_students:
                        group_student_dict.pop(student, None)
                    group.students = list(group_student_dict)
        return data
