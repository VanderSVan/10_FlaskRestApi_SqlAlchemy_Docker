import pytest

from api_university.config import Configuration as Config
from api_university.responses.response_strings import gettext_
from api_university.models.course import CourseModel

from tests.test_data.data import course_count

api_url = Config.API_URL

course_resources = {
    'course': "{}/courses/{}",
    'full_course': "{}/courses/{}?full={}",

    'course_list': "{}/courses",
    'full_course_list': "{}/courses?full={}",
}


class TestCourse:
    @pytest.mark.parametrize("course_id", [1, 2, 3])
    # default (short schema)
    def test_get_default_schema(self, course_id, client):
        url = course_resources['course'].format(api_url, course_id)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['course_id', 'name']
        assert response.json['course_id'] == course_id
        assert isinstance(response.json['name'], str) is True

    @pytest.mark.parametrize("course_id", [1, 2, 3])
    # full schema
    def test_get_full_default_schema(self, course_id, client):
        url = course_resources['full_course'].format(api_url, course_id, 'true')
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['course_id', 'name', 'description', 'students']
        assert response.json['course_id'] == course_id
        assert isinstance(response.json['name'], str) is True
        assert isinstance(response.json['description'], (str, type(None))) is True
        assert isinstance(response.json['students'], list) is True

    @pytest.mark.parametrize("course_id, json_to_send, result_json, student_count", [
        (
                4,
                {"description": "It's pain",
                 "name": "Physics"},
                {'message': gettext_("course_post").format(4),
                 'status': 200},
                0
        ),
        (
                5,
                {"description": "It's wonderful",
                 "name": "Relaxation",
                 "students": [1, 3, 5]},
                {'message': gettext_("course_post").format(5),
                 'status': 200},
                3
        )
    ])
    def test_post(self, course_id, json_to_send, result_json, student_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = course_resources['course'].format(api_url, course_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert CourseModel.find_by_id(course_id) is not None
        assert len(CourseModel.get_course_students(course_id)) == student_count

    @pytest.mark.parametrize("course_id, json_to_send, result_json, student_count", [
        (
                1,
                {"description": "Math, Math, again Math",
                 "name": "Math"},
                {'message': gettext_("course_put").format(1),
                 'status': 200},
                6
        ),
        (
                3,
                {"add_students": [1, 3],
                 "delete_students": [2, 4, 7, 9],
                 "description": "Come on learn it",
                 "name": "English"},
                {'message': gettext_("course_put").format(3),
                 'status': 200},
                2
        )
    ])
    def test_put(self, course_id, json_to_send, result_json, student_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = course_resources['course'].format(api_url, course_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert len(CourseModel.get_course_students(course_id)) == student_count

    @pytest.mark.parametrize("course_id, result_json, remaining_course_count", [
        (
                1,
                {'message': gettext_("course_delete").format(1),
                 'status': 200},
                2
        ),
        (
                3,
                {'message': gettext_("course_delete").format(3),
                 'status': 200},
                2
        )
    ])
    def test_delete(self, course_id, result_json, remaining_course_count, client):
        url = course_resources['course'].format(api_url, course_id)
        response = client.delete(url)
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == result_json
        assert len(CourseModel.get_all_courses()) == remaining_course_count


class TestCourseException:
    @pytest.mark.parametrize("course_id, wrong_data", [
        (1, 'smth_wrong'),
        (2, 1000)
    ])
    # wrong query string "?full="
    def test_get_wrong_full(self, course_id, wrong_data, client):
        url = course_resources['full_course'].format(api_url, course_id, wrong_data)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['course_id', 'name']
        assert response.json['course_id'] == course_id
        assert isinstance(response.json['name'], str) is True

    @pytest.mark.parametrize("course_id, json_to_send, status, result_json", [
        # 0 don't give required field:
        (
                4,
                {"description": "smth", "students": [1, 2]},
                400,
                {'err_name': 'ValidationError',
                 'message': {'name': ['Missing data for required field.']},
                 'status': 400}
        ),
        # 1 course already exists:
        (
                1,
                {"name": "Physics"},
                400,
                {'message': gettext_("course_exists").format(1),
                 'status': 400}
        ),
        # 2 give nonexistent students
        (
                4,
                {"name": "some_course", "students": [1000, 2000]},
                404,
                {'message': gettext_("student_not_found").format(1000),
                 'status': 404}
        )
    ])
    def test_post_wrong_course(self, course_id, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = course_resources['course'].format(api_url, course_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("course_id, json_to_send, status, result_json", [
        # 0 course not found
        (
                4,
                {"name": "Physics"},
                404,
                {'message': gettext_("course_not_found").format(4),
                 'status': 404}
        ),
        # 1 give 'students' list instead of 'add_students' and 'delete_students' lists
        (
                1,
                {"students": [1, 2, 3]},
                400,
                {"message": gettext_("course_err_put_students"),
                 "status": 400}
        ),
        # 2 give nonexistent students
        (
                3,
                {"add_students": [1000, 2000]},
                404,
                {'message': gettext_("student_not_found").format(1000),
                 'status': 404}
        )
    ])
    def test_put_wrong_course(self, course_id, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = course_resources['course'].format(api_url, course_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("course_id, result_json, status", [
        # 0 delete nonexistence course
        (
            100,
            {'message': gettext_("course_not_found").format(100),
             'status': 404},
            404
        )
    ])
    def test_delete_wrong_course(self, course_id, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = course_resources['course'].format(api_url, course_id)
        response = client.delete(url, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json


class TestCourseList:
    # default (short schema)
    def test_get_default_schema(self, client):
        url = course_resources['course_list'].format(api_url)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == course_count
        for course in response.json:
            attrs_ = list(course.keys())
            assert attrs_ == ['course_id', 'name']
            assert isinstance(course['name'], str) is True

    # full schema
    def test_get_full_schema(self, client):
        url = course_resources['full_course_list'].format(api_url, 'true')
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == course_count
        for full_course in response.json:
            attrs_ = list(full_course.keys())
            assert attrs_ == ['course_id', 'name', 'description', 'students']
            assert isinstance(full_course['name'], str) is True
            assert isinstance(full_course['description'], str) is True
            assert isinstance(full_course['students'], list) is True


@pytest.mark.parametrize("wrong_data", ['smth_wrong', 1000])
class TestCourseListException:
    # wrong query string "?full="
    def test_get_wrong_full(self, wrong_data, client):
        url = course_resources['full_course_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == course_count
        for course in response.json:
            attrs_ = list(course.keys())
            assert attrs_ == ['course_id', 'name']
            assert isinstance(course['name'], str) is True



