# !!! Inserting data into an empty database only !!!

from api_university.db.db_sqlalchemy import db as initialized_db
from api_university.models.student import StudentModel
from api_university.models.group import GroupModel
from api_university.models.course import CourseModel
from api_university.data.input_data import first_names_list, last_names_list, courses_dict
from api_university.data.data_preparation import (generate_group_instances,
                                                  generate_course_instances,
                                                  generate_available_places_in_groups,
                                                  generate_student_instances)


def insert_data_to_db(db: initialized_db,
                      group_count: int,
                      student_count: int,
                      lower_limit_students_in_group: int,
                      upper_limit_of_students_in_group: int) -> None:
    """Inserts prepared data into an empty database only!"""

    if (StudentModel.query.count() == 0 and
            GroupModel.query.count() == 0 and
            CourseModel.query.count() == 0):

        # OPEN TRANSACTION:
        # Add groups to db
        db.session.add_all(generate_group_instances(number_of_instance=group_count))

        # Add courses to db
        db.session.add_all(generate_course_instances(courses=courses_dict))

        # Get all course instances from db
        all_courses = db.session.query(CourseModel).all()

        # Create dict with available places as value and group_id as key
        group_ids = generate_available_places_in_groups(
            lower_limit_of_students=lower_limit_students_in_group,
            upper_limit_of_students=upper_limit_of_students_in_group,
            number_of_groups=group_count
        )

        # Add students with all relationships to db
        db.session.add_all(generate_student_instances(
            number_of_students=student_count,
            first_names=first_names_list,
            last_names=last_names_list,
            groups=group_ids,
            courses=all_courses)
        )

        # CLOSE TRANSACTION.
        db.session.commit()

    else:
        print(f"Database {db} not empty")
