import pytest

from api_university.config import Configuration as Config
from api_university.models.student import StudentModel
from api_university.models.course import CourseModel
from api_university.models.group import GroupModel
from api_university.responses.response_strings import gettext_

from tests.test_data.data import student_count

api_url = Config.API_URL

student_resources = {
    'student': "{}/students/{}",

    'full_student': "{}/students/{}?full={}",

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

class TestStudent:
    @pytest.mark.parametrize("student_id", [1, 3, 5])
    # default (short schema)
    def test_get_default_schema(self, student_id, client):
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

    @pytest.mark.parametrize("student_id", [2, 4, 6])
    # full schema
    def test_get_full_schema(self, student_id, client):
        url = student_resources['full_student'].format(api_url, student_id, 'true')
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

    @pytest.mark.parametrize("student_id, json_to_send, result_json, group_id, course_count", [
        (
                11,
                {"first_name": "John",
                 "last_name": "Marlin"},
                {'message': gettext_("student_post").format(11),
                 'status': 200},
                None,
                0
        ),
        (
                12,
                {"first_name": "Alex",
                 "last_name": "Brown",
                 "group_id": 1,
                 "courses": [1, 2, 3]},
                {'message': gettext_("student_post").format(12),
                 'status': 200},
                1,
                3
        )
    ])
    def test_post(self, student_id, json_to_send, result_json, group_id, course_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student'].format(api_url, student_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert StudentModel.find_by_id(student_id) is not None
        assert StudentModel.find_by_id(student_id).group_id == group_id
        assert len(StudentModel.find_by_id(student_id).courses) == course_count

    @pytest.mark.parametrize("student_id, json_to_send, result_json, group_id, course_count", [
        (
                2,
                {"add_courses": [1],
                 "delete_courses": [2, 3],
                 "group_id": 2},
                {'message': gettext_("student_put").format(2),
                 'status': 200},
                2,
                1
        ),
        (
                3,
                {"first_name": "Somebody",
                 "last_name": "Everybody"},
                {'message': gettext_("student_put").format(3),
                 'status': 200},
                2,
                1
        )
    ])
    def test_put(self, student_id, json_to_send, result_json, group_id, course_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student'].format(api_url, student_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert StudentModel.find_by_id(student_id).group_id == group_id
        assert len(StudentModel.find_by_id(student_id).courses) == course_count

    @pytest.mark.parametrize("student_id, result_json, remaining_student_count", [
        (
                2,
                {'message': gettext_("student_delete").format(2),
                 'status': 200},
                9

        ),
        (
                3,
                {'message': gettext_("student_delete").format(3),
                 'status': 200},
                9
        )
    ])
    def test_delete(self, student_id, result_json, remaining_student_count, client):
        url = student_resources['student'].format(api_url, student_id)
        response = client.delete(url)
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == result_json
        assert len(StudentModel.get_all_students()) == remaining_student_count


class TestStudentException:
    @pytest.mark.parametrize("student_id, wrong_data", [(1, 'smth_wrong'), (2, 1000)])
    # wrong query string "?full="
    def test_get_wrong_full(self, student_id, wrong_data, client):
        url = student_resources['full_student'].format(api_url, student_id, wrong_data)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        student_data = response.json
        attrs_ = list(student_data.keys())
        assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
        assert isinstance(student_data['first_name'], str) is True
        assert isinstance(student_data['last_name'], str) is True
        assert isinstance(student_data['group_name'], (str, type(None))) is True
        assert isinstance(student_data['course_names'], (str, type(None))) is True

    @pytest.mark.parametrize("student_id, json_to_send, status, result_json", [
        # 0 don't give required field:
        (
                15,
                {"group_id": 3, "courses": [1, 2]},
                400,
                {'err_name': 'ValidationError',
                 'message': {'first_name': ['Missing data for required field.'],
                             'last_name': ['Missing data for required field.']},
                 'status': 400}
        ),
        # 1 incorrect foreign key of group_id:
        pytest.param(
            15,
            {"first_name": "John",
             "last_name": "Marlin",
             "group_id": 3000,
             "courses": [1, 2]},
            400,
            {'err_name': 'IntegrityError',
             'message': 'FOREIGN KEY constraint failed',
             'status': 400},
            marks=pytest.mark.xfail(reason='incorrect foreign key of group_id')
        ),
        # 2 incorrect course_id:
        (
                15,
                {"first_name": "John",
                 "last_name": "Marlin",
                 "group_id": 3,
                 "courses": [1000, 20]},
                404,
                {'message': gettext_("course_not_found").format(1000),
                 'status': 404}
        )
    ])
    def test_post_wrong_student(self, student_id, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student'].format(api_url, student_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("student_id, json_to_send, status, result_json", [
        # 0 student not found:
        (
                1000,
                {"group_id": 3, "add_courses": [1, 2]},
                404,
                {'message': gettext_("student_not_found").format(1000),
                 'status': 404}
        ),
        # 1 give 'courses' list instead of 'add_courses' and 'delete_courses' lists:
        (
                1,
                {"student_id": 3, "courses": [1, 2]},
                400,
                {'message': gettext_("student_err_put_courses"),
                 'status': 400}
        ),
        # 2 incorrect group_id (foreign key):
        pytest.param(
            1,
            {"student_id": 1,
             "group_id": 3000,
             "add_courses": [1, 2]},
            400,
            {'err_name': 'IntegrityError',
             'message': 'FOREIGN KEY constraint failed',
             'status': 400},
            marks=pytest.mark.xfail(reason='incorrect input data: give nonexistence group_id')
        ),
        # 3 give nonexistent courses:
        (
                1,
                {"student_id": 5,
                 "group_id": 3,
                 "delete_courses": [1000, 20]},
                404,
                {'message': gettext_("course_not_found").format(1000),
                 'status': 404}
        )
    ])
    def test_put_wrong_student(self, student_id, json_to_send, status, result_json, session, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student'].format(api_url, student_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("student_id, result_json, status", [
        # 0 give incorrect student_id (delete nonexistence students)
        (
                1000,
                {'message': gettext_("student_not_found").format(1000),
                 'status': 404},
                404
        ),
        # 1 give incorrect type student_id
        (
                "a",
                {'message': '404 Not Found: The requested URL was not found on the server. If '
                            'you entered the URL manually please check your spelling and try '
                            'again.',
                 'status': 404},
                404,
        )
    ])
    def test_delete_wrong_student(self, student_id, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = student_resources['student'].format(api_url, student_id)
        response = client.delete(url, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json


class TestStudentList:
    @pytest.mark.parametrize("group_id, course_id, number_of_student", [
        (None, None, 10),
        (2, None, 3),
        (None, 2, 5),
        (3, 3, 2),
        (1, 1, 3)
    ])
    # default (short schema)
    def test_get_default_schema(self, group_id, course_id, number_of_student, client):
        if group_id:
            url = student_resources['group_student_list'].format(api_url, group_id)
        elif course_id:
            url = student_resources['course_student_list'].format(api_url, course_id)
        elif group_id and course_id:
            url = student_resources['group&course_student_list'].format(api_url, group_id, course_id)
        else:
            url = student_resources['student_list'].format(api_url)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == number_of_student
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group_name'], (str, type(None))) is True
            assert isinstance(student['course_names'], (str, type(None))) is True

    @pytest.mark.parametrize("group_id, course_id, number_of_student", [
        (None, None, 10),
        (2, None, 3),
        (None, 2, 5),
        (3, 3, 2),
        (1, 1, 3)
    ])
    # full schema
    def test_get_full_schema(self, group_id, course_id, number_of_student, client):
        if group_id:
            url = student_resources['group_full_student_list'].format(api_url, 'true', group_id)
        elif course_id:
            url = student_resources['course_full_student_list'].format(api_url, 'true', course_id)
        elif group_id and course_id:
            url = student_resources['group&course_full_student_list'].format(api_url, 'true', group_id, course_id)
        else:
            url = student_resources['full_student_list'].format(api_url, 'true')
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == number_of_student
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group', 'courses']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group'], (dict, type(None))) is True
            assert isinstance(student['courses'], list) is True

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

    @pytest.mark.parametrize("json_to_send, result_json", [
        # give all correct data
        (
                {"student_id_list": [1, 2]},
                {'message': gettext_("student_list_delete").format([1, 2]),
                 'status': 200}
        ),
        # give one of two incorrect student_id
        (
                {"student_id_list": [3, 2000]},
                {'message': gettext_("student_list_delete").format([3]),
                 'status': 200}
        )

    ])
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


class TestStudentListException:
    @pytest.mark.parametrize("wrong_data", ['smth_wrong', 1000])
    # wrong query string "?full="
    def test_get_wrong_full(self, wrong_data, client):
        url = student_resources['full_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == student_count
        for student in response.json:
            attrs_ = list(student.keys())
            assert attrs_ == ['student_id', 'first_name', 'last_name', 'group_name', 'course_names']
            assert isinstance(student['first_name'], str) is True
            assert isinstance(student['last_name'], str) is True
            assert isinstance(student['group_name'], (str, type(None))) is True
            assert isinstance(student['course_names'], (str, type(None))) is True

    @pytest.mark.parametrize("wrong_data, status", [
        ('smth_wrong', 400),
        (1000, 404)
    ])
    # wrong query string "?group="
    def test_gives_wrong_group(self, wrong_data, status, client):
        url = student_resources['group_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        if isinstance(wrong_data, int):
            assert response.json == {'message': gettext_('group_not_found').format(wrong_data), 'status': 404}

    @pytest.mark.parametrize("wrong_data, status", [
        ('smth_wrong', 400),
        (1000, 404)
    ])
    # wrong query string "?course="
    def test_gives_wrong_course(self, wrong_data, status, client):
        url = student_resources['course_student_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        if isinstance(wrong_data, int):
            assert response.json == {'message': gettext_('course_not_found').format(wrong_data), 'status': 404}

    @pytest.mark.parametrize("json_to_send, status, result_json", [
        # 0 don't give required field:
        (
                [{"group_id": 3, "courses": [1, 2]}],
                400,
                {'err_name': 'ValidationError',
                 'message': {'first_name': ['Missing data for required field.'],
                             'last_name': ['Missing data for required field.']},
                 'status': 400}
        ),
        # 1 incorrect foreign key of group_id:
        pytest.param(
            [{"first_name": "John",
              "last_name": "Marlin",
              "group_id": 3000,
              "courses": [1, 2]}],
            400,
            {'err_name': 'IntegrityError',
             'message': 'FOREIGN KEY constraint failed',
             'status': 400},
            marks=pytest.mark.xfail(reason='incorrect foreign key of group_id')
        ),
        # 2 incorrect course_id:
        (
                [{"first_name": "John",
                  "last_name": "Marlin",
                  "group_id": 3,
                  "courses": [1000, 20]}],
                404,
                {'message': gettext_("course_not_found").format(1000),
                 'status': 404}
        )
    ])
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

    @pytest.mark.parametrize("json_to_send, status, result_json", [
        # 0 student not found:
        (
                [{"group_id": 3, "add_courses": [1, 2]}],
                404,
                {'message': gettext_("student_not_found").format(None),
                 'status': 404}
        ),
        # 1 give 'courses' list instead of 'add_courses' and 'delete_courses' lists:
        (
                [{"student_id": 3, "courses": [1, 2]}],
                400,
                {'message': gettext_("student_err_put_courses"),
                 'status': 400}
        ),
        # 2 incorrect group_id (foreign key):
        pytest.param(
            [{"student_id": 1,
              "group_id": 3000,
              "add_courses": [1, 2]}],
            400,
            {'err_name': 'IntegrityError',
             'message': 'FOREIGN KEY constraint failed',
             'status': 400},
            marks=pytest.mark.xfail(reason='incorrect input data: give nonexistence group_id')
        ),
        # 3 give nonexistent courses:
        (
                [{"student_id": 5,
                  "group_id": 3,
                  "delete_courses": [1000, 20]}],
                404,
                {'message': gettext_("course_not_found").format(1000),
                 'status': 404}
        )
    ])
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

    @pytest.mark.parametrize("json_to_send, result_json, status", [
        # 0 give incorrect student_id_list (delete nonexistence students)
        (
                {"student_id_list": [5000, 2000]},
                {'message': gettext_("student_list_delete_err_no_one"),
                 'status': 400},
                400
        ),
        # 1 give incorrect type student_id
        pytest.param(
            {"student_id_list": ['a', 'b']},
            {'message': gettext_("student_list_delete_err_no_one"),
             'status': 400},
            400,
            marks=pytest.mark.xfail(reason='incorrect input data: given str instead of int')
        )
    ])
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
