from marshmallow import pre_load
from flask import request

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.models.group import GroupModel
from api_university.models.student import StudentModel


class GroupSchema(ma.SQLAlchemyAutoSchema):
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
                group = GroupModel.find_by_id_or_404(data.get('group_id'))
                if data.get('add_students'):
                    new_students = StudentModel.get_students_by_ids(data['add_students'])
                    group.students.extend(new_students)
                    print(group.students)
                if data.get('delete_students'):
                    deletion_students = StudentModel.get_students_by_ids(data['delete_students'])
                    group_student_dict = dict.fromkeys(group.students, True)
                    for student in deletion_students:
                        group_student_dict.pop(student, None)
                    group.students = list(group_student_dict)
                    print(group.students)
        return data
