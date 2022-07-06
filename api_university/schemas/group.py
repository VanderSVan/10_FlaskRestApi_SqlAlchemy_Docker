from marshmallow import validate, pre_load
from flask import request, abort

from api_university.db.db_sqlalchemy import db
from api_university.ma import ma
from api_university.handlers import make_error
from api_university.responses.response_strings import gettext_
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
    def process_data(self, data: dict, **kwargs):
        if isinstance(data, dict):
            method = request.method
            match method:
                case 'POST':
                    GroupModel.not_find_by_id_or_400(data.get('group_id'))
                    StudentModel.get_students_by_ids_or_404(data.get('students'))
                case 'PUT':
                    group = GroupModel.find_by_id_or_404(data.get('group_id'))

                    if data.get('students'):
                        message = gettext_("group_err_put_students")
                        status = 400
                        abort(make_error(status, message))

                    if data.get('add_students'):
                        new_students = StudentModel.get_students_by_ids_or_404(data['add_students'])
                        group.students.extend(new_students)

                    if data.get('delete_students'):
                        deletion_students = StudentModel.get_students_by_ids_or_404(data['delete_students'])
                        group_student_dict = dict.fromkeys(group.students, True)
                        for student in deletion_students:
                            group_student_dict.pop(student, None)
                        group.students = list(group_student_dict)
        return data
