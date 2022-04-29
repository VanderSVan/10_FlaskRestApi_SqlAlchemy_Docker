from marshmallow import INCLUDE

from api_university.responses.response_strings import gettext_


class StudentListResponse:
    @classmethod
    def save_to_db(cls, schema, json):
        updated_students = schema.load(json, partial=True, unknown=INCLUDE)
        for updated_student in updated_students:
            updated_student.save_to_db()

    @staticmethod
    def create_response_for_put_method(updated_students: list,
                                       nonexistent_students: list,
                                       schema,
                                       json):
        if len(updated_students) == 0:
            tuple_output = ({'status': 404,
                             'message': gettext_("student_list_not_found").format(nonexistent_students)}, 404)

        elif len(nonexistent_students) == 0 and len(updated_students) != 0:
            StudentListResponse.save_to_db(schema, json)
            tuple_output = (
                {'status': 200,
                 'message': gettext_("student_list_put").format(updated_students)}, 200)

        else:
            StudentListResponse.save_to_db(schema, json)
            tuple_output = (
                {'status': 200,
                 'message': (gettext_("student_list_put").format(updated_students) + " and " +
                             gettext_("student_list_not_found").format(nonexistent_students))}, 200)
        return tuple_output

    @staticmethod
    def create_response_for_delete_method(deleted_students: list, nonexistent_students: list):

        if len(deleted_students) == 0:
            tuple_output = ({'status': 404,
                             'message': gettext_("student_list_not_found").format(nonexistent_students)}, 404)

        elif len(nonexistent_students) == 0 and len(deleted_students) != 0:
            tuple_output = (
                {'status': 200,
                 'message': gettext_("student_list_delete").format(deleted_students)}, 200)

        else:
            tuple_output = (
                {'status': 200,
                 'message': (gettext_("student_list_delete").format(deleted_students) + " and " +
                             gettext_("student_list_not_found").format(nonexistent_students))}, 200)
        return tuple_output
