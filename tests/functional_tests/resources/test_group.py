import pytest

from api_university.config import Configuration as Config
from api_university.responses.response_strings import gettext_
from api_university.models.group import GroupModel

from tests.test_data.data import group_count

api_url = Config.API_URL

group_resources = {
    'group': "{}/groups/{}",
    'full_group': "{}/groups/{}?full={}",

    'group_list': "{}/groups",
    'full_group_list': "{}/groups?full={}",
    'group_list_by_student_count': "{}/groups?student_count={}"
}


class TestGroup:
    @pytest.mark.parametrize("group_id", [1, 2, 3])
    # default (short schema)
    def test_get_default_group_schema(self, group_id, client):
        url = group_resources['group'].format(api_url, group_id)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['group_id', 'name']
        assert response.json['group_id'] == group_id
        assert isinstance(response.json['name'], str) is True

    @pytest.mark.parametrize("group_id", [1, 2, 3])
    # full schema
    def test_get_full_default_group_schema(self, group_id, client):
        url = group_resources['full_group'].format(api_url, group_id, 'true')
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['group_id', 'name', 'students']
        assert response.json['group_id'] == group_id
        assert isinstance(response.json['name'], str) is True
        assert isinstance(response.json['students'], list) is True

    @pytest.mark.parametrize("group_id, json_to_send, result_json, student_count", [
        (
                4,
                {"name": "DD-44"},
                {'message': gettext_("group_post").format(4),
                 'status': 200},
                0
        ),
        (
                5,
                {"name": "EE-55",
                 "students": [1, 3, 5]},
                {'message': gettext_("group_post").format(5),
                 'status': 200},
                3
        )
    ])
    def test_post(self, group_id, json_to_send, result_json, student_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = group_resources['group'].format(api_url, group_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert GroupModel.find_by_id(group_id) is not None
        assert len(GroupModel.get_group_students(group_id)) == student_count

    @pytest.mark.parametrize("group_id, json_to_send, result_json, student_count", [
        (
                1,
                {"name": "DD-44"},
                {'message': gettext_("group_put").format(1),
                 'status': 200},
                3
        ),
        (
                3,
                {"add_students": [1, 5, 6],
                 "delete_students": [8, 10],
                 "name": "XY-77"},
                {'message': gettext_("group_put").format(3),
                 'status': 200},
                3
        )
    ])
    def test_put(self, group_id, json_to_send, result_json, student_count, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = group_resources['group'].format(api_url, group_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == 200
        assert response.content_type == mimetype
        assert response.json == result_json
        assert len(GroupModel.get_group_students(group_id)) == student_count

    @pytest.mark.parametrize("group_id, result_json, remaining_group_count", [
        (
                1,
                {'message': gettext_("group_delete").format(1),
                 'status': 200},
                2
        ),
        (
                3,
                {'message': gettext_("group_delete").format(3),
                 'status': 200},
                2
        )
    ])
    def test_delete(self, group_id, result_json, remaining_group_count, client):
        url = group_resources['group'].format(api_url, group_id)
        response = client.delete(url)
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == result_json
        assert len(GroupModel.get_all_groups()) == remaining_group_count


class TestGroupException:
    @pytest.mark.parametrize("group_id, wrong_data", [
        (1, 'smth_wrong'),
        (2, 1000)
    ])
    # wrong query string "?full="
    def test_get_wrong_full(self, group_id, wrong_data, client):
        url = group_resources['full_group'].format(api_url, group_id, wrong_data)
        response = client.get(url)
        attrs_ = list(response.json.keys())
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert attrs_ == ['group_id', 'name']
        assert response.json['group_id'] == group_id
        assert isinstance(response.json['name'], str) is True

    @pytest.mark.parametrize("group_id, json_to_send, status, result_json", [
        # 0 don't give required field:
        (
                4,
                {"students": [1, 2]},
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
                {'message': gettext_("group_exists").format(1),
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
    def test_post_wrong_group(self, group_id, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = group_resources['group'].format(api_url, group_id)
        response = client.post(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("group_id, json_to_send, status, result_json", [
        # 0 course not found
        (
                4,
                {"name": "TT-99"},
                404,
                {'message': gettext_("group_not_found").format(4),
                 'status': 404}
        ),
        # 1 give 'students' list instead of 'add_students' and 'delete_students' lists
        (
                1,
                {"students": [1, 2, 3]},
                400,
                {"message": gettext_("group_err_put_students"),
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
    def test_put_wrong_group(self, group_id, json_to_send, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = group_resources['group'].format(api_url, group_id)
        response = client.put(url, json=json_to_send, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json

    @pytest.mark.parametrize("group_id, result_json, status", [
        # 0 delete nonexistence course
        (
                100,
                {'message': gettext_("group_not_found").format(100),
                 'status': 404},
                404
        )
    ])
    def test_delete_wrong_group(self, group_id, status, result_json, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'accept': mimetype
        }
        url = group_resources['group'].format(api_url, group_id)
        response = client.delete(url, headers=headers)
        assert response.status_code == status
        assert response.content_type == mimetype
        assert response.json == result_json


class TestGroupList:
    # default (short schema)
    def test_get_default_schema(self, client):
        url = group_resources['group_list'].format(api_url)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == group_count
        for group in response.json:
            attrs_ = list(group.keys())
            assert attrs_ == ['group_id', 'name']
            assert isinstance(group['name'], str) is True

    # full schema
    def test_get_full_schema(self, client):
        url = group_resources['full_group_list'].format(api_url, 'true')
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == group_count
        for full_group in response.json:
            attrs_ = list(full_group.keys())
            assert attrs_ == ['group_id', 'name', 'students']
            assert isinstance(full_group['name'], str) is True
            assert isinstance(full_group['students'], list) is True

    @pytest.mark.parametrize("student_count, number_of_group", [(1, 0), (3, 3), (6, 3)])
    def test_get_groups_filter_by_student_count(self, student_count, number_of_group, client):
        url = group_resources['group_list_by_student_count'].format(api_url, student_count)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == number_of_group
        for group in response.json:
            attrs_ = list(group.keys())
            assert attrs_ == ['group_id', 'name']
            assert isinstance(group['name'], str) is True


class TestGroupListException:
    @pytest.mark.parametrize("wrong_data", ['smth_wrong', 1000])
    # wrong query string "?full="
    def test_get_wrong_full(self, wrong_data, client):
        url = group_resources['full_group_list'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json) == group_count
        for group in response.json:
            attrs_ = list(group.keys())
            assert attrs_ == ['group_id', 'name']
            assert isinstance(group['name'], str) is True

    @pytest.mark.parametrize("wrong_data, status, result_json", [
        (
                'smth_wrong',
                400,
                {'message': {'student_count': "invalid literal for int() with base 10: "
                                              "'smth_wrong'"}}
        ),
        (
                1000,
                200,
                [{'group_id': 1, 'name': 'AA-11'},
                 {'group_id': 2, 'name': 'BB-22'},
                 {'group_id': 3, 'name': 'CC-33'}]
        )
    ])
    # wrong query string "?student_count="
    def test_get_wrong_student_count(self, wrong_data, status, result_json, client):
        url = group_resources['group_list_by_student_count'].format(api_url, wrong_data)
        response = client.get(url)
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        assert response.json == result_json
