import pytest
import json

from api_university.config import Configuration as Config
from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from api_university.models.group import GroupModel
# from api_university.schemas.student import (ShortStudentSchema,
#                                             FullStudentSchema)
# from api_university.schemas.course import CourseSchema
from api_university.responses.response_strings import gettext_
# from tests.test_data.data import student_list

api_url = Config.API_URL

# test_short_student_schema = ShortStudentSchema()
# test_short_student_list_schema = ShortStudentSchema(many=True)
#
# test_full_student_schema = FullStudentSchema()
# test_full_student_list_schema = FullStudentSchema(many=True)
#
# full_course_list_schema = CourseSchema(many=True)

student_resources = {
    'student': "{}/students/{}",

    'full_student': "{}/students/{}?full=true",

    'student_list': "{}/students",
    'group_student_list': "{}/students?group={}",
    'course_student_list': "{}/students?course={}",
    'group&course_student_list': "{}/students?group={}&course={}",

    'full_student_list': "{}/students?full={}",
    'group_full_student_list': "{}/students?full={}&group={}",
    'course_full_student_list': "{}/students?full={}&course={}",
    'group&course_full_student_list': "{}/students?full={}&group={}&course={}",
}


# Student
@pytest.mark.parametrize("student_id", [1, 4, 5])
class TestGetStudent:
    # default (short schema)
    def test_get_default_student_schema(self, student_id, client):
        url = student_resources['student'].format(api_url, student_id)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
        assert response.json['student_id'] == student_id
        assert isinstance(response.json['first_name'], str) is True
        assert isinstance(response.json['last_name'], str) is True
        assert isinstance(response.json['group_name'], (str, type(None))) is True
        assert isinstance(response.json['course_names'], (str, type(None))) is True

    # full schema
    def test_get_full_student_schema(self, student_id, client):
        url = student_resources['full_student'].format(api_url, student_id)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        print(response.json)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json['student_id'] == student_id
        assert attrs_ == ['student_id', 'first_name', 'last_name', 'group', 'courses']
        assert isinstance(response.json['first_name'], str) is True
        assert isinstance(response.json['last_name'], str) is True
        assert isinstance(response.json['group'], (dict, type(None))) is True
        assert isinstance(response.json['courses'], list) is True


# StudentList
@pytest.mark.parametrize("group_id, course_id, student_count", [
    (None, None, 10),
    (2, None, 3),
    (None, 2, 5),
    (3, 3, 2),
    (1, 1, 3)
])
class TestGetStudentList:
    # default (short schema)
    def test_get_default_students_schema(self, group_id, course_id, student_count, client):
        if group_id:
            url = student_resources['group_student_list'].format(api_url, group_id)
        elif course_id:
            url = student_resources['course_student_list'].format(api_url, course_id)
        elif group_id and course_id:
            url = student_resources['group&course_student_list'].format(api_url, group_id, course_id)
        else:
            url = student_resources['student_list'].format(api_url)
        response = client.get(url)
        assert len(response.json) == student_count
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group_name'], (str, type(None))) is True
            assert isinstance(student['course_names'], (str, type(None))) is True

    # full schema
    def test_get_full_schema(self, group_id, course_id, student_count, client):
        if group_id:
            url = student_resources['group_full_student_list'].format(api_url, 'true', group_id)
        elif course_id:
            url = student_resources['course_full_student_list'].format(api_url, 'true', course_id)
        elif group_id and course_id:
            url = student_resources['group&course_full_student_list'].format(api_url, 'true', group_id, course_id)
        else:
            url = student_resources['full_student_list'].format(api_url, 'true')
        response = client.get(url)
        assert len(response.json) == student_count
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group', 'courses']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group'], (dict, type(None))) is True
            assert isinstance(student['courses'], list) is True


# @pytest.mark.parametrize("group, course, result", [
#     (None, None, student_list),
#     (2, None, [student_list[0], student_list[2], student_list[6]]),
#     (None, 2, [student_list[1], student_list[3], student_list[5],
#                student_list[8], student_list[9]]),
#     (3, 3, [student_list[7], student_list[9]])
# ])
# class TestGetStudentList:
#     # default (short schema)
#     def test_get_default_students_schema(self, group, course, result, client):
#         if group:
#             query_string = f"?group={group}"
#         elif course:
#             query_string = f"?course={course}"
#         elif group and course:
#             query_string = f"?group={group}&course={course}"
#         else:
#             query_string = "?"
#         response = client.get(f'{api_url}/students{query_string}')
#         output_json = json.loads(response.data)
#         assert response.status_code == 200
#         assert 'application/json' in response.headers['Content-Type']
#         assert len(output_json) == len(result)
#         assert output_json == test_short_student_list_schema.dump(result)
#
#     # full schema
#     def test_get_full_schema(self, group, course, result, client):
#         if group:
#             query_string = f"?full=true&group={group}"
#         elif course:
#             query_string = f"?full=true&course={course}"
#         elif group and course:
#             query_string = f"?full=true&group={group}&course={course}"
#         else:
#             query_string = "?full=true&"
#         response = client.get(f'{api_url}/students{query_string}')
#         output_json = json.loads(response.data)
#         assert response.status_code == 200
#         assert 'application/json' in response.headers['Content-Type']
#         assert len(output_json) == len(result)
#         assert output_json == test_full_student_list_schema.dump(result)


@pytest.mark.parametrize("wrong_data, status", [
    ('smth_wrong', 400),
    (1000, 404)
])
class TestGetStudentListExceptions:
    # default working
    def test_gives_wrong_full(self, wrong_data, status, client):
        url = student_resources['full_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == 10
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group_name'], (str, type(None))) is True
            assert isinstance(student['course_names'], (str, type(None))) is True

    def test_gives_wrong_group(self, wrong_data, status, client):
        url = student_resources['group_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        if isinstance(wrong_data, int):
            assert response.json == {'message': gettext_('group_not_found').format(wrong_data), 'status': 404}

    def test_gives_wrong_course(self, wrong_data, status, client):
        url = student_resources['course_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        if isinstance(wrong_data, int):
            assert response.json == {'message': gettext_('course_not_found').format(wrong_data), 'status': 404}


@pytest.mark.parametrize("json_to_send, result_json", [
    ([
         {
             "first_name": "John",
             "last_name": "Marlin"
         },
         {
             "first_name": "Alex",
             "last_name": "Brown",
             "group_id": 3,
             "courses": [1, 2]
         }
     ],
     {
         'message': gettext_("student_list_post").format([11, 12]),
         'status': 200
     })
])
class TestPostStudentList:
    def test_post(self, json_to_send, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert StudentModel.find_by_id(11) is not None
        assert StudentModel.find_by_id(12) is not None


@pytest.mark.parametrize("json_to_send, status, result_json", [
    # 0
    ([{"group_id": 3, "courses": [1, 2]}],
     400,
     {'err_name': 'ValidationError',
      'message': {'first_name': ['Missing data for required field.'],
                  'last_name': ['Missing data for required field.']},
      'status': 400}),
    # 1
    ([{"first_name": "John",
       "last_name": "Marlin",
       "group_id": 3000,
       "courses": [1, 2]}],
     400,
     {'err_name': 'IntegrityError',
      'message': 'FOREIGN KEY constraint failed',
      'status': 400}),
    # 2
    ([{"first_name": "John",
       "last_name": "Marlin",
       "group_id": 3,
       "courses": [1000, 20]}],
     404,
     {'message': gettext_("course_not_found").format(1000),
      'status': 404})
])
class TestPostStudentListExceptions:
    def test_post_wrong_student_list(self, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json


@pytest.mark.parametrize("json_to_send, result_json", [
    ([
         {
             "student_id": 1,
             "add_courses": [2, 3]
         },
         {
             "student_id": 2,
             "first_name": "Alex",
             "last_name": "Brown",
             "add_courses": [1],
             "delete_courses": [2],
             "group_id": 3
         }
     ],
     {
         'message': gettext_("student_list_put").format([1, 2]),
         'status': 200
     })
])
class TestPutStudentList:
    def test_put(self, json_to_send, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.put(url, json=json_to_send, headers=headers)
        student_1 = StudentModel.find_by_id(1)
        student_2 = StudentModel.find_by_id(2)
        student_2_full_name = student_2.first_name + student_2.last_name
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json

        assert student_1 in CourseModel.get_course_students(2)
        assert student_1 in CourseModel.get_course_students(3)

        assert student_2_full_name == json_to_send[1]['first_name'] + json_to_send[1]['last_name']
        assert student_2 in CourseModel.get_course_students(1)
        assert student_2 not in CourseModel.get_course_students(2)
        assert student_2 not in GroupModel.get_group_students(1)


@pytest.mark.parametrize("json_to_send, status, result_json", [
    # 0
    ([{}],
     404,
     {'message': gettext_("student_not_found").format(None),
      'status': 404}),
    # 1
    ([{"group_id": 3, "add_courses": [1, 2]}],
     404,
     {'message': gettext_("student_not_found").format(None),
      'status': 404}),
    # 2
    ([{"student_id": 3, "courses": [1, 2]}],
     400,
     {'message': gettext_("student_err_put_course"),
      'status': 400}),
    # 3
    ([{"student_id": 1,
       "group_id": 3000,
       "add_courses": [1, 2]}],
     400,
     {'err_name': 'IntegrityError',
      'message': 'FOREIGN KEY constraint failed',
      'status': 400}),
    # 4
    ([{"student_id": 2,
       "group_id": 3,
       "delete_courses": [1000, 20]}],
     404,
     {'message': gettext_("course_not_found").format(1000),
      'status': 404})
])
class TestPutStudentListExceptions:
    def test_put_wrong_student_list(self, json_to_send, status, result_json, session, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json


@pytest.mark.parametrize("json_to_send, result_json", [
    ({"student_id_list": [1, 2]},
     {'message': gettext_("student_list_delete").format([1, 2]),
      'status': 200}),

])
class TestDeleteStudentList:
    def test_delete(self, json_to_send, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.delete(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        for student_id in json_to_send["student_id_list"]:
            assert StudentModel.find_by_id(student_id) is None


@pytest.mark.parametrize("json_to_send, result_json, status", [
    ({"student_id_list": [3, 2000]},
     {'message': gettext_("student_list_delete").format([3]),
      'status': 200},
     200),
    ({"student_id_list": [5000, 2000]},
     {'message': gettext_("student_list_delete_err_no_one"),
      'status': 400},
     400),
    ({"student_id_list": ['a', 'b']},
     {'message': gettext_("student_list_delete_err_no_one"),
      'status': 400},
     400)
])
class TestDeleteStudentListExceptions:
    def test_delete_wrong_student_list(self, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student_list'].format(api_url)
        response = client.delete(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json
