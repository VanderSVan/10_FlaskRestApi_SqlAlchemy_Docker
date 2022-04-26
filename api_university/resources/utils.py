from marshmallow import INCLUDE


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
                             'message': f"students '{nonexistent_students}' not found "}, 404)
        elif len(nonexistent_students) == 0 and len(updated_students) != 0:
            StudentListResponse.save_to_db(schema, json)
            tuple_output = (
                {'status': 200,
                 'message': f"students '{updated_students}' were successfully updated"}, 200)
        else:
            StudentListResponse.save_to_db(schema, json)
            tuple_output = (
                {'status': 200,
                 'message': f"students '{updated_students}' were successfully updated and "
                            f"students '{nonexistent_students}' not found"}, 200)
        return tuple_output

    @staticmethod
    def create_response_for_delete_method(deleted_students: list, nonexistent_students: list):
        if len(deleted_students) == 0:
            tuple_output = ({'status': 404,
                             'message': f"students '{nonexistent_students}' not found "}, 404)
        elif len(nonexistent_students) == 0 and len(deleted_students) != 0:
            tuple_output = (
                {'status': 200,
                 'message': f"students '{deleted_students}' were successfully deleted"}, 200)
        else:
            tuple_output = (
                {'status': 200,
                 'message': f"students '{deleted_students}' were successfully deleted and "
                            f"students '{nonexistent_students}' not found"}, 200)
        return tuple_output


# def set_new_values_for_student(student, json, course_model):
#     for key, new_value in json.items():
#         getattr(student, key)
#         if key == 'courses':
#             correct_course_objs = course_model.get_courses_by_ids(json.get('courses'))
#             setattr(student, key, correct_course_objs)
#         else:
#             setattr(student, key, new_value)


# def _get_json_default_error(err: Exception):
#     return {'status': 400,
#             'message': f'{err}',
#             'type error': f'{type(err)}'}

