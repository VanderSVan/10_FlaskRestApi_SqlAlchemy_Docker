import pytest
from unittest.mock import patch, Mock

from api_university.data.data_preparation import (
    _generate_group_name,
    _assign_student_to_group,
    generate_available_places_in_groups,
    generate_group_instances,
    generate_course_instances,
    generate_student_instances
)


class TestDataPreparation:
    @patch("api_university.data.data_preparation.randint")
    def test_generate_available_places_in_groups(self, mock_randint):
        # input_data:
        lower_limit_of_students = 5
        upper_limit_of_students = 10
        number_of_groups = 5

        # processed data:
        mock_randint.side_effect = (5, 10, 7, 9, 7)
        assert generate_available_places_in_groups(lower_limit_of_students,
                                                   upper_limit_of_students,
                                                   number_of_groups) == {1: 5, 2: 10, 3: 7, 4: 9, 5: 7}

    @patch("api_university.data.data_preparation.randint")
    @patch("api_university.data.data_preparation.choices")
    def test_generate_group_name(self, mock_choices, mock_randint):
        # input_data:
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        separator = "-"

        # processed data:
        mock_choices.return_value = ["A", "F"]
        mock_randint.return_value = 56
        assert _generate_group_name(letters, separator) == "AF-56"

    @patch("api_university.data.data_preparation._generate_group_name")
    def test_generate_group_instances(self, mock_gen_group_name):
        # input_data:
        group_count = 3
        group_names = ["DS-37", "AF-56", "XY-93"]

        # processed data:
        group_objects = [Mock(group_id=group_id, name=name) for group_id, name in enumerate(group_names, start=1)]

        with patch("api_university.data.data_preparation.GroupModel", side_effect=group_objects):
            assert generate_group_instances(group_count) == group_objects

    def test_generate_course_instances(self):
        # input_data:
        course_dict = {'Math': 'smth1', 'Physics': 'smth2', 'English': 'smth3'}

        # processed data:
        course_objects = [Mock(course_id=course_id,
                               name=course[0].title(),
                               description=course[1].title())
                          for course_id, course in
                          enumerate(course_dict.items(), start=1)]

        with patch("api_university.data.data_preparation.CourseModel", side_effect=course_objects):
            assert generate_course_instances(course_dict) == course_objects

    @pytest.mark.parametrize('test_available_places_in_groups, group_id_output', [
        ({1: 1, 2: 5, 3: 10}, 1),
        ({1: 0, 2: 5, 3: 10}, 2),
        ({1: 0, 2: 0, 3: 10}, 3),
        ({1: 0, 2: 0, 3: 0}, None)
    ])
    def test_assign_student_to_group(self, test_available_places_in_groups, group_id_output):
        assert _assign_student_to_group(test_available_places_in_groups) == group_id_output

    def test_generate_student_instances(self):
        # input_data:
        number_of_students = 3
        first_names = ['JAMES', 'JOHN', 'ROBERT']
        last_names = ['JONES', 'SMITH', 'JOHNSON']
        available_places_in_groups = {1: 1, 2: 5, 3: 10}
        courses = ['CourseModel 1', 'CourseModel 2', 'CourseModel 3']  # must be an object of the CourseModel class

        # processed data:
        processed_first_names = ['James', 'John', 'Robert']
        processed_last_names = ['Jones', 'Smith', 'Johnson']
        processed_group_id = [1, 2, 2]
        processed_courses = [['CourseModel 1', 'CourseModel 2'],
                             ['CourseModel 1'],
                             ['CourseModel 2', 'CourseModel 3']]
        student_objects = [Mock(student_id=student_id,
                                first_name=first_name,
                                last_name=last_name,
                                group_id=group_id,
                                courses=course)
                           for student_id, (first_name, last_name, group_id, course) in
                           enumerate(zip(processed_first_names, processed_last_names,
                                         processed_group_id, processed_courses))]

        with patch("api_university.data.data_preparation.StudentModel", side_effect=student_objects):
            assert (generate_student_instances(number_of_students,
                                               first_names,
                                               last_names,
                                               available_places_in_groups,
                                               courses)) == student_objects
