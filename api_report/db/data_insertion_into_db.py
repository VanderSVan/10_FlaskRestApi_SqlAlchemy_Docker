# !!! Inserting data into an empty database only !!!

from .db_sqlalchemy import db as initialized_db
from api_report.models.models import StudentModel, GroupModel, CourseModel
from api_report.data.input_data import first_names_list, last_names_list, courses_dict
from api_report.data.data_preparation import (generate_group_instances,
                                              generate_course_instances,
                                              generate_available_places_in_groups,
                                              generate_student_instances)


def insert_data_to_db(db: initialized_db) -> None:
    if (StudentModel.query.count() == 0 and
            GroupModel.query.count() == 0 and
            CourseModel.query.count() == 0):
        # Constants
        number_of_groups = 10
        number_of_students = 200

        # OPEN TRANSACTION:
        # Add groups to db
        db.session.add_all(generate_group_instances(number_of_instance=number_of_groups))

        # Add courses to db
        db.session.add_all(generate_course_instances(courses=courses_dict))

        # Get all course instances from db
        all_courses = db.session.query(CourseModel).all()

        # Create dict with available places as value and group_id as key
        group_ids = generate_available_places_in_groups(lower_limit_of_students=10,
                                                        upper_limit_of_students=30,
                                                        number_of_groups=number_of_groups)

        # Add students with all relationships to db
        db.session.add_all(generate_student_instances(number_of_students=number_of_students,
                                                      first_names=first_names_list,
                                                      last_names=last_names_list,
                                                      groups=group_ids,
                                                      courses=all_courses))

        # CLOSE TRANSACTION.
        db.session.commit()
