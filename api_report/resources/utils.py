from flask import jsonify


class StudentListResponse:
    @staticmethod
    def create_response_for_post_method(added_students: list):
        return {'status': 201,
                'message': f"students '{added_students}' were successfully added"}, 201

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


json_value_error = {'status': 400,
                    'message': f"student_ids must have only sequence of integers"}


def _get_json_default_error(err: Exception):
    return {'status': 400,
            'message': f'{err}',
            'type error': f'{type(err)}'}


def handle_query_string(output_val_err):
    def outer_wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except ValueError as val_err:
                print('Got ValueError =', val_err)
                return jsonify(output_val_err)
            except Exception as default_err:
                print(f"Got an type Exception: {type(default_err)} "
                      f"message: {default_err}")
                return jsonify(_get_json_default_error(default_err))

        return inner_wrapper

    return outer_wrapper


@handle_query_string(json_value_error)
def _convert_string_to_int_list(str_: str, separator: str):
    str_list = str_.split(separator)
    return [int(string_.strip()) for string_ in str_list]
